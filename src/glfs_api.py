#!/usr/bin/python

# Copyright 2011-2017 Red Hat, Inc. and/or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import ctypes
import os

CHUNK_SIZE = 10 * 1024 * 1024  # 10MB


class GlfsApi:
    GLUSTER_DEFAULT_PORT = 24007
    # C function prototypes for using the library gfapi
    _lib = ctypes.CDLL("libgfapi.so.0", use_errno=True)

    _glfs_new = ctypes.CFUNCTYPE(
        ctypes.c_void_p, ctypes.c_char_p)(('glfs_new', _lib))

    _glfs_set_volfile_server = ctypes.CFUNCTYPE(
        ctypes.c_int,
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_int)(('glfs_set_volfile_server', _lib))

    _glfs_init = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_void_p)(('glfs_init', _lib))

    _glfs_creat = ctypes.CFUNCTYPE(
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_uint)(('glfs_creat', _lib))

    _glfs_ftruncate = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_void_p, ctypes.c_int)(('glfs_ftruncate', _lib))

    _glfs_write = ctypes.CFUNCTYPE(
        ctypes.c_ssize_t,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_int)(('glfs_write', _lib))

    _glfs_close = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_void_p)(('glfs_close', _lib))

    _glfs_fini = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_void_p)(('glfs_fini', _lib))

    def __init__(self, address, path):
        # New libgfapi expects volume name without prefix
        if path.startswith("/"):
            path = path[1:]
        fs = self._glfs_new(path)
        ret = self._glfs_set_volfile_server(fs, "tcp",
                                            address, self.GLUSTER_DEFAULT_PORT)
        if ret == -1:
            err = ctypes.get_errno()
            raise IOError(
                "glfs_set_volfile_server failed: %s" % os.strerror(err))

        ret = self._glfs_init(fs)
        if ret == -1:
            err = ctypes.get_errno()
            raise IOError(
                "glfs_init failed: %s" % os.strerror(err))
        self.fs = fs

    def umount(self):
        ret = self._glfs_fini(self.fs)
        if ret == -1:
            err = ctypes.get_errno()
            raise IOError(
                "glfs_fini failed: %s" % os.strerror(err))

    def upload(self, local, remote):
        remote_fd = self._glfs_creat(self.fs, remote, os.O_RDWR, 0644)
        if remote_fd is None:
            err = ctypes.get_errno()
            raise IOError(
                "Failed to create %s: %s" % (remote, os.strerror(err)))

        ret = self._glfs_ftruncate(remote_fd, 0)
        if ret == -1:
            err = ctypes.get_errno()
            raise IOError(
                "Failed to truncate %s: %s" % (remote, os.strerror(err)))

        with open(local, "r") as local_fd:
            while True:
                chunk = local_fd.read(CHUNK_SIZE)
                if not chunk:
                    break
                ret = self._glfs_write(remote_fd, chunk, len(chunk), 0)
                if ret == -1:
                    err = ctypes.get_errno()
                    raise IOError(
                        "Write failed%s" % os.strerror(err))

        self._glfs_close(remote_fd)
