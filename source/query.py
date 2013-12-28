#!/usr/bin/python3


# Modules
# ------------------------------------------------
import re
import socket
import telnetlib

# local
from protocoll import TS3Commands

# Data
# ------------------------------------------------
__all__ = [
    "TS3Escape",
    "TS3RegEx",
    "TS3ParserError",
    "TS3Response",
    "TS3Connection"]


# Classes
# ------------------------------------------------
class TS3Escape(object):

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

    # The same map, but with the byte strings.
    _B_MAP = [(e0.encode(), e1.encode()) for e0, e1 in _MAP]

    @classmethod
    def _get_map(cls, str_):
        """
        Returns the string escape map or the bytes escape map, depending
        on the type of *str_*. If there's no map for the type of *str_*
        available, a TypeError is raised.
        """
        if isinstance(str_, bytes):
            return cls._B_MAP
        elif isinstance(str_, str):
            return cls._MAP
        else:
            raise TypeError("*str_* has to be bytes or str object.")        

    @classmethod
    def escape(cls, str_):
        """
        Escapes the characters in the string as described in the manual.

        >>> TS3Escape.escape('Hallo Welt')
        'Hallo\\sWelt'
        """                
        # The order of the replacement is not trivial.
        for char, repl_char in cls._get_map(str_):
            str_ = str_.replace(char, repl_char)
        return str_

    @classmethod
    def unescape(cls, str_):
        """
        Unescapes the charactes in the string as described in the manual.

        >>> TS3Escape.unescape('Hallo\\sWelt')
        'Hallo Welt'
        """
        # Again, the order of the replacement is not trivial.
        for repl_char, char in reversed(cls._get_map(str_)):
            str_ = str_.replace(char, repl_char)
        return str_

    @classmethod
    def parameters_to_str(cls, params):
        """
        Folds the *params* dict to a string, so that it can be used in a query
        command.
        If *params* is None, the empty string is returned.
        
        >>> TS3Escape.properties_to_str({'virtualserver_name': 'foo bar'})
        'virtualserver_name=foo\\\sbar'
        """
        if params is None:
            return str()
        
        # It's not necessairy to escape the key.
        tmp = " ".join(str(key).lower() + "=" + cls.escape(str(val))
                       for key, val in params.items())
        return tmp

    @classmethod
    def key_mulval_to_str(cls, key, values):
        """
        Can be used to convert multiple key value pairs, with the same key
        to a valid TS3 ServerQuery string.
        
        >>> TS3Escape.key_mulval_str('clid', [1,2,3])
        'clid=1|clid=2|clid=3'
        """
        key = str(key)
        tmp = "|".join(key + "=" + cls.escape(str(val))
                       for val in values)
        return tmp

    @classmethod
    def options_to_str(cls, options):
        """
        Escapes the options and adds a *-* if necessairy to each option.
        If *options* is None, the empty string will be returned.

        >>> TS3Escape.options_to_str(['permsid', '-virtual'])
        '-permsid -virtual'
        """
        if options is None:
            return str()
        
        tmp = list()
        for i, e in enumerate(options):
            if not e.startswith("-"):
                e = "-" + e
            tmp.append(e)        
        tmp = " ".join(tmp)
        return tmp
    

class TS3RegEx(object):
    """
    Frequently used and important regular expressions.
    """

    # XXX: The telnet interface does not accept compiled regex.
    LINE =  b"\n\r"

    # Matches the error *line* (with line ending)
    ERROR_LINE = re.compile(b"error id=(.)*? msg=(.)*?\n\r")

    # Matches the error line (without the line ending)
    ERROR = re.compile(b"error id=(.)*? msg=(.)*?")

    # Matches the end of the first response in a string.
    RESPONES = re.compile(b"(.)*?error id=(.)*? msg=(.)*?\n\r", re.DOTALL)
 

class TS3ParserError(Exception):
    """
    Raised, if the data could not be parsed. Only used internally.
    """
    pass

    
