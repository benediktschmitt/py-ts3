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
:mod:`ts3.escape`
=================

This module contains classes and functions used to build valid query strings
and to unescape responses.

.. versionchanged:: 2.0.0

    The *TS3Escape* class has been replaced by the :func:`escape` and
    :func:`unescape` functions, because most of its methods became
    obsolete with the introduction of the :class:`TS3QueryBuilder`.
"""

__all__ = [
    "escape",
    "unescape"
]


# Table with escape strings.
# DO NOT CHANGE THE ORDER, IF YOU DON'T KNOW, WHAT YOU'RE DOING.
_ESCAPE_MAP = [
    ("\\", r"\\"),
    ("/", r"\/"),
    (" ", r"\s"),
    ("|", r"\p"),
    ("\a", r"\a"),
    ("\b", r"\b"),
    ("\f", r"\f"),
    ("\n", r"\n"),
    ("\r", r"\r"),
    ("\t", r"\t"),
    ("\v", r"\v")
    ]


def escape(value):
    """
    Escapes the *value* as required by the Server Query Manual:

    .. code-block:: python

        >>> escape('Hello World')
        'Hello\\sWorld'
        >>> escape('TeamSpeak ]|[ Server')
        'TeamSpeak\s]\p[\sServer'

    :seealso: :func:`unescape`
    """
    # The order of the replacement is important.
    for char, repl_char in _ESCAPE_MAP:
        value = value.replace(char, repl_char)
    return value


def unescape(value):
    """
    Undo the escaping used for transport:

    .. code-block:: python

        >>> unescape('Hello\\sWorld')
        'Hello World'
        >>> unescape('TeamSpeak\s]\p[\sServer')
        'TeamSpeak ]|[ Server'
    """
    # The order of the replacement is important.
    for repl_char, char in reversed(_ESCAPE_MAP):
        value = value.replace(char, repl_char)
    return value
