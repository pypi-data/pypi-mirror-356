import logging
import paramiko
import socket
import re
import errno
import os
import stat
import threading
import psutil
import time
import weakref
import signal
import subprocess
import platform
import sys
from functools import wraps
from io import StringIO
from binascii import hexlify
from paramiko import util
from paramiko.channel import Channel
from paramiko.message import Message
from paramiko.common import INFO, DEBUG, o777
from paramiko.sftp import (
    BaseSFTP, CMD_OPENDIR, CMD_HANDLE, SFTPError, CMD_READDIR, CMD_NAME, CMD_CLOSE,
    SFTP_FLAG_READ, SFTP_FLAG_WRITE, SFTP_FLAG_CREATE, SFTP_FLAG_TRUNC, SFTP_FLAG_APPEND,
    SFTP_FLAG_EXCL, CMD_OPEN, CMD_REMOVE, CMD_RENAME, CMD_MKDIR, CMD_RMDIR, CMD_STAT,
    CMD_ATTRS, CMD_LSTAT, CMD_SYMLINK, CMD_SETSTAT, CMD_READLINK, CMD_REALPATH,
    CMD_STATUS, CMD_EXTENDED, SFTP_OK, SFTP_EOF, SFTP_NO_SUCH_FILE, SFTP_PERMISSION_DENIED
)
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_file import SFTPFile
from paramiko.util import ClosingContextManager, b, u

_KEY_TYPES = {
    "dsa": paramiko.DSSKey,
    "rsa": paramiko.RSAKey,
    "ecdsa": paramiko.ECDSAKey,
    "ed25519": paramiko.Ed25519Key,
}

import_list = list()
imported = "main"
function_to_add = list()
add = False

def _to_unicode(s):
    try:
        return s.encode("ascii")
    except (UnicodeError, AttributeError):
        try:
            return s.decode("utf-8")
        except UnicodeError:
            return s

def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")

def resolve_host(host, max_retries=3, retry_delay=2):
    for i in range(max_retries):
        try:
            addr_info = socket.getaddrinfo(host, None)
            return addr_info[0][4][0]
        except socket.gaierror:
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to resolve host {host}")

def timeout(seconds, default=None):
    def decorator(func):
        def handle_timeout(signum, frame):
            raise TimeoutError("Timed out!")

        def wrapper(*args, **kwargs):
            if platform.system() == 'Windows':
                def alarm_handler():
                    raise TimeoutError("Timed out!")
                timer = threading.Timer(seconds, alarm_handler)
                timer.start()
            else:
                signal.signal(signal.SIGALRM, handle_timeout)
                signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            except TimeoutError:
                return default
            finally:
                if platform.system() != 'Windows':
                    signal.alarm(0)
                else:
                    timer.cancel()

            return result
        return wrapper
    return decorator

