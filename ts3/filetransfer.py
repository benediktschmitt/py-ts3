#!/usr/bin/python3

# The MIT License (MIT)
# 
# Copyright (c) 2013 Benedikt Schmitt
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Modules
# ------------------------------------------------
import socket
import select
import time
import threading

# local
try:
    from common import TS3Error
except ImportError:
    from .common import TS3Error
    

# Data
# ------------------------------------------------
__all__ = ["TS3FileTransfer"]


# Exceptions
# ------------------------------------------------
class TS3FileTransferError(TS3Error):
    """
    Base class for all exceptions in this module.
    """


class TS3FtUploadError(TS3FileTransferError):
    """
    Raised when an upload fails.
    """
    

class TS3FtDownloadError(TS3FileTransferError):
    """
    Raised, when a download fails.

    resp: The TS3QueryResponse used to init the download.
    read_size: The number of read bytes till the error occured.
    err: The original exception
    """

    def __init__(self, resp, read_size, err=None):
        self.resp = resp
        self.read_size = read_size
        self.err = err
        return None

    def __str__(self):
        tmp = "Download of clientftid={} failed."\
              .format(self.resp[0]["clientftfid"]) 
        return tmp
    

# Classes
# ------------------------------------------------
class TS3FileTransfer(object):
    """
    High-Level ts3 file transfer handler.
    """

    # Counter for the client file transfer ids.
    _FTID = int(time.time())
    _FTID_LOCK = threading.Lock()

    def __init__(self, ts3conn):
        self.ts3conn = ts3conn
        return None

    @classmethod
    def get_ftid(cls):
        """
        Returns a unique id for the file transfer.
        """
        with cls._FTID_LOCK:
            tmp = cls._FTID
            cls._FTID += 1
        return tmp

    def init_download(self, output_file, name, cid, cpw=None, seekpos=0,
                      query_resp_hook=None, reporthook=None):
        """
        This is method is a shortcut for:
        >>> resp = ts3conn.ftinitdownload(
            TS3FileTransfer.get_ftid(), name, cid, cpw, seekpos)
        >>> ts3ft.download(resp, output_file, reporthook)
        
        *name*, *cid*, *cpw* and *seekpos* are the parameters for the TS3
        query command ftinitdownload.
        
        *query_resp_hook*, if provided, is called, when the response of the
        ftinitdownload query has been received. It has as single parameter
        the response of the querry.

        For further information take a look at: *TS3FileTransfer.download()*.
        """
        if cpw is None:
            cpw = ""

        ftid = self.get_ftid()
        resp = self.ts3conn.ftinitdownload(
            ftid, name, cid, cpw, seekpos)

        if query_resp_hook is not None:
            query_resp_hook(resp)

        return self.download(output_file, resp, seekpos, reporthook=reporthook)

    @classmethod
    def download(cls, output_file, ftinitdownload_resp,
                 seekpos=0, reporthook=None):
        """
        The received data is directly written into the *output_file*.
        
        *ftinitdownload* is a TS3QueryResponse object that contains the
        response of a ftinitdownload query.
        
        *reporthook* is a function, which accepts three paramters:
        *read_size*, *block_size*, *total_size* and is called whenever a new
        data block has been received.
        
        >>> hook = lambda read_size, block_size, total_size: \
                print("{} of {} bytes received.".format(read_size, total_size)

        *seekpos* must be provided, when you use the seekpos parameter in the
        query. If you use this parameter and don't provide it here, a
        *TS3FtDownloadError* will be raised, because the download will be
        considered as incomplete.
        
        If the download fails, a *TS3FtDownloadError* is raised. The error
        object contains the downloaded size. So that you can use *seekpos*
        to resume the download at this position.
        """
        # Convert some types
        meta = ftinitdownload_resp[0]        
        meta["port"] = int(meta["port"])
        meta["size"] = int(meta["size"])
        
        # Multiple ips are not parsed correct, so we parse them here.
        meta["ip"] = meta["ip"].split(",")
        meta["ip"] = meta["ip"][0]
        if meta["ip"] == "0.0.0.0":
            meta["ip"] = "localhost"

        # Start downloading the file.
        read_size = seekpos
        block_size = 4096
        try:
            with socket.create_connection((meta["ip"], meta["port"])) as sock:
                sock.sendall(meta["ftkey"].encode())

                while True:
                    rs, ws, xs = select.select([], [sock], [])
                    data = sock.recv(block_size)
                    output_file.write(data)
                    
                    read_size += len(data)
                    if reporthook is not None:
                        reporthook(read_size, block_size, meta["size"])

                    # Break, if the connection has been closed.
                    if not data:
                        break
        # Catch all socket errors.
        except OSError as err:
            raise TS3FtDownloadError(ftinitdownload_resp, read_size, err)

        # Raise an error, if the download is not complete.
        if read_size < meta["size"]:
            raise TS3FtDownloadError(ftinitdownload_resp, read_size)
        return None

    def init_upload(self, input_file, name, cid, cpw=None,
                    overwrite=True, resumse=False, reporthook=None):
        """
        """

    @classmethod
    def upload(cls, input_file, ftinitupload_resp, reporthook=None):
        """
        Uploads the data in *input_file* to the ts3server using the
        *ftinitupload_resp* to connect to the server and authenticate the
        file transfer.
        """
        pass
