#!/usr/bin/python3


"""
This module contains some little helper classes and functions.
"""


# Modules
# ------------------------------------------------
import re


# Data
# ------------------------------------------------
__all__ = ["TS3RegEx"]


# Classes
# ------------------------------------------------
class TS3RegEx(object):
    """
    Frequently used and important regular expressions.
    """

    # XXX: The telnet interface does not accept compiled regex ...
    LINE =  b"\n\r"

    # Matches the error *line* (with line ending)
    ERROR_LINE = re.compile(b"error id=(.)*? msg=(.)*?\n\r")

    # Matches the error line (without the line ending)
    ERROR = re.compile(b"error id=(.)*? msg=(.)*?")

    # Matches the end of the first response in a string.
    RESPONES = re.compile(b"(.)*?error id=(.)*? msg=(.)*?\n\r", re.DOTALL)