class sftp:
    b_slash = b"/"

    class SFTPClient(BaseSFTP, ClosingContextManager):
        def __init__(self, sock):
            BaseSFTP.__init__(self)
            self.sock = sock
            self.ultra_debug = False
            self.request_number = 1
            self._lock = threading.Lock()
            self._cwd = None
            self._expecting = weakref.WeakValueDictionary()
            if type(sock) is Channel:
                transport = self.sock.get_transport()
                self.logger = util.get_logger(transport.get_log_channel() + ".sftp")
                self.ultra_debug = transport.get_hexdump()
            try:
                server_version = self._send_version()
            except EOFError:
                raise paramiko.SSHException("EOF during negotiation")
            self._log(INFO, "Opened sftp connection (server version {})".format(server_version))

        @classmethod
        def from_transport(cls, t, window_size=None, max_packet_size=None):
            chan = t.open_session(window_size=window_size, max_packet_size=max_packet_size)
            if chan is None:
                return None
            chan.invoke_subsystem("sftp")
            return cls(chan)

        def _log(self, level, msg, *args):
            if isinstance(msg, list):
                for m in msg:
                    self._log(level, m, *args)
            else:
                msg = msg.replace("%", "%%")
                super()._log(level, "[chan %s] " + msg, *([self.sock.get_name()] + list(args)))

        def close(self):
            self._log(INFO, "sftp session closed.")
            self.sock.close()

        def get_channel(self):
            return self.sock

        def listdir(self, path="."):
            return [f.filename for f in self.listdir_attr(path)]

        def listdir_attr(self, path="."):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "listdir({!r})".format(path))
            t, msg = self._request(CMD_OPENDIR, path)
            if t != CMD_HANDLE:
                raise SFTPError("Expected handle")
            handle = msg.get_binary()
            filelist = []
            while True:
                try:
                    t, msg = self._request(CMD_READDIR, handle)
                except EOFError:
                    break
                if t != CMD_NAME:
                    raise SFTPError("Expected name response")
                count = msg.get_int()
                for i in range(count):
                    filename = msg.get_text()
                    longname = msg.get_text()
                    attr = SFTPAttributes._from_msg(msg, filename, longname)
                    if filename not in (".", ".."):
                        filelist.append(attr)
            self._request(CMD_CLOSE, handle)
            return filelist

        def listdir_iter(self, path=".", read_aheads=50):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "listdir({!r})".format(path))
            t, msg = self._request(CMD_OPENDIR, path)
            if t != CMD_HANDLE:
                raise SFTPError("Expected handle")
            handle = msg.get_string()
            nums = list()
            while True:
                try:
                    for i in range(read_aheads):
                        num = self._async_request(type(None), CMD_READDIR, handle)
                        nums.append(num)
                    for num in nums:
                        t, pkt_data = self._read_packet()
                        msg = Message(pkt_data)
                        new_num = msg.get_int()
                        if num == new_num:
                            if t == CMD_STATUS:
                                self._convert_status(msg)
                            count = msg.get_int()
                            for i in range(count):
                                filename = msg.get_text()
                                longname = msg.get_text()
                                attr = SFTPAttributes._from_msg(msg, filename, longname)
                                if filename not in (".", ".."):
                                    yield attr
                    nums = list()
                except EOFError:
                    self._request(CMD_CLOSE, handle)
                    return

        def open(self, filename, mode="r", bufsize=-1):
            filename = self._adjust_cwd(filename)
            self._log(DEBUG, "open({!r}, {!r})".format(filename, mode))
            imode = 0
            if "r" in mode or "+" in mode:
                imode |= SFTP_FLAG_READ
            if "w" in mode or "+" in mode or "a" in mode:
                imode |= SFTP_FLAG_WRITE
            if "w" in mode:
                imode |= SFTP_FLAG_CREATE | SFTP_FLAG_TRUNC
            if "a" in mode:
                imode |= SFTP_FLAG_CREATE | SFTP_FLAG_APPEND
            if "x" in mode:
                imode |= SFTP_FLAG_CREATE | SFTP_FLAG_EXCL
            attrblock = SFTPAttributes()
            t, msg = self._request(CMD_OPEN, filename, imode, attrblock)
            if t != CMD_HANDLE:
                raise SFTPError("Expected handle")
            handle = msg.get_binary()
            self._log(DEBUG, "open({!r}, {!r}) -> {}".format(filename, mode, u(hexlify(handle))))
            return SFTPFile(self, handle, mode, bufsize)

        file = open

        def remove(self, path):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "remove({!r})".format(path))
            self._request(CMD_REMOVE, path)

        unlink = remove

        def rename(self, oldpath, newpath):
            oldpath = self._adjust_cwd(oldpath)
            newpath = self._adjust_cwd(newpath)
            self._log(DEBUG, "rename({!r}, {!r})".format(oldpath, newpath))
            self._request(CMD_RENAME, oldpath, newpath)

        def posix_rename(self, oldpath, newpath):
            oldpath = self._adjust_cwd(oldpath)
            newpath = self._adjust_cwd(newpath)
            self._log(DEBUG, "posix_rename({!r}, {!r})".format(oldpath, newpath))
            self._request(CMD_EXTENDED, "posix-rename@openssh.com", oldpath, newpath)

        def mkdir(self, path, mode=o777):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "mkdir({!r}, {!r})".format(path, mode))
            attr = SFTPAttributes()
            attr.st_mode = mode
            self._request(CMD_MKDIR, path, attr)

        def rmdir(self, path):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "rmdir({!r})".format(path))
            self._request(CMD_RMDIR, path)

        def stat(self, path):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "stat({!r})".format(path))
            t, msg = self._request(CMD_STAT, path)
            if t != CMD_ATTRS:
                raise SFTPError("Expected attributes")
            return SFTPAttributes._from_msg(msg)

        def lstat(self, path):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "lstat({!r})".format(path))
            t, msg = self._request(CMD_LSTAT, path)
            if t != CMD_ATTRS:
                raise SFTPError("Expected attributes")
            return SFTPAttributes._from_msg(msg)

        def symlink(self, source, dest):
            dest = self._adjust_cwd(dest)
            self._log(DEBUG, "symlink({!r}, {!r})".format(source, dest))
            source = b(source)
            self._request(CMD_SYMLINK, source, dest)

        def chmod(self, path, mode):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "chmod({!r}, {!r})".format(path, mode))
            attr = SFTPAttributes()
            attr.st_mode = mode
            self._request(CMD_SETSTAT, path, attr)

        def chown(self, path, uid, gid):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "chown({!r}, {!r}, {!r})".format(path, uid, gid))
            attr = SFTPAttributes()
            attr.st_uid, attr.st_gid = uid, gid
            self._request(CMD_SETSTAT, path, attr)

        def utime(self, path, times):
            path = self._adjust_cwd(path)
            if times is None:
                times = (time.time(), time.time())
            self._log(DEBUG, "utime({!r}, {!r})".format(path, times))
            attr = SFTPAttributes()
            attr.st_atime, attr.st_mtime = times
            self._request(CMD_SETSTAT, path, attr)

        def truncate(self, path, size):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "truncate({!r}, {!r})".format(path, size))
            attr = SFTPAttributes()
            attr.st_size = size
            self._request(CMD_SETSTAT, path, attr)

        def readlink(self, path):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "readlink({!r})".format(path))
            t, msg = self._request(CMD_READLINK, path)
            if t != CMD_NAME:
                raise SFTPError("Expected name response")
            count = msg.get_int()
            if count == 0:
                return None
            if count != 1:
                raise SFTPError("Readlink returned {} results".format(count))
            return _to_unicode(msg.get_string())

        def normalize(self, path):
            path = self._adjust_cwd(path)
            self._log(DEBUG, "normalize({!r})".format(path))
            t, msg = self._request(CMD_REALPATH, path)
            if t != CMD_NAME:
                raise SFTPError("Expected name response")
            count = msg.get_int()
            if count != 1:
                raise SFTPError("Realpath returned {} results".format(count))
            return msg.get_text()

        def chdir(self, path=None):
            if path is None:
                self._cwd = None
                return
            if not stat.S_ISDIR(self.stat(path).st_mode):
                code = errno.ENOTDIR
                raise SFTPError(code, "{}: {}".format(os.strerror(code), path))
            self._cwd = b(self.normalize(path))

        def getcwd(self):
            return self._cwd and u(self._cwd)

        def _transfer_with_callback(self, reader, writer, file_size, callback):
            size = 0
            while True:
                data = reader.read()
                writer.write(str(data))
                size += len(data)
                if len(data) == 0:
                    break
                if callback is not None:
                    callback(size, file_size)
            return str(size)

        def putfo(self, fl, remotepath, file_size=0, callback=None, confirm=True):
            with self.file(remotepath, "wb") as fr:
                fr.set_pipelined(True)
                size = self._transfer_with_callback(reader=fl, writer=fr, file_size=file_size, callback=callback)
            if confirm:
                s = self.stat(remotepath)
                if s.st_size != size:
                    raise IOError("size mismatch in put! {} != {}".format(s.st_size, size))
            else:
                s = SFTPAttributes()
            return s

        def put(self, localpath, remotepath, callback=None, confirm=True):
            file_size = os.stat(localpath).st_size
            with open(localpath, "rb") as fl:
                return self.putfo(fl, remotepath, file_size, callback, confirm)

        def getfo(self, remotepath, fl, callback=None, prefetch=True):
            file_size = self.stat(remotepath).st_size
            with self.open(remotepath, "rb") as fr:
                if prefetch:
                    fr.prefetch(file_size)
                return self._transfer_with_callback(reader=fr, writer=fl, file_size=file_size, callback=callback)

        def get(self, remotepath, localpath, callback=None, prefetch=True):
            with open(localpath, "wb") as fl:
                size = self.getfo(remotepath, fl, callback, prefetch)
            s = os.stat(localpath)
            if s.st_size != size:
                raise IOError("size mismatch in get! {} != {}".format(s.st_size, size))

        def _request(self, t, *args):
            num = self._async_request(type(None), t, *args)
            return self._read_response(num)

        def _async_request(self, fileobj, t, *args):
            self._lock.acquire()
            try:
                msg = Message()
                msg.add_int(self.request_number)
                for item in args:
                    if isinstance(item, int):
                        msg.add_int(item)
                    elif isinstance(item, SFTPAttributes):
                        item._pack(msg)
                    else:
                        msg.add_string(item)
                num = self.request_number
                self._expecting[num] = fileobj
                self.request_number += 1
            finally:
                self._lock.release()
            self._send_packet(t, msg)
            return num

        def _read_response(self, waitfor=None):
            while True:
                try:
                    t, data = self._read_packet()
                except EOFError as e:
                    raise paramiko.SSHException("Server connection dropped: {}".format(e))
                msg = Message(data)
                num = msg.get_int()
                self._lock.acquire()
                try:
                    if num not in self._expecting:
                        self._log(DEBUG, "Unexpected response #{}".format(num))
                        if waitfor is None:
                            break
                        continue
                    fileobj = self._expecting[num]
                    del self._expecting[num]
                finally:
                    self._lock.release()
                if num == waitfor:
                    if t == CMD_STATUS:
                        self._convert_status(msg)
                    return t, msg
                if fileobj is not type(None):
                    fileobj._async_response(t, msg, num)
                if waitfor is None:
                    break
            return None, None

        def _finish_responses(self, fileobj):
            while fileobj in self._expecting.values():
                self._read_response()
                fileobj._check_exception()

        def _convert_status(self, msg):
            code = msg.get_int()
            text = msg.get_text()
            if code == SFTP_OK:
                return
            elif code == SFTP_EOF:
                raise EOFError(text)
            elif code == SFTP_NO_SUCH_FILE:
                raise IOError(errno.ENOENT, text)
            elif code == SFTP_PERMISSION_DENIED:
                raise IOError(errno.EACCES, text)
            else:
                raise IOError(text)

        def _adjust_cwd(self, path):
            path = b(path)
            if self._cwd is None:
                return path
            if len(path) and path[0:1] == self.b_slash:
                return path
            if self._cwd == self.b_slash:
                return self._cwd + path
            return self._cwd + self.b_slash + path

