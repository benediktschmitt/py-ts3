#!/usr/bin/python3


# Modules
# ------------------------------------------------
import re

# local
try:
    from common import TS3RegEx
    from escape import TS3Escape
except ImportError:
    from .common import TS3RegEx
    from .escape import TS3Escape


# Data
# ------------------------------------------------
__all__ = ["TS3Response"]


# Classes
# ------------------------------------------------
class TS3ParserError(Exception):
    """
    Raised, if the data could not be parsed.
    Only used internally and never uncatched.
    """
    pass

    
class TS3Response(object):
    """
    Parses **ONE** response and stores it's data. If you init an instance
    with the data of more than one response, parsing will fail.

    Note, that this class is **lazy**. The response is only parsed, if you
    request an attribute, that requires a parsed version of the data.
    """
        
    def __init__(self, data):
        self._data = data
        self._data_bytestr = None

        self._parsed = None
        self._parseable = None
        
        self._error = None
        return None

    @property
    def data(self):
        """
        The raw response as byte list.
        """
        return self._data

    @property
    def data_bytestr(self):
        """
        Returns the data as byte string.
        """
        if self._data_bytestr is None:
            tmp = b"\n\r".join(self._data)
            self._data_bytestr = tmp
        return self._data_bytestr

    @property
    def parsed(self):
        """
        The parsed response as list of dictionaries. If the response
        is not parseable, None.
        """
        self._parse_content()
        return self._parsed

    @property
    def is_parseable(self):
        """
        Returns True, if the data is parseable and has been parsed.
        """
        self._parse_content()
        return self._parseable
    
    @property
    def error(self):
        """
        Dictionary, that contains the error attributes of the response.
        """
        self._parse_error()
        return self._error

    # ----------- LIST EMULATION ----------

    # Only rudimentary support. I think nobody should need more.
    
    def __getitem__(self, index):
        return self.parsed[index]

    def __len__(self):
        return len(self.parsed)

    def __iter__(self):
        return iter(self.parsed)

    # ----------- PARSER ----------
    
    """
    The data is parsed after this simplified syntaxdiagramm:
               
                  +-----------------+
        data -----|                 |----->
                  +-----> item -----+
                     ^           |
                     +--- b'|' <-+

        item -----> property ----->
               ^               |
               +--- b' '     <-+

                                 +------------------------------+
        property -----> key -----|                              |----->
                                 +-----> b'=' -----> value -----+

        Terminals: {key, value}

    The return value is then similar to this structure:
    
        [{key00: val00, key01: val01, ...}, # item 0
         {key10: val10, key11: val11, ...}, # item 1
         ...
        ]

    Note, that if a property has no value, the value will be set to b''.
    """

    def _parse_property(self, prop):
        """
        >>> parse_property(b'key=value')
        ('key', 'value')
        
        >>> parse_property(b'foo')
        ('foo', '')

        >>> parse_property(b'client_unique_identifier=gZ7K[...]GIik=')
        ('client_unique_identifier', 'gZ7K[...]GIik=')
        """
        prop = prop.split(b"=")
        if len(prop) == 1:
            key = prop[0]
            val = bytes()
        elif len(prop) == 2:
            key, val = prop
        else:
            key = prop[0]
            val = b"=".join(prop[1:])

        try:
            key = key.decode()
            val = val.decode()
        except UnicodeDecodeError:
            # Todo: - Should we simply ignore decode errors?
            #       - Is decoding reasonable?
            raise TS3ParserError()

        key = TS3Escape.unescape(key)
        val = TS3Escape.unescape(val)
        return (key, val)

    def _parse_item(self, item):
        """
        >>> parse_item(b'key0=val0 key1=val1')
        {'key0': 'val0', 'key1': 'val1'}
        """
        properties = item.split()
        properties = dict(self._parse_property(p) for p in properties)
        return properties

    def _parse_content(self):
        """
        Parses *self._data* excluding the error line.
        """
        # Return, if we already tried to parse the data.
        if self._parsed is not None or self._parseable is not None:
            return None

        try:
            parsed = list()
            for i, line in enumerate(self._data):
                # Don't parse the error line.
                if i + 1 == len(self._data):
                    break
                # Split the items
                line = line.split(b"|")
                line = [self._parse_item(item) for item in line]
                parsed.extend(line)
        except TS3ParserError:
            self._parsed = None
            self._parseable = False
        else:
            self._parsed = parsed
            self._parseable = True
        return None

    def _parse_error(self):
        """
        Parses the *error* line of a TS3 query response and saves it's value
        in *self._error*.

        >>> self._parse_error(b'error id=0 msg=ok')
        """
        # Skip if we already parsed the error line.
        if self._error is not None:
            return None
        
        # The error line is the last line in the response. This line is usually
        # in all ts3 query responses.
        tmp = self._data[-1]
        if not re.match(TS3RegEx.ERROR, tmp):
            raise ValueError("No *error* line!")

        tmp = tmp.split()
        error = dict(self._parse_property(tmp[i]) \
                     for i in range(1, len(tmp)))

        self._error = error
        return None
