#!/usr/bin/env python3

import os
import ctypes
import ctypes.util
import struct
from contextlib import suppress
from collections import namedtuple

from .constants import *

# syscall interface

inotify_event_struct = struct.Struct("@iIII")


libc_path = ctypes.util.find_library('c') or 'libc.so.6'
libc_instance = ctypes.CDLL(libc_path, use_errno = True)

def check_result(result):
	if result < 0:
		errno = ctypes.get_errno()
		err_str = ""
		with suppress(ValueError):
			err_str = os.strerror(errno)

		raise OSError(errno, err_str)
	return result

inotify_init1 = libc_instance.inotify_init1
inotify_init1.argtypes = [ctypes.c_int]
inotify_init1.restype = check_result

inotify_add_watch = libc_instance.inotify_add_watch
inotify_add_watch.argtypes = [
	ctypes.c_int,
	ctypes.c_char_p,
	ctypes.c_uint32]

inotify_add_watch.restype = check_result

inotify_rm_watch = libc_instance.inotify_rm_watch
inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]
inotify_rm_watch.restype = check_result

inotify_event = namedtuple("inotify_event", ("wd", "mask", "cookie", "len", "name"))

def parse_event(data):
	parsed_info = inotify_event_struct.unpack_from(data)
	name_len = parsed_info[3]
	offset = inotify_event_struct.size + name_len
	name = data[inotify_event_struct.size:offset]
	with suppress(UnicodeError):
		name = name.rstrip(b'\x00').decode()

	event = inotify_event(*parsed_info, name)

	return event, data[offset:]


class Inotify:
	def __init__(self, flags = 0):
		self.fd = inotify_init1(flags)
		self.watches = {}

	def close(self):
		if self.fd is not None:
			with suppress(OSError):
				os.close(self.fd)
			self.fd = None

	def __del__(self):
		self.close()

	def fileno(self):
		return self.fd

	def add_watch(self, path, /, mask = IN_ALL_EVENTS):
		wd = inotify_add_watch(self.fd, path.encode(), mask)
		self.watches[wd] = os.path.normpath(path)
		return wd

	def rm_watch(self, wd):
		self.watches.pop(wd, None)
		inotify_rm_watch(self.fd, wd)

	def get(self, wd):
		return self.watches.get(wd)

	def read(self):
		data = None
		with suppress(BlockingIOError):
			data = os.read(self.fd, 0x1000)
		result = []
		while data:
			event, data = parse_event(data)
			result.append(event)

		return result