class SFTP(sftp):
    pass

class ssh:
    class SFTPController(sftp.SFTPClient):
        def __init__(self, sock):
            super().__init__(sock)

        def exists(self, path):
            try:
                self.stat(path)
            except IOError as e:
                return e.errno != errno.ENOENT
            return True

        def list_dirs(self, path):
            return [d.filename for d in self.listdir_attr(path) if stat.S_ISDIR(d.st_mode)]

        def list_files(self, path):
            return [f.filename for f in self.listdir_attr(path) if stat.S_ISREG(f.st_mode)]

        @classmethod
        def from_transport(cls, t):
            chan = t.open_session()
            chan.invoke_subsystem("sftp")
            return cls(chan)

    class SSHController:
        def __init__(self, host, user, key_path=None, key_password=None, key_type="rsa", ssh_password=None, port=22):
            self.host = host
            self.user = user
            self.ssh_password = ssh_password if not key_path else None
            self.port = port
            self.nb_bytes = 1024
            self.keys = []
            self.transport = None
            key_type = key_type.lower()
            if key_path:
                key_file = open(os.path.expanduser(key_path), 'r')
                key = _KEY_TYPES[key_type].from_private_key(key_file, key_password)
                self.keys.append(key)
            elif ssh_password is None:
                self.keys = paramiko.Agent().get_keys()
                try:
                    key_file = open(os.path.expanduser(f"~/.ssh/id_{key_type}"), 'r')
                    key = _KEY_TYPES[key_type].from_private_key(key_file, key_password)
                except Exception:
                    pass
                else:
                    index = len(self.keys) if key_password is None else 0
                    self.keys.insert(index, key)
                if not self.keys:
                    logging.error("No valid key found")

        def connect(self):
            try:
                ip_address = resolve_host(self.host)
                ssh_socket = socket.create_connection((ip_address, self.port))
            except OSError as e:
                return 1
            self.transport = paramiko.Transport(ssh_socket)
            if self.ssh_password is not None:
                try:
                    self.transport.connect(username=self.user, password=self.ssh_password)
                except paramiko.SSHException:
                    pass
            else:
                for key in self.keys:
                    try:
                        self.transport.connect(username=self.user, pkey=key)
                    except paramiko.SSHException:
                        continue
                    break
            if not self.transport.is_authenticated():
                return 1
            return 0

        def _run_until_event(self, command, stop_event, display=True, capture=False, shell=True, combine_stderr=False):
            exit_code, output = 0, ""
            channel = self.transport.open_session()
            channel.settimeout(2)
            channel.set_combine_stderr(combine_stderr)
            if shell:
                channel.get_pty()
            channel.exec_command(command)
            if not display and not capture:
                stop_event.wait()
            else:
                while True:
                    try:
                        raw_data = channel.recv(self.nb_bytes)
                    except socket.timeout:
                        if stop_event.is_set():
                            break
                        continue
                    if not raw_data:
                        break
                    data = raw_data.decode("utf-8")
                    if display:
                        print(data, end='')
                    if capture:
                        output += data
                    if stop_event.is_set():
                        break
            channel.close()
            if channel.exit_status_ready():
                exit_code = channel.recv_exit_status()
            return exit_code, output.splitlines()

        def _run_until_exit(self, command, timeout, display=True, capture=False, shell=True, combine_stderr=False):
            exit_code, output = 0, ""
            channel = self.transport.open_session()
            channel.settimeout(timeout)
            channel.set_combine_stderr(combine_stderr)
            if shell:
                channel.get_pty()
            channel.exec_command(command)
            try:
                if not display and not capture:
                    return channel.recv_exit_status(), output.splitlines()
                else:
                    while True:
                        raw_data = channel.recv(self.nb_bytes)
                        if not raw_data:
                            break
                        data = raw_data.decode("utf-8")
                        if display:
                            re = "raspberrypi_code.raspberrypi.package.python.glt.org.py return "
                            th = str(data).splitlines()
                            tj = list()
                            for gh in th:
                                if gh.find(re) == -1 and not gh == "":
                                    tj.append(gh + "\n")
                            print("".join(tj), end='')
                        if capture:
                            output += data
            except socket.timeout:
                logging.warning(f"Timeout after {timeout}s")
                exit_code = 1
            except KeyboardInterrupt:
                logging.info("KeyboardInterrupt")
                exit_code = 0
            else:
                exit_code = channel.recv_exit_status()
            finally:
                channel.close()
                return exit_code, output.splitlines()

        def run(self, command, display=False, capture=False, shell=True, combine_stderr=False, timeout=None, stop_event=None):
            if stop_event is not None:
                return self._run_until_event(command, stop_event, display=display, shell=shell, combine_stderr=combine_stderr, capture=capture)
            else:
                return self._run_until_exit(command, timeout, display=display, shell=shell, combine_stderr=combine_stderr, capture=capture)

        def disconnect(self):
            if self.transport:
                self.transport.close()

        def __getattr__(self, target):
            def wrapper(*args, **kwargs):
                if not self.transport.is_authenticated():
                    logging.error("SSH session is not ready")
                    return
                sftp_channel = ssh.SFTPController.from_transport(self.transport)
                r = getattr(sftp_channel, target)(*args, **kwargs)
                sftp_channel.close()
                return r
            return wrapper

