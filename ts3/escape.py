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
__all__ = ["TS3Escape"]


# Classes
# ------------------------------------------------
class TS3Escape(object):
    """
    Methods to escape a string properly and to build query strings.
    The methods work only correct, if the parameters have the correct type.
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
    def escape(cls, txt):
        """
        txt: str
        
        Escapes the characters in the string *txt* as described in the
        TS3 server query manual:

            >>> TS3Escape.escape('Hallo Welt')
            'Hallo\\sWelt'
        """
        if not isinstance(txt, str):
            raise TypeError("*txt* has to be a string.")
            
        # The order of the replacement is not trivial.
        for char, repl_char in cls._MAP:
            txt = txt.replace(char, repl_char)
        return txt

    @classmethod
    def unescape(cls, txt):
        """
        txt: str
        
        Unescapes the charactes in the string *txt* as described in the
        manual.

            >>> TS3Escape.unescape('Hallo\\sWelt')
            'Hallo Welt'
        """
        if not isinstance(txt, str):
            raise TypeError("*txt* has to be a string.")
        
        # Again, the order of the replacement is not trivial.
        for repl_char, char in reversed(cls._MAP):
            txt = txt.replace(char, repl_char)
        return txt

    @classmethod
    def parameters_to_str(cls, params):
        """
        *params* is either a dictionary with the possible key-value types:
            key    value
            str -> str
            str -> [str]
            str -> None

        or None.

        The return value is a string formatted as described in the TS3 server
        query manual:

            >>> # None
            >>> TS3Escape.parameters_to_str(None)
            ''
            
            >>> # key -> str
            >>> TS3Escape.parameters_to_str({'virtualserver_name': 'foo bar'})
            'virtualserver_name=foo\\\sbar'

            >>> # key -> [str]
            >>> TS3Escape.parameters_to_str({'clid': [0,2,4,45]})
            'clid=0|clid=2|clid=4|clid=45'
            
            >>> # key -> None
            >>> TS3Escape.parameters_to_str({"permsid": None})
            ''
        """
        if params is None:
            return str()

        tmp = list()
        for key, val in params.items():
            # Escaping a key will never making it a valid key.
            key = key.lower()

            if val is None:
                pass
            elif isinstance(val, list):
                tmp.append(cls.key_mulval_to_str(key, val))
            else:
                val = cls.escape(str(val))
                tmp.append(key + "=" + val)
        tmp = " ".join(tmp)
        return tmp

    @classmethod
    def key_mulval_to_str(cls, key, values):
        """
        key: str
        values: [str|None]
        
        Can be used to convert multiple key value pairs, with the same key
        to a valid TS3 server query string. If an item is None, it will be
        ignored:
        
            >>> TS3Escape.key_mulval_str('clid', [1, 2, None, 3])
            'clid=1|clid=2|clid=3'
        """
        key = str(key).lower()
        tmp = "|".join(key + "=" + cls.escape(val) \
                       for val in values if val is not None)
        return tmp

    @classmethod
    def options_to_str(cls, options):
        """
        options: None | [str|None]
        
        Escapes the options and prepends a *-* if necessairy to an option.
        If *options* is None, the empty string will be returned. If
        *options* itself is None, the emtpy string will be returned.

            >>> TS3Escape.options_to_str(None)
            ''

            >>> TS3Escape.options_to_str([None, 'permsid', '-virtual'])
            '-permsid -virtual'
        """
        if options is None:
            return str()

        # Either an option is valid or not. Escaping doesn't change this fact.
        tmp = list()
        for i, e in enumerate(options):
            if e is None:
                continue
            elif not e.startswith("-"):
                e = "-" + e
            tmp.append(e)
        tmp = " ".join(tmp)
        return tmp
