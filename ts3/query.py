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


# Modules
# ------------------------------------------------
import re
import socket
import telnetlib
import logging

# local
try:
    from commands import TS3Commands
    from common import TS3RegEx
    from escape import TS3Escape
    from response import TS3Response
    from exceptions import TS3QueryError
except ImportError:
    from .commands import TS3Commands
    from .common import TS3RegEx
    from .escape import TS3Escape
    from .response import TS3Response
    from .exceptions import TS3QueryError
    

# Data
# ------------------------------------------------
__all__ = [
    "TS3RegEx",
    "TS3BaseConnection",
    "TS3Connection"]

_logger = logging.getLogger(__name__)


# Classes
# ------------------------------------------------
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

        # Always wait for responses if true.
        self.patient_mode = False

        # Wait for responses and raise an error, if the error code of the
        # response is not 0.
        self.quiet_mode = False
        
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

        if self.patient_mode or not self.quiet_mode:
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
                resp = TS3Response(resp)
                self._responses.append(resp)
                self._unfetched_resp -= 1

                # Raise an error, if wished.
                if (not self.quiet_mode) and resp.error["id"] != "0":
                    raise TS3QueryError(resp.error["id"], resp.error["msg"])
                
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
