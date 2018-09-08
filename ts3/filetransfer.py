#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2013-2018 <see AUTHORS.txt>
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

"""
:mod:`ts3.filetransfer`
=======================

This module contains an API for the TS3 file transfer interface.
"""

# std
import socket
import time
import threading

# local
from .common import TS3Error


__all__ = [
    "TS3FileTransferError",
    "TS3UploadError",
    "TS3DownloadError",
    "TS3FileTransfer"]


class TS3FileTransferError(TS3Error):
    """
    This is the base class for all exceptions in this module.
    """


class TS3UploadError(TS3FileTransferError):
    """
    Is raised, when an upload fails.
    """

    def __init__(self, send_size, err=None):
        #: The number of sent bytes till the error occured.
        self.send_size = send_size

        #: A string describing the condition which caused the exception more
        #: precise.
        self.err = err
        return None

    def __str__(self):
        tmp = "TS3 file upload failed. "
        if self.err is not None:
            tmp += str(self.err)
        return tmp


class TS3DownloadError(TS3FileTransferError):
    """
    Is raised, when a download fails.
    """

    def __init__(self, read_size, err=None):
        #: The number of read bytes untill the error occured.
        self.read_size = read_size

        #: A string describing the condition which caused the exception more
        #: precise.
        self.err = err
        return None

    def __str__(self):
        tmp = "TS3 file download failed. "
        if self.err is not None:
            tmp += str(self.err)
        return tmp


