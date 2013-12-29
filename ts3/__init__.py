#!/usr/bin/python3


__version__ = "0.1.0"


try:
    import query
    import filetransfer

    # For convenience
    from definitions import *

except ImportError:
    from . import query
    from . import filetransfer

    from .definitions import *
