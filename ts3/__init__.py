#!/usr/bin/python3


# Data
# ------------------------------------------------
__version__ = "0.0.10"


# Modules
# ------------------------------------------------
try:
    from commands import TS3Commands
    from common import TS3RegEx
    from escape import TS3Escape
    from filetransfer import TS3FileTransfer
    from query import TS3BaseConnection, TS3Connection
    from response import TS3Response

except ImportError:
    from .commands import TS3Commands
    from .common import TS3RegEx
    from .escape import TS3Escape
    from .filetransfer import TS3FileTransfer
    from .query import TS3BaseConnection, TS3Connection
    from .response import TS3Response

    
# Main
# ------------------------------------------------
if __name__ == "__main__":
    # Only for development.
    from pprint import pprint

    # Using a local testserver.
    with TS3Connection("localhost") as ts3conn:
        ts3conn.login("serveradmin", "1U0FkWci")
        pprint(ts3conn.last_resp.error)
        
        ts3conn.use(1)
        pprint(ts3conn.last_resp.error)
        
        pprint(ts3conn.last_resp.parsed)
        pprint(ts3conn.last_resp.error)

