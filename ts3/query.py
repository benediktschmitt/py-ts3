#!/usr/bin/python3

# The MIT License (MIT)
# 
# Copyright (c) 2013-2014 Benedikt Schmitt
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
This module contains a high-level API for the TeamSpeak 3 Server Query.
"""


# Modules
# ------------------------------------------------
import re
import time
import socket
import telnetlib
import logging
import threading

# local
try:
    from commands import TS3Commands
    from common import TS3Error
    from escape import TS3Escape
    from response import TS3Response, TS3QueryResponse, TS3Event
except ImportError:
    from .commands import TS3Commands
    from .common import TS3Error
    from .escape import TS3Escape
    from .response import TS3Response, TS3QueryResponse, TS3Event
    

# Data
# ------------------------------------------------
__all__ = [
    "TS3QueryError",
    "TS3ResponseRecvError",
    "TS3BaseConnection",
    "TS3Connection"]

_logger = logging.getLogger(__name__)


# Exceptions
# ------------------------------------------------
class TS3QueryError(TS3Error):
    """
    Raised, if the error code of the response was not 0.
    """

    def __init__(self, resp):
        #: The :class:`TS3Response` instance with the response data.
        self.resp = resp
        return None

    def __str__(self):
        tmp = "error id {}: {}".format(
            self.resp.error["id"], self.resp.error["msg"])
        return tmp


class TS3ResponseRecvError(TS3Error, TimeoutError):
    """
    Raised, if a response could not be received due to a *timeout* or
    if the receive progress has been *canceled* by another thread.
    """

    def __str__(self):
        tmp = "Could not receive the response from the server."
        return tmp
    

# Classes
# ------------------------------------------------
class TS3BaseConnection(object):
    """
    The TS3 query client.

    This class provides only the methods to **handle** the connection to a
    TeamSpeak 3 Server. For a more convenient interface, use the
    :class:`TS3Connection` class.

    Note, that this class supports the ``with`` statement:

        >>> with TS3BaseConnection() as ts3conn:
        ...     ts3conn.open("localhost")
        ...     ts3conn.send(...)
        >>> # This is equal too:
        >>> ts3conn = TS3BaseConnection()
        >>> try:
        ...     ts3conn.open("localhost")
        ...     ts3conn.send(...)
        ... finally:
        ...     ts3conn.close()
    """ 
   
    def __init__(self, host=None, port=10011):
        """
        If *host* is provided, the connection will be established before
        the constructor returns.

        .. seealso:: :meth:`open`
        """
        # None, if the client is not connected.
        self._telnet_conn = None

        # The last query id, that has been given.
        self._query_counter = 0
        
        # The last query id, that has been fetched.
        self._query_id = 0

        # Maps the query id to the response.
        # query id => TS3Response
        self._responses = dict()

        # Set to true, if a new response has been received.
        self._new_response_event = threading.Condition()

        # Avoid sending data to the same time.
        self._send_lock = threading.Lock()

        # To stop the receive progress, if we are waiting for events from
        # another thread.
        self._stop_event = threading.Event()
        self._waiting_for_stop = False
        self._is_listening = False
        
        if host is not None:
            self.open(host, port)
        return None

    # *Simple* get and set methods
    # ------------------------------------------------

    @property
    def telnet_conn(self):
        """
        :getter:
            If the client is connected, the used Telnet instance
            else None.
        :type:
            None or :class:`telnetlib.Telnet`.
        """
        return self._telnet_conn

    def is_connected(self):
        """
        :return:
            True, if the client is currently connected.
        :rtype:
            bool
        """
        return self._telnet_conn is not None
        
    @property
    def last_resp(self):
        """
        :getter:
            The last received response.
        :type:
            :class:`~response.TS3Response`

        :raises LookupError:
            If no response has been received yet.
        """
        # Get the responses with the highest query id in the response
        # dictionary.
        try:
            tmp = max(self._responses)
        except ValueError:
            raise LookupError()
        else:
            return self._responses[tmp]

    def remaining_responses(self):
        """
        :return:
            The number of unfetched responses.
        :type:
            int
        """
        return self._query_counter - self._query_id
        
    # Networking
    # ------------------------------------------------
    
    def open(self, host, port=10011,
             timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """
        Connect to the TS3 Server listening on the address given by the
        *host* and *port* parmeters. If *timeout* is provided, this is the
        maximum time in seconds for the connection attempt.

        :raises OSError:
            If the client is already connected.
        :raises TimeoutError:
            If the connection can not be created.
        """
        if self.is_connected():
             raise OSError("The client is already connected.") 
        else:
            self._query_counter = 0
            self._query_id = 0
            self._responses = dict()

            self._telnet_conn = telnetlib.Telnet(host, port, timeout)            
            # Wait for the first and the second greeting:
            # b'TS3\n\r'
            # b'Welcome to the [...] on a specific command.\n\r'
            self._telnet_conn.read_until(b"\n\r")
            self._telnet_conn.read_until(b"\n\r")

            _logger.info("Created connection to {}:{}.".format(host, port))
        return None

    def close(self):
        """
        Sends the ``quit`` command and closes the telnet connection.

        If you are receiving data from another thread, this method will
        call :meth:`stop_recv` and therefore block, until the the receive
        thread stopped.
        """
        if self.is_connected():
            try:
                # We need to send the quit command directly to avoid
                # dead locks.
                self._telnet_conn.write(b"quit\n\r")
            finally:
                self.stop_recv()
                self._telnet_conn.close()
                self._telnet_conn = None
                _logger.debug("Disconnected client.")
        return None

    def fileno(self):
        """
        :return:
            The fileno() of the socket object used internally.
        :rtype:
            int
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

    # Receiving
    # -------------------------

    def on_event(self, event):
        """
        Called, when an event has been received.

        When you use ``servernotifyregister``, I assume, that you want to
        be informed, when the server reported an event. To use your own
        event handler, you have the choice between:
        
            * Subclassing and overwriting this method.
            * ts3conn.on_event = my_handler
        
        :arg event:
            The catched event.
        :type event:
            :class:`~response.TS3Event`
        """
        msg = "Uncatched event: {}".format(event.event)
        _logger.debug(msg)
        return None
    
    def wait_for_resp(self, query_id, timeout=None):
        """
        Waits for an response. This method will block untill the response to
        the query has been received, when *timeout* exceeds or when the
        connection is closed.

        :arg query_id:
            The id of the query internally used to identify the corresponding
            response.
        :type query_id:
            int

        :arg timeout:
            Maximum time in seconds waited for the response.
        :type timeout:
            None or int

        :raises TS3ResponseRecvError:
            If the response could not be received, because the connection has
            been closed or the timeout has been exceeded.
        :raises TS3QueryError:
            If the *error id* of the query was not 0.
        """
        if timeout is None:
            end_time = None
        else:
            end_time = time.time() + timeout

        while True:
            # We need to catch this case here, to avoid dead locks, when we
            # are not in threading mode.
            if query_id in self._responses:
                break           
            if not self.is_connected():
                break
            if timeout is not None and time.time() < end_time:
                break
            
            # Wait for a new response and try to find the
            # response corresponding to the query.
            with self._new_response_event:
                self._new_response_event.wait(timeout=0.1)

        resp = self._responses.get(query_id)
        if resp is None:
            raise TS3ResponseRecvError()
        if resp.error["id"] != "0":
            raise TS3QueryError(resp)
        return resp
    
    def stop_recv(self):
        """
        If :meth:`recv` has been called from another thread, it will be
        told to stop.
        This method blocks, until :meth:`recv` has terminated.
        """
        if self._is_listening:
            self._stop_event.clear()
            self._waiting_for_stop = True
            self._stop_event.wait()
        return None

    def recv_in_thread(self):
        """
        Calls :meth:`recv` in a thread. This is useful,
        if you used ``servernotifyregister`` and you expect to receive events.
        """
        thread = threading.Thread(target=self.recv, args=(True,))
        thread.start()
        return None

    def recv(self, recv_forever=False, poll_intervall=0.5):
        """
        Blocks untill all unfetched responses have been received or
        forever, if *recv_forever* is true.

        :arg recv_forever:
            If true, this method waits forever for a response and you have to
            call :meth:`stop_recv` from another thread, to stop it.
        :type recv_forever:
            bool

        :arg poll_intervall:
            Seconds between checks for the stop request.
        :type poll_intervall:
            float

        :raises RuntimeError:
            When the client is already listening.
        """           
        if self._is_listening:
            raise RuntimeError("Already receiving data!")
        
        self._is_listening = True
        try:
            lines = list()
            # Stop, when
            # * the client is disconnected.
            # * the stop flag is set.
            # * we don't recv forever and we don't wait for responses.
            while self.is_connected() \
                  and (not self._waiting_for_stop) \
                  and (self.remaining_responses() or recv_forever):

                # Read one line
                # 1.) An event (Note, that an event has no trailing error line)
                # 2.) Query response
                # 3.) The error line of the query response.                
                data = self._telnet_conn.read_until(
                    b"\n\r", timeout=poll_intervall)
                if not data:
                    continue
                
                lines.append(data)

                # If we found an error line, the previous received line must
                # be the response we are waiting for.
                if re.match(b"error id=(.)*? msg=(.)*?\n\r", data):
                    resp = TS3QueryResponse(lines)
                    lines = list()
                    
                    self._query_id += 1
                    self._responses[self._query_id] = resp

                    with self._new_response_event:
                        self._new_response_event.notify_all()
                
                # If we are not waiting for a response or we received two
                # lines and the second one is no error line, the first one
                # must have been an event.
                elif (not self.remaining_responses()) or len(lines) == 2:
                    event = TS3Event([lines.pop(0)])
                    self.on_event(event)
                    
        # Catch socket and telnet errors
        except (OSError, EOFError) as err:
            # We need to set this flag here, to avoid dead locks while closing.
            self._is_listening = False
            self.close()
            raise
        finally:
            self._stop_event.set()
            self._waiting_for_stop = False
            self._is_listening = False
        return None
    
    # Sending
    # -------------------------

    def send(self, command, common_paramters=None, unique_parameters=None,
             options=None, timeout=None):
        """
        The general structure of a query command is::

            <command> <options> <common parameters> <unique parameters>|<unique parameters>|...

        Examples are here worth a thousand words:

        >>> # clientaddperm cldbid=16 permid=17276 permvalue=50 permskip=1|permid=21415 permvalue=20 permskip=0
        >>> ts3conn.send(
        ...     command = "clientaddperm",
        ...     common_paramters = {"cldbid": 16},
        ...     parameterlist = [
        ...         {"permid": 17276, "permvalue": 50, "permskip": 1},
        ...         {"permid": 21415, "permvalue": 20, "permskip": 0}
        ...         ]
        ...     )
        >>> # clientlist -uid -away
        >>> ts3conn.send(
        ...     command = "clientlist",
        ...     options = ["uid", "away"]
        ...     )

        .. seealso::
            :meth:`recv`, :meth:`wait_for_resp`
        """
        # Escape the command and build the final query command string.
        if not isinstance(command, str):
            raise TypeError("*command* has to be a string.")
        
        command = command
        common_parameters = TS3Escape.escape_parameters(common_parameters)
        unique_parameters = TS3Escape.escape_parameterlist(unique_parameters)
        options = TS3Escape.escape_options(options)
        
        query_command = command\
                        + " " + common_parameters\
                        + " " +  unique_parameters\
                        + " " + options \
                        + "\n\r"
        query_command = query_command.encode()

        # Send the command.
        with self._send_lock:
            self._telnet_conn.write(query_command)
            # To identify the response when we receive it.
            self._query_counter += 1
            query_id = self._query_counter

        # Make sure, that we receive the command if we are not in
        # threading mode.
        try:
            self.recv()
        except RuntimeError:
            pass                
        return self.wait_for_resp(query_id, timeout)
    

class TS3Connection(TS3BaseConnection, TS3Commands):
    """
    TS3 server query client.

    This class provides the command wrapper capabilities
    :class:`~commands.TS3Commands` and the ability to handle a
    connection to a TeamSpeak 3 server of :class:`TS3BaseConnection`.

    >>> with TS3Connection("localhost") as tsconn:
    ...     # From the TS3Commands class:
    ...     ts3conn.login("serveradmin", "FooBar")
    ...     ts3conn.clientkick(1)
    """

    def _return_proxy(self, command, common_parameters, unique_parameters,
                      options):
        """
        Executes the command created with a method of TS3Commands directly.
        """
        return TS3BaseConnection.send(
            self, command, common_parameters, unique_parameters, options)