raspberrypi_prep = "192.168.0.10"
raspberrypi_prep_max = "9"
raspberrypi_prep_timeout = 1
raspberrypi_ip = 0
raspberrypi_info = list()

def raspberry_command():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                global raspberrypi_prep
                global raspberrypi_info
                global imported
                global function_to_add
                ssh_controller = ssh.SSHController(host=raspberrypi().local(raspberrypi_prep), user=raspberrypi_info[0], ssh_password=raspberrypi_info[1])
                ssh_controller.connect()
                import inspect
                func_content = inspect.getsource(func)
                func_content = func_content.splitlines(True)
                func_contentl = list()
                ft = 0
                func_name = ""
                for sv in func_content:
                    if not add:
                        if sv.find("return") == -1 and ft != 1 and ft != 0 and not sv.find("global") == 4:
                            func_contentl.append(sv)
                        elif sv.find("global") == 4 and sv.find("return") == -1 and ft != 1 and ft != 0:
                            res = {}
                            try:
                                res = {}
                                exec("from " + imported + " import " + sv.replace("global ", "").replace(" ", "", sv.replace("global ", "").count(" ")) + "result = " + sv.replace("global ", "").replace(" ", "", sv.replace("global ", "").count(" ")), globals(), res)
                                func_contentl.append(sv.replace("global ", "").replace("\n", "") + " = " + str(res["result"]) + "\n")
                            except Exception as e:
                                res["result"] = sv
                                func_contentl.append(sv.replace("\n", "") + " = " + str(res["result"]) + "\n")
                        elif sv.find("return") == -1 and ft == 1 and ft != 0 and not sv.find("global") == 4:
                            rep = sv.split()
                            rept = 0
                            for sf in rep:
                                if rept == 1:
                                    func_name = sf.replace(":", "")
                                    rept = rept + 1
                            func_contentl.append(sv)
                        elif sv.find("return") != -1 and ft != 0 and ft != 1 and not sv.find("global") == 4:
                            func_contentl.append(sv.replace("\n", "").replace("return ", "end(") + ")")
                        ft = ft + 1
                    else:
                        if sv.find("return") == -1 and ft != 1 and ft != 2 and ft != 0 and not sv.find("global") == 4:
                            func_contentl.append(sv)
                        elif sv.find("global") == 4 and sv.find("return") == -1 and ft != 1 and ft != 0 and ft != 2:
                            res = {}
                            try:
                                res = {}
                                exec("from " + imported + " import " + sv.replace("global ", "").replace(" ", "", sv.replace("global ", "").count(" ")) + "result = " + sv.replace("global ", "").replace(" ", "", sv.replace("global ", "").count(" ")), globals(), res)
                                func_contentl.append(sv.replace("global ", "").replace("\n", "") + " = " + str(res["result"]) + "\n")
                            except Exception as e:
                                res["result"] = sv
                                func_contentl.append(sv.replace("\n", "") + " = " + str(res["result"]) + "\n")
                        elif sv.find("return") == -1 and ft == 2 and ft != 1 and ft != 0 and not sv.find("global") == 4:
                            rep = sv.split()
                            rept = 0
                            for sf in rep:
                                if rept == 1:
                                    func_name = sf.replace(":", "")
                                    rept = rept + 1
                            func_contentl.append(sv)
                        elif sv.find("return") != -1 and ft != 0 and ft != 1 and ft != 2 and not sv.find("global") == 4:
                            func_contentl.append(sv.replace("\n", "").replace("return ", "end(") + ")")
                        ft = ft + 1
                global import_list
                func_contentl.insert(0, 'def end(mess):\n\tprint("raspberrypi_code.raspberrypi.package.python.glt.org.py return " + str(mess))\n' + import_list + "\n" + "".join(function_to_add))
                func_contentl.append("\n" + func_name)
                func_content = "".join(func_contentl)
                file_name = "raspberrypi_code.raspberrypi.package.python.glt.org.py"
                buf = StringIO(func_content)
                ssh_controller.putfo(buf, file_name)
                exit_code, output = ssh_controller.run(command="python " + file_name, display=True, capture=True)
                ssh_controller.remove(file_name)
                re = "raspberrypi_code.raspberrypi.package.python.glt.org.py return "
                if output[-1].find(re) != -1:
                    return output[-1].replace(re, "")
                else:
                    return None
                ssh_controller.disconnect()
            except Exception as f:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def raspberry_command_add():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            global function_to_add
            func_data = inspect.getsource(func)
            func_data = func_data.splitlines(True)
            func_datal = list()
            em = list()
            ct = 0
            for g in func_data:
                if not ct == 0:
                    em.append(g)
                ct += 1
            ft = 0
            for sv in func_data:
                if sv.find("return") == -1 and ft != 1 and ft != 0 and not sv.find("global") == 4:
                    func_datal.append(sv)
                elif sv.find("global") == 4 and sv.find("return") == -1 and ft != 1 and ft != 0:
                    res = {}
                    try:
                        res = {}
                        exec("from " + imported + " import " + sv.replace("global ", "").replace(" ", "", sv.replace("global ", "").count(" ")) + "result = " + sv.replace("global ", "").replace(" ", "", sv.replace("global ", "").count(" ")), globals(), res)
                        func_datal.append(sv.replace("global ", "").replace("\n", "") + " = " + str(res["result"]) + "\n")
                    except Exception as e:
                        res["result"] = sv
                        func_datal.append(sv.replace("\n", "") + " = " + str(res["result"]) + "\n")
                elif sv.find("return") == -1 and ft == 1 and ft != 0 and not sv.find("global") == 4:
                    rep = sv.split()
                    rept = 0
                    for sf in rep:
                        if rept == 1:
                            func_name = sf.replace(":", "")
                        rept = rept + 1
                    func_datal.append(sv)
                elif sv.find("return") != -1 and ft != 0 and ft != 1 and not sv.find("global") == 4:
                    func_datal.append(sv.replace("\n", "").replace("return ", "end(") + ")")
                ft = ft + 1
            function_to_add.append("".join(function_to_add))
            return True
        return wrapper
    return decorator

