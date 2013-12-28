#!/usr/bin/python3


__version__ = "0.1.0"


try:
    import query
    import filetransfer
    import protocoll

    # For convenience
    from definitions import *

except ImportError:
    from . import query
    from . import filetransfer
    from . import protocoll
    from .definitions import *
