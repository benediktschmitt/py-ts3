#!/usr/bin/python3


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