class TS3Response(object):
    """
    Parses **ONE** response and stores it's data.
    """
        
    def __init__(self, data):
        self._data = data

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
        The error id of the returned command.
        """
        self._parse_error()
        return self._error    

    # ----------- DICT TYPE ----------

    def __getitem__(self, key):
        """
        Returns the value in the *parsed* dict corresponding to the *key*.
        """
        return self.parsed[key]

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
        Traceback (most recent call last):
          ...
            raise TS3ParserError()
        TS3ParserError
        """
        prop = prop.split(b"=")
        if len(prop) == 1:
            key = prop[0]
            val = bytes()
        elif len(prop) == 2:
            key, val = prop
        else:
            # XXX: If a b'=' is in a string. Error occured while parsing
            #  b''client_unique_identifier=gZ7Kw+uoO9LppsDG0\\/T2lqOGIik='
            key = prop[0]
            val = b"=".join(prop[1:])

        # TODO: Is decoding really necessairy?
        try:
            key = key.decode()
            val = val.decode()
        except UnicodeDecodeError:
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

    
class TS3BaseConnection(object):
    """
    The TS3 query client.

    For a more convenient interface, use the TS3Connection class.    
    """ 
   
    def __init__(self, host=None, port=10011):
        """
        If *host* is provided, the connection will be established before
        the constructor returns.
        """
        self._telnet_conn = None

        # Counter for unfetched responses and a queue for the responses.
        self._unfetched_resp = 0
        self._responses = list()

        # Always wait for responses.
        self.wait_for_resp = False
        
        if host is not None:
            self.open(host, port)
        return None

    def get_telnet_connection(self):
        """
        Returns the used telnet instance.
        """
        return self._telnet_conn

    def is_connected(self):
        """
        Returnes *True*, if a connection is currently established.
        """
        return self._telnet_conn is not None

    def open(self, host, port=10011,
                timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """
        Connect to a TS3 server.

        The optional second argument is the port number, which defaults to the
        standard TS3 ServerQuery port (10011).

        If a connection has already been established, an Exception will be
        raised.
        """
        if not self.is_connected():
            self._telnet_conn = telnetlib.Telnet(host, port, timeout)            
            # Wait for the first and the second greeting:
            # b'TS3\n\r'
            # b'Welcome to the [...] on a specific command.\n\r'
            self._telnet_conn.read_until(b"\n\r")
            self._telnet_conn.read_until(b"\n\r")
        return None

    def close(self):
        """
        Sends the *quit* command and closes the telnet connection.
        """
        if self.is_connected():
            try:
                self.send("quit")
            finally:
                self._telnet_conn.close()
                self._telnet_conn = None
                
                self._unfetched_resp = 0
                self._responses = list()
        return None

    def fileno(self):
        """
        Return the fileno() of the socket object used internally.
        """
        return self._telnet_conn.fileno()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()
        return None

    def __del__(self):
        self.close()
        return None

    def send(self, command, parameters=None, options=None):
        """
        The general syntax of a TS3 query command is:
        
            command [parameter...] [option]
            
        where *command* is a single word, *parameter* is a key value pair and
        *option* is a word beginning with *-*.
        
            command key1=value1 key2=value2 ... -option1 -option2 ...
            
        Examples:
        ---------
            >>> # serverlist
            >>> self.send("serverlist")
            
            >>> # clientlist -uid -away
            >>> self.send("clientlist", options=["uid", "away"])
            
            >>> # clientdbfind pattern=FOOBAR -uid
            >>> self.send("clientdbfind", {"pattern": "FOOBAR"}, ["uid"])
        """
        # Escape the command and build the final query command string.
        command = str(command)
        parameters = TS3Escape.parameters_to_str(parameters)
        options = TS3Escape.options_to_str(options)
        
        query_command = command + " " + parameters + " " + options + "\n\r"
        query_command = query_command.encode()

        # Send the command.
        return self.send_raw(query_command)

    def send_raw(self, msg):
        """
        Sends the bytestring *msg* directly to the server. If *msg* is
        a string, it will be encoded.

        !!! DON'T FORGET THE b'\n\r' ENDING !!!
        """
        if isinstance(msg, str):
            msg = msg.encode()
        self._telnet_conn.write(msg)
        self._unfetched_resp += 1
        
        if self.wait_for_resp:
            self._recv()
        return None

    def _recv(self):
        """
        Waits for a response and stores all responses in *self._resp*.

        Stores unfetched responses in the resp_queue.
        """
        # Send the new command.
        all_resp = list()
        resp = list()
        while self._unfetched_resp:
            line = self._telnet_conn.read_until(TS3RegEx.LINE)
            resp.append(line)
            if re.match(TS3RegEx.ERROR_LINE, line):
                all_resp.append(TS3Response(resp))
                resp = list()
                self._unfetched_resp -= 1
        self._responses.extend(all_resp)
        return None

    @property
    def resp(self):
        """
        Fetches all unfetched responses and returns them.
        """
        self._recv()
        return self._responses

    @property
    def last_resp(self):
        """
        Returns the last response. If there's no response available,
        None is returned.
        """
        self._recv()
        return self._responses[-1] if self._responses else None
        
    def flush_resp_queue(self):
        """
        Clears the response queue.
        """
        self._responses = list()
        return None


class TS3Connection(TS3BaseConnection, TS3Commands):
    """
    TS3 server query client.
    """

    def _return_proxy(self, cmd, params, opt):
        """
        Executes the command created with a method of TS3Protocoll directly.
        """
        return TS3BaseConnection.send(self, cmd, params, opt)

    
# Main
# ------------------------------------------------
if __name__ == "__main__":
    from pprint import pprint

    with TS3Connection("localhost") as ts3conn:
        ts3conn.login("serveradmin", "1U0FkWci")
        ts3conn.use(1)
        ts3conn.gm("Hello World")

        ts3conn.channellist()
        pprint(ts3conn.last_resp.parsed)
