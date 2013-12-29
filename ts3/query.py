#!/usr/bin/python3


# Modules
# ------------------------------------------------
import re
import socket
import telnetlib

# local
try:
    from commands import TS3Commands
except ImportError:
    from .commands import TS3Commands
    

# Data
# ------------------------------------------------
__all__ = [
    "TS3Escape",
    "TS3RegEx",
    "TS3ParserError",
    "TS3Response",
    "TS3BaseConnection",
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
 

class TS3ParserError(Exception):
    """
    Raised, if the data could not be parsed. Only used internally.
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
            tmp = b"\n".join(self._data)
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
        The error id of the returned command.
        """
        self._parse_error()
        return self._error    

    # ----------- DICT TYPE ----------

    def __getitem__(self, index):
        """
        Todo: let this simulate a dict, not a list.
        """
        # self[0, "cid"] -> self.parsed[index][key] <- Not nice
        return self.parsed[index]

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
        command: str
        parameters: None | {str->None|str->[str]|str->str}
        options: None | [None|str]
        
        The general syntax of a TS3 query command is:
        
            command [parameter...] [option]
            
        where *command* is a single word, *parameter* is a key value pair and
        *option* is a word beginning with *-*.
        
            command key1=value1 key2=value2 ... -option1 -option2 ...
            
        Possible calls:
        ---------------
            >>> # serverlist
            >>> self.send("serverlist")
            
            >>> # clientlist -uid -away
            >>> self.send("clientlist", options=["uid", "away"])
            
            >>> # clientdbfind pattern=FOOBAR -uid
            >>> self.send("clientdbfind", {"pattern": "FOOBAR"}, ["uid"])
        """
        # Escape the command and build the final query command string.
        if not isinstance(command, str):
            raise TypeError("*command* has to be a string.")
        
        command = command
        parameters = TS3Escape.parameters_to_str(parameters)
        options = TS3Escape.options_to_str(options)
        
        query_command = command + " " + parameters + " " + options + "\n\r"
        query_command = query_command.encode()

        return self.send_raw(query_command)

    def send_raw(self, msg):
        """
        msg: bytes
        
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
        Blocks until all unfetched responses are received. The responses
        are stored in *self_resp*.
        """
        resp = list()
        while self._unfetched_resp:
            line = self._telnet_conn.read_until(TS3RegEx.LINE)
            resp.append(line)
            if re.match(TS3RegEx.ERROR_LINE, line):
                self._responses.append(TS3Response(resp))
                self._unfetched_resp -= 1
                resp = list()
        return None

    @property
    def resp(self):
        """
        Fetches all unfetched responses and returns all responses in the
        response list.
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
        
    def clear_resp_list(self):
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
        pprint(ts3conn.last_resp.error)
        
        ts3conn.use(1)
        pprint(ts3conn.last_resp.error)
        
        ts3conn.gm("Hello World")
        pprint(ts3conn.last_resp.error)

        ts3conn.whoami()
        pprint(ts3conn.last_resp.parsed)
