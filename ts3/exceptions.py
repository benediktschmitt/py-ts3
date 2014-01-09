#!/usr/bin/python3


"""
All package dependant exceptions.

Note:
    This classes of this module could moved in other modules in future
    versions.
"""


# Data
# ------------------------------------------------
__all__ = ["TS3Error",
           "TS3QueryError"
           ]


# Exceptions
# ------------------------------------------------
class TS3Error(Exception):
    """
    Base class for all exceptions.
    """


class TS3QueryError(Exception):
    """
    Raised, if the error code of the response was not 0.
    """

    def __init__(self, error_id, error_msg):
        self.id = error_id
        self.msg = error_msg
        return None

    def __str__(self):
        tmp = "Error ID {}: {}".format(self.id, self.msg)
        return tmp