class TS3FileTransfer(object):
    """
    A high-level TS3 file transfer handler.

    The recommended methods to download or upload a file are:

        * :meth:`init_download`
        * :meth:`init_upload`

    You can either use the low-level class methods,
    e.g. :meth:`download_by_resp` or the high-level ones like
    :meth:`init_download` to handle the file transfers::

        ts3ft = TS3FileTransfer(ts3conn)
		with open("baz.png", "rb") as file:
			ts3ft.init_upload(input_file=file, name="/baz.png", cid=2)
		with open("baz1.png", "wb") as file:
			ts3ft.init_download(output_file=file, name="/baz.png", cid=2)

    File transports can be monitored using a *reporthook*, a function which
    is periodically called with the current transfer stats::

        def reporthook(size, block_size, total_size):
            print("{}% done.".format(size/total_size))
    """

    # Counter for the client file transfer ids.
    _FTID = 0
    _FTID_LOCK = threading.Lock()

    def __init__(self, ts3conn):
        """
        Creates a new TS3FileTransfer object, that is associated with
        the TS3Connection ts3conn. This means, that calls of
        :meth:`init_download` and :meth:`init_upload` will use this
        connection to authenticate the file transfer.
        """
        self.ts3conn = ts3conn
        return None

    # Common stuff
    # --------------------------------------------

    @classmethod
    def get_ftid(cls):
        """
        :return:
            Returns a unique id for a file transfer.
        :rtype:
            int
        """
        with cls._FTID_LOCK:
            tmp = cls._FTID
            cls._FTID += 1
        return tmp

    @classmethod
    def _ip_from_resp(self, ip_val):
        """
        The value of the ip key in a TS3QueryResponse is a comma separated
        list of ips and this method parses the list and returns the first ip.

        >>> ts3ft._ip_from_resp('0.0.0.0,91.1.2.3')
        'localhost'
        >>> ts3ft._ip_from_resp('91.1.2.3,')
        '91.1.2.3'
        """
        ip_val = ip_val.split(",")
        ip = ip_val[0]
        if ip == "0.0.0.0":
            ip = "localhost"
        return ip

    # Download
    # --------------------------------------------

    def init_download(self, output_file,
                      name, cid, cpw="", seekpos=0,
                      query_resp_hook=None, reporthook=None):
        """
        This is the recommended method to download a file from a TS3 server.

        **name**, **cid**, **cpw** and **seekpos** are the parameters for the
        TS3 query command **ftinitdownload**. The parameter **clientftid** is
        automatically created and unique for the whole runtime of the programm.

        **query_resp_hook**, if provided, is called, when the response of the
        ftinitdownload query has been received. Its single parameter is the
        the response of the query.

        For downloading the file from the server, :meth:`download()` is called.
        So take a look a this method for further information.

        :seealso: The TS3 *ftinitdownload* command
        """
        resp = self.ts3conn.query("ftinitdownload",
            clientftfid=self.get_ftid(),
            name=name,
            cid=cid,
            cpw=cpw,
            seekpos=seekpos
        ).fetch()

        if query_resp_hook is not None:
            query_resp_hook(resp)
        return self.download_by_resp(
            output_file=output_file, ftinitdownload_resp=resp,
            seekpos=seekpos, reporthook=reporthook,
            fallbackhost=self.ts3conn.host)

    @classmethod
    def download_by_resp(cls, output_file, ftinitdownload_resp,
                         seekpos=0, reporthook=None, fallbackhost=None):
        """
        Kicks off a file download by using a query response to a
        *ftinitdownload* command.

        This is *almost* a shortcut for:

            >>> TS3FileTransfer.download(
            ...     output_file = file,
            ...     adr = (resp[0]["ip"], int(resp[0]["port"])),
            ...     ftkey = resp[0]["ftkey"],
            ...     seekpos = seekpos,
            ...     total_size = resp[0]["size"],
            ...     reporthook = reporthook
            ...     )

        Note, that the value of ``resp[0]["ip"]`` is a csv list and needs
        to be parsed.

        :seealso: :meth:`download`
        """
        if "ip" in ftinitdownload_resp[0]:
            ip = cls._ip_from_resp(ftinitdownload_resp[0]["ip"])
        elif fallbackhost:
            ip = fallbackhost
        else:
            raise TS3DownloadError(0, "The response did not contain an ip.")

        port = int(ftinitdownload_resp[0]["port"])
        adr = (ip, port)

        ftkey = ftinitdownload_resp[0]["ftkey"]
        total_size = int(ftinitdownload_resp[0]["size"])
        return cls.download(
            output_file=output_file, adr=adr, ftkey=ftkey, seekpos=seekpos,
            total_size=total_size, reporthook=reporthook)

    @classmethod
    def download(cls, output_file, adr, ftkey,
                 seekpos=0, total_size=0, reporthook=None):
        """
        Downloads a file from a TS3 server in the file **output_file**. The
        TS3 file transfer interface is specified with the address tuple **adr**
        and the download with the file transfer key **ftkey**.

        If **seekpos** and the total **size** are provided, the **reporthook**
        function (``lambda read_size, block_size, total_size: None``) is called
        each time a new data block has been received.

        If you provide **seekpos** and **total_size**, this method will check,
        if the download is complete and raise a :exc:`TS3DownloadError` if not.

        Note, that if **total_size** is 0 or less, each download will be
        considered as complete.

        If no error is raised, the number of read bytes is returned.

        :return:
            The number of received bytes.
        :rtype:
            int

        :raises TS3DownloadError:
            If the download is incomplete or a socket error occured.
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
            raise TS3DownloadError(read_size) from err

        # Raise an error, if the download is not complete.
        if read_size < total_size:
            raise TS3DownloadError(read_size, "The download is incomplete.")
        return read_size

    # Upload
    # --------------------------------------------

    def init_upload(self, input_file,
                    name, cid, cpw="", overwrite=True, resume=False,
                    query_resp_hook=None, reporthook=None):
        """
        This is the recommended method to upload a file to a TS3 server.

        **name**, **cid**, **cpw**, **overwrite** and **resume** are the
        parameters for the TS3 query command **ftinitdownload**.
        The parameter **clientftid** is automatically created and unique for
        the whole runtime of the programm and the value of **size** is
        retrieved by the size of the **input_file**.

        **query_resp_hook**, if provided, is called, when the response of the
        ftinitupload query has been received. Its single parameter is the
        the response of the query.

        For uploading the file to the server :meth:`upload` is called. So
        take a look at this method for further information.

        :seealso: The TS3 *ftinitdownload* command
        """
        input_file.seek(0, 2)
        size = input_file.tell()

        resp = self.ts3conn.query("ftinitupload",
            clientftfid=self.get_ftid(),
            name=name,
            cid=cid,
            cpw=cpw,
            size=size,
            overwrite="1" if overwrite else "0",
            resume="1" if resume else "0"
        ).fetch()

        if query_resp_hook is not None:
            query_resp_hook(resp)
        return self.upload_by_resp(
            input_file=input_file, ftinitupload_resp=resp,
            reporthook=reporthook, fallbackhost=self.ts3conn.host)

    @classmethod
    def upload_by_resp(cls, input_file, ftinitupload_resp,
                       reporthook=None, fallbackhost=None):
        """
        This is *almost* a shortcut for:

            >>> TS3FileTransfer.upload(
            ...     input_file = file,
            ...     adr = (resp[0]["ip"], int(resp[0]["port"])),
            ...     ftkey = resp[0]["ftkey"],
            ...     seekpos = resp[0]["seekpos"],
            ...     reporthook = reporthook
            ...    )

        Note, that the value of ``resp[0]["ip"]`` is a csv list and needs
        to be parsed.

        :seealso: :meth:`upload`
        """
        if "ip" in ftinitupload_resp[0]:
            ip = cls._ip_from_resp(ftinitupload_resp[0]["ip"])
        elif fallbackhost:
            ip = fallbackhost
        else:
            raise TS3UploadError(0, "The response did not contain an ip.")

        port = int(ftinitupload_resp[0]["port"])
        adr = (ip, port)

        ftkey = ftinitupload_resp[0]["ftkey"]
        seekpos = int(ftinitupload_resp[0]["seekpos"])
        return cls.upload(
            input_file=input_file, adr=adr, ftkey=ftkey, seekpos=seekpos,
            reporthook=reporthook)

    @classmethod
    def upload(cls, input_file, adr, ftkey, seekpos=0, reporthook=None):
        """
        Uploads the data in the file **input_file** to the TS3 server listening
        at the address **adr**. **ftkey** is used to authenticate the file
        transfer.

        When the upload begins, the *get pointer* of the **input_file** is set
        to seekpos.

        If the **reporthook** function
        (``lambda send_size, block_size, total_size``) is provided, it is called
        each time a data block has been successfully transfered.

        :raises TS3UploadError:
            If the upload is incomplete or a socket error occured.
        """
        if isinstance(ftkey, str):
            ftkey = ftkey.encode()

        # Get the total size of the file and put the get pointer to the correct
        # position.
        input_file.seek(0, 2)
        total_size = input_file.tell()
        input_file.seek(seekpos)

        send_size = seekpos
        block_size = 4096
        try:
            with socket.create_connection(adr) as sock:
                sock.sendall(ftkey)

                # Begin with the upload
                if reporthook is not None:
                    reporthook(send_size, block_size, total_size)

                while True:
                    data = input_file.read(block_size)
                    sock.sendall(data)

                    send_size += len(data)
                    if reporthook is not None:
                        reporthook(send_size, block_size, total_size)

                    if not data:
                        break
        except OSError:
            raise TS3FtUploadError(send_size) from err

        # Raise an error, if the upload is not complete.
        if send_size < total_size:
            raise TS3FtUploadError(send_size, "The upload is incomplete.")
        return send_size
