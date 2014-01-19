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


# Data
# ------------------------------------------------
__version__ = "0.2.1"


# Modules
# ------------------------------------------------
try:
    from common import TS3Error
    from escape import TS3Escape
    from filetransfer import (TS3FileTransferError, TS3FtUploadError,
                              TS3FtDownloadError, TS3FileTransfer)
    from query import (TS3QueryError, TS3ResponseRecvError,
                       TS3BaseConnection, TS3Connection)
    from response import (TS3Response, TS3ParserError,
                          TS3QueryResponse, TS3Event)

    # For convenience
    from definitions import *
except ImportError:
    from .common import TS3Error
    from .escape import TS3Escape
    from .filetransfer import (TS3FileTransferError, TS3FtUploadError,
                               TS3FtDownloadError, TS3FileTransfer)
    from .query import (TS3QueryError, TS3ResponseRecvError,
                        TS3BaseConnection, TS3Connection)
    from .response import (TS3Response, TS3ParserError,
                           TS3QueryResponse, TS3Event)

    # For convenience
    from .definitions import *
    
    
# Main
# ------------------------------------------------
if __name__ == "__main__":
    # Only for development
    from pprint import pprint
    import time
    import sys
    import logging
    import socket

    # Set the logger up to print all debug messages.
    logger = logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout)

    # Using a local testserver.
    ts3conn = TS3Connection("localhost")
    ts3conn.login("serveradmin", "xh4ie1HL")        
    ts3conn.use(1)
