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
