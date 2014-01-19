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

    read_size: The number of read bytes till the error occured.
    err: The original exception
    """

    def __init__(self, read_size, err=None):
        self.read_size = read_size
        self.err = err
        return None

    def __str__(self):
        tmp = "TS3 file download failed. "
        if self.err is not None:
            tmp += str(self.err)
        return tmp
    

# Classes
# ------------------------------------------------
class TS3FileTransfer(object):
    """
    High-Level ts3 file transfer handler.
    """

    # Counter for the client file transfer ids.
    _FTID = int(time.time()*100)
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

    # Download
    # --------------------------------------------

    def init_download(self, output_file,
                      name, cid, cpw=None, seekpos=0,
                      query_resp_hook=None, reporthook=None):
        """
        This is the recommended method to download a file from a TS3 server.        
        
        *name*, *cid*, *cpw* and *seekpos* are the parameters for the TS3
        query command *ftinitdownload*. The parameter *clientftid* is
        automatically created and unique for the whole runtime of the programm.

        *query_resp_hook*, if provided, is called, when the response of the
        ftinitdownload query has been received. Its single parameter is the 
        the response of the querry.

        For downloading the file from the server, **TS3FileTransfer.download()*
        is called. So take a look a this method for further information.
        """
        if cpw is None:
            cpw = str()
            
        ftid = self.get_ftid()
        resp = self.ts3conn.ftinitdownload(
            ftid, name, cid, cpw, seekpos)
        
        if query_resp_hook is not None:
            query_resp_hook(resp)

        return self.download_by_resp(output_file, resp, seekpos, reporthook)

    @classmethod
    def download_by_resp(cls, output_file, ftinitdownload_resp,
                         seekpos=0, reporthook=None):
        """
        This is *almost* a shortcut for:
            >>> TS3FileTransfer.download(
                    output_file,
                    adr = (resp[0]["ip"], int(resp[0]["port"])),
                    ftkey = resp[0]["ftkey"],
                    seekpos = seekpos,
                    total_size = resp[0]["size"],
                    reporthook = reporthook
                    )
            ...
        Note, that the value of resp[0]["ip"] is a csv list a has to be parsed.
        """
        # The csv ip list is not parsed by the TS3ResponseParser, so we have
        # to parse the list here.
        ip_list = ftinitdownload_resp[0]["ip"]
        ip_list = ip_list.split(",")
        # Use the first ip in the list and make sure, that the ip is defined.
        ip = ip_list[0] if ip_list[0] != "0.0.0.0" else "localhost"
        
        port = int(ftinitdownload_resp[0]["port"])
        adr = (ip, port)
        
        ftkey = ftinitdownload_resp[0]["ftkey"]
        total_size = ftinitdownload_resp[0]["size"]
        return cls.download(output_file, adr, ftkey, seekpos, total_size, reporthook)

    @classmethod
    def download(cls, output_file, adr, ftkey,
                 seekpos=0, total_size=0, reporthook=None):
        """
        Downloads a file from a TS3 server in the file *output_file*. The
        TS3 file transfer interface is specified witht the address tuple *adr*
        and the download with the file transfer key *ftkey*.

        If *seekpos* and the total *size* are provided, the *reporthook*
        function (lambda read_size, block_size, total_size: None) is called
        after receiving a new block.

        If you provide *seekpos* and *total_size*, this method will check, if
        the download is complete and raise a *TS3FtDownloadError* if not.

        Note, that if *total_size* is 0 or less, each download will be considered
        as complete.

        If no error is raised, **read_size is returned**.
        """
        # Convert the ftkey if necessairy
        if isinstance(ftkey, str):
            ftkey = ftkey.encode()
        if seekpos < 0:
            raise ValueError("Seekpos has to be >= 0!")
            
        read_size = seekpos
        block_size = 4096
        try:
            with socket.create_connection(adr) as sock:
                sock.sendall(ftkey)

                # Begin with the download.
                if reporthook is not None:
                    reporthook(read_size, block_size, total_size)

                while True:
                    data = sock.recv(block_size)
                    output_file.write(data)
                    
                    read_size += len(data)
                    if reporthook is not None:
                        reporthook(read_size, block_size, total_size)

                    # Break, if the connection has been closed.
                    if not data:
                        break
                    
        # Catch all socket errors.
        except OSError as err:
            raise TS3FtDownloadError(read_size, err)

        # Raise an error, if the download is not complete.
        if read_size < total_size:
            raise TS3FtDownloadError(read_size)
        return read_size

    # Upload
    # --------------------------------------------