def config(file_name):
    if file_name[-3:-1] == ".py":
        file_name = file_name[0:-4]
    file_name = file_name.replace(".", "-", str(file_name).count("."))
    global imported
    imported = file_name
    global import_list
    import_list_finish = list()
    file = open(file_name + ".py", "r").read().splitlines()
    for imp in file:
        if imp.find("import ") != -1 and imp.find("import raspberrypi") == -1 and imp.replace("import ", "") != "" and imp.replace("import ", "") != " ":
            imp = imp.split(" ")
            imp = imp[1]
            import_list.append(imp)
    for item in import_list:
        if not item == "" and not item == " ":
            item_res = ["'pip install " + item + "'", "import " + item, "try:\n\timport " + item + "\nexcept:\n\timport os\n\t" + "os.system('pip install " + item + "')\n\timport " + item]
            import_list_finish.append(item_res)
    import_list_end = list()
    for thing in import_list_finish:
        import_list_end.append(thing[2])
    import_list = "\n".join(import_list_end)

class raspberrypi:
    global raspberrypi_prep_timeout

    @timeout(raspberrypi_prep_timeout, default=False)
    def check(self, hoip):
        global raspberrypi_info
        HOST_IP = hoip
        SSH_PWD = raspberrypi_info[1]
        ssh_controller = ssh.SSHController(host=HOST_IP, user=raspberrypi_info[0], ssh_password=SSH_PWD)
        ssh_controller.connect()
        try:
            ssh_controller.run(command="ls")
            return True
        except:
            return False

    def set_preparation(self, ip, max_loop, timeout_time):
        global raspberrypi_prep
        global raspberrypi_prep_max
        global raspberrypi_prep_timeout
        raspberrypi_prep = ip
        raspberrypi_prep_max = max_loop
        raspberrypi_prep_timeout = timeout_time

    def ipChecker(self,ip):
        return ip.replace('.', '',ip.count(".")).isdigit()
    def local(self, start_ip=None):
        global raspberrypi_ip
        global raspberrypi_prep_max
        global raspberrypi_prep
        if not self.ipChecker(raspberrypi_prep):
            if raspberrypi().check(raspberrypi_prep):
                raspberrypi_ip = raspberrypi_prep
            return raspberrypi_prep
        start_ip = raspberrypi_prep
        if raspberrypi_ip == 0 and raspberrypi_prep == start_ip:
            gh = 0
            gj = []
            while True:
                gj.append(start_ip + str(gh))
                gh = gh + 1
                if gh == int(raspberrypi_prep_max):
                    break
            for host in gj:
                hoip = host
                if raspberrypi().check(hoip):
                    raspberrypi_ip = hoip
                    break
                else:
                    continue
        res = raspberrypi_ip
        if res != 0:
            return res
        else:
            raise IOError("password or username are not good or raspberry is on your local internet")

    def set_raspberry_info(self, user_name, password):
        global raspberrypi_info
        raspberrypi_info = list()
        raspberrypi_info.append(user_name)
        raspberrypi_info.append(password)

