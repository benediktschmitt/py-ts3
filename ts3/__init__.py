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
__version__ = "0.1.5"


# Modules
# ------------------------------------------------
try:
    from commands import TS3Commands
    from common import TS3RegEx
    from escape import TS3Escape
    from exceptions import TS3Error, TS3QueryError
    from filetransfer import TS3FileTransfer
    from query import TS3BaseConnection, TS3Connection
    from response import TS3Response

    # For convenience
    import definitions as defs

except ImportError:
    from .commands import TS3Commands
    from .common import TS3RegEx
    from .escape import TS3Escape
    from .exceptions import TS3Error, TS3QueryError
    from .filetransfer import TS3FileTransfer
    from .query import TS3BaseConnection, TS3Connection
    from .response import TS3Response

    from . import definitions as defs

    
# Main
# ------------------------------------------------
if __name__ == "__main__":
    # Only for development.
    from pprint import pprint

    # Using a local testserver.
    with TS3Connection("localhost") as ts3conn:
        ts3conn.login("serveradmin", "xh4ie1HL")        
        ts3conn.use(1)

        ts3conn.send_raw("blabla\n\r")

