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
This module contains classes and functions used to build valid query strings
and to unescape responses.
"""


# Data
# ------------------------------------------------
__all__ = ["TS3Escape"]


# Classes
# ------------------------------------------------
class TS3Escape(object):
    """
    Provides methods to escape a string properly and to build query strings.
    """

    # Table with escape strings.
    # DO NOT CHANGE THE ORDER, IF YOU DON'T KNOW, WHAT YOU'RE DOING.
    _MAP = [
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

    @classmethod
    def escape(cls, raw):
        """
        Escapes the value of *raw*.

        >>> TS3Escape.escape(None)
        ''
        >>> TS3Escape.escape(2)
        '2'
        >>> TS3Escape.escape(True)
        '1'
        >>> TS3Escape.escape('Hello World')
        'Hello\\sWorld'

        :arg raw: The value to escape.
        :type raw: None, str, bool, int or RawParameter

        :return: The escaped value of *raw*
        :rtype: string

        :raises TypeError: If *raw* has an unsupported type.
        """
        if raw is None:
            return str()
        elif isinstance(raw, bool):
            return "1" if raw else "0"
        elif isinstance(raw, int):
            return str(raw)
        elif isinstance(raw, str):
            # The order of the replacement is not trivial.
            for char, repl_char in cls._MAP:
                raw = raw.replace(char, repl_char)
            return raw
        elif isinstance(raw, RawParameter):
            return str(raw)
        else:
            raise TypeError("*raw* has to be a string.")

    @classmethod
    def unescape(cls, txt):
        """
        Unescapes the str *txt*.

        >>> TS3Escape.unescape('Hello\\sWorld')
        'Hello World'

        :arg txt: The string to escape.
        :type txt: string

        :raises TypeError: If *txt* is not a string.
        """
        if isinstance(txt, str):
            # Again, the order of the replacement is not trivial.
            for repl_char, char in reversed(cls._MAP):
                txt = txt.replace(char, repl_char)
            return txt
        else:
            raise TypeError("*txt* has to be a string.")

    @classmethod
    def escape_parameters(cls, parameters):
        """
        Escapes the parameters of a TS3 query and encodes it as a part
        of a valid ts3 query string.

        >>> # None
        >>> TS3Escape.escape_parameters(None)
        ''
        >>> # key -> str
        >>> TS3Escape.escape_parameters({'virtualserver_name': 'foo bar'})
        'virtualserver_name=foo\\\sbar'
        >>> # key -> None
        >>> TS3Escape.escape_parameters({"permsid": None})
        ''
        >>> # Of course, you can mix them:
        >>> TS3Escape.escape_parameters(
        ...     {'virtualserver_name': 'foo bar',
        ...      'permsid': None}
        ...     )
        'virtualserver_name=foo\\\sbar'

        :arg parameters: The dictionary with the key value pairs.
        :type parameters: dictionary
        """
        if parameters is None:
            return str()

        tmp = list()
        for key, val in parameters.items():
            if val is None:
                continue
            # Note, that escaping a key will never make it valid or invalid.
            # In other words: It's not necessairy to escape the key.
            key = key.lower()
            val = cls.escape(val)
            # if the key is empty => do not add an equal sign
            # this allows unnamed parameters
            if key:
                tmp.append(key + "=" + val)
            else:
                tmp.append(val)
        tmp = " ".join(tmp)
        return tmp

    @classmethod
    def escape_parameterlist(cls, parameterslist):
        """
        Escapes each parameter dictionary in the parameterslist and encodes
        the list as a part of a valid ts3 query string.

        >>> TS3Escape.escape_parameterlist(None)
        ''
        >>> TS3Escape.escape_parameterlist(
        ...     [{"permid": 17276, "permvalue": 50, "permskip": 1},
        ...      {"permid": 21415, "permvalue": 20, "permskip": 0}]
        ...     )
        'permid=17276 permvalue=50 permskip=1|permid=21415 permvalue=20 permskip=0'

        Note, that the order of the parameters might change, when you use the
        built-in dictionary, that does not care about the order.

        :arg parameterslist: A list of parameters.
        :type parameterslist: None or a list of dictionaries
        """
        if parameterslist is None:
            return str()

        tmp = "|".join(cls.escape_parameters(parameters) \
                       for parameters in parameterslist)
        return tmp

    @classmethod
    def escape_options(cls, options):
        """
        Escapes the items in the *options* list and prepends a '-' if
        necessairy.
        If *options* is None, the empty string will be returned.

        >>> TS3Escape.options_to_str(None)
        ''
        >>> TS3Escape.options_to_str([None, 'permsid', '-virtual'])
        '-permsid -virtual'

        :arg options: A list with the options.
        :type options: None or a list of strings.
        """
        if options is None:
            return str()

        # Either an option is valid or not.
        # Escaping doesn't change this fact.
        tmp = list()
        for i, e in enumerate(options):
            if e is None:
                continue
            elif not e.startswith("-"):
                e = "-" + e
            tmp.append(e)
        tmp = " ".join(tmp)
        return tmp


class RawParameter():
    """Parameters wrapped in a RawParameter are not escaped."""

    def __init__(self, parameter):
        """
        :arg parameter: The parameter which should not be escaped
        :type parameter: string
        """
        self.parameter = parameter

    def __str__(self):
        return self.parameter