def run_command(command=None, display=False):
    if command is not None:
        global raspberrypi_prep
        global raspberrypi_info
        SSH_PWD = "geoloup"
        HOST_IP = raspberrypi().local(raspberrypi_prep)
        ssh_controller = ssh.SSHController(host=HOST_IP, user=raspberrypi_info[0], ssh_password=raspberrypi_info[1])
        try:
            ssh_controller.connect()
            exit_code, output = ssh_controller.run(command=command, display=display, capture=True)
            ssh_controller.disconnect()
            return output[-1]
        except Exception:
            import os
            return os.system(command)
    else:
        raise ValueError("You need to have a command... At run_command")

class file:
    file_content = None

    def __init__(self, name):
        global raspberrypi_prep
        global raspberrypi_info
        SSH_PWD = "geoloup"
        HOST_IP = raspberrypi().local(raspberrypi_prep)
        ssh_controller = ssh.SSHController(host=HOST_IP, user=raspberrypi_info[0], ssh_password=raspberrypi_info[1])
        ssh_controller.connect()
        buffer = StringIO("")
        content = ssh_controller.getfo(name, buffer)
        buffer.seek(0)
        buffer.write(buffer.read()[2:-2])
        buffer.seek(0)
        self.file_content = buffer
        ssh_controller.disconnect()

    def get(self):
        self.file_content.seek(0)
        return self.file_content

    def update(self, new_buffer):
        self.file_content.seek(0)
        self.file_content = new_buffer
        file.file_content = self.file_content
        return new_buffer

    def download(self, result_file):
        self.file_content.seek(0)
        with open(result_file, "w") as f:
            f.write(self.file_content.read())
        with open(result_file, "r") as f:
            return f.read()

class runner:
    def __init__(self, code):
        self.code = code
        self.P = None

    def run(self):
        P = subprocess.Popen(self.code, shell=True)
        self.current = psutil.Process(pid=P.pid)
        self.P = P

    def pause(self):
        self.current.suspend()

    def unpause(self):
        self.current.resume()

    def stop(self):
        self.current.terminate()

    def restart(self, code=None):
        if code is None:
            self.stop()
            self.run()
        else:
            self.stop()
            self.code = code
            self.run()
