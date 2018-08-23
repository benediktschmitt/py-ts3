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
This module contains a high-level API for the TeamSpeak 3 Server Query.
"""


# Modules
# ------------------------------------------------
import re
import time
import socket
import telnetlib
import logging

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


# Backward compatibility
# ------------------------------------------------
try:
    TimeoutError
except NameError:
    TimeoutError = OSError


# Data
# ------------------------------------------------
__all__ = [
    "TS3QueryError",
    "TS3TimeoutError",
    "TS3RecvError",
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


class TS3TimeoutError(TS3Error, TimeoutError):
    """
    Raised, if a response or event could not be received due to a *timeout*.
    """

    def __str__(self):
        tmp = "Could not receive data from the server within the timeout."
        return tmp


class TS3RecvError(TS3Error):
    """
    Raised if receiving data from the server failed, because the connection
    was closed or for other reasons.
    """

    def __str__(self):
        tmp = "Could not receive data from the server."
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

    .. warning::

        This class is **not thread safe**!
    """

    def __init__(self, host=None, port=10011):
        """
        If *host* is provided, the connection will be established before
        the constructor returns.

        .. seealso:: :meth:`open`
        """
        self._telnet_conn = None
        self._telnet_queue = None

        # The number of queries for which we have not received a response yet.
        self._num_pending_queries = 0

        # The undelivered events. These events are returned, the next time
        # *wait_for_event()* is called.
        self._event_queue = list()

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
            self._telnet_conn = telnetlib.Telnet(host, port, timeout)
            self._telnet_queue = list()

            # Wait for the first and the second greeting:
            # b'TS3\n\r'
            # b'Welcome to the [...] on a specific command.\n\r'
            self._telnet_conn.read_until(b"\n\r")
            self._telnet_conn.read_until(b"\n\r")

            self._num_pending_queries = 0
            self._event_queue = list()

            _logger.info("Created connection to {}:{}.".format(host, port))
        return None

    def close(self):
        """
        Sends the ``quit`` command and closes the telnet connection.
        """
        if self._telnet_conn is not None:
            try:
                # Sent it directly, to avoid a recursive call of this method.
                self._telnet_conn.write(b"quit\n\r")
            finally:
                self._telnet_conn.close()
                self._telnet_conn = None
                self._telnet_queue = None

                del self._event_queue[:]
                self._num_pending_queries = 0

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

    def _recv(self, timeout=None):
        """
        Blocks, until a message (response or event) has been received.

        If an event is received it is appended to the :attr:`_event_queue` and
        returned.

        If a query response is received, it is only returned (but not cachd).

        :arg float timeout:
            The maximum time in seconds waited for a response a event.
        :type timeout:
            None or float

        :rtype: TS3Event or TS3QueryResponse
        :returns:
            A TS3Event or TS3QueryResponse

        :raises TS3TimeoutError:
        :raises TS3RecvError:
        """
        end_time = timeout + time.time() if timeout is not None else None

        while True:
            timeout = end_time - time.time() if end_time is not None else None

            try:
                data = self._telnet_conn.read_until(b"\n\r", timeout=timeout)
            # Catch socket and telnet errors
            except (OSError, EOFError) as err:
                self.close()
                raise
            # Handle the receives message.
            else:
                if not data:
                    raise TS3TimeoutError()
                elif data.startswith(b"notify"):
                    event = TS3Event(data)
                    self._event_queue.append(event)
                    return event

                elif data.startswith(b"error"):
                    self._telnet_queue.append(data)
                    data = b"".join(self._telnet_queue)
                    self._telnet_queue = list()

                    resp = TS3QueryResponse(data)
                    self._num_pending_queries -= 1
                    return resp
                else:
                    self._telnet_queue.append(data)
        return None

    def wait_for_event(self, timeout=None):
        """
        Blocks until an event is received or the *timeout* exceeds. The next
        received event is returned.

        A simple event loop looks like this:

        .. code-block:: python3

            ts3conn.servernotifyregister(event="server")
            while True:
                ts3conn.send_keepalive()
                try:
                    event = ts3conn.wait_for_event(timeout=60)
                except TS3TimeoutError:
                    pass
                else:
                    # Handle the received event here ...

        :arg timeout:
            The maximum number of seconds waited for the next event.
        :type timeout:
            None or float

        :rtype: TS3Event
        :returns:
            The next received ts3 event.

        :raises TS3TimeoutError:
        :raises TS3RecvError:
        """
        start_time = time.time()
        while not self._event_queue:

            if timeout is not None:
                remaining_time = timeout - (time.time() - start_time)
                if remaining_time <= 0:
                    raise TS3TimeoutError()
            else:
                remaining_time = None

            self._recv(timeout=remaining_time)

        return self._event_queue.pop(0) if self._event_queue else None

    def _wait_for_resp(self, timeout=None):
        """
        Waits for the response to the last issued query.

        :arg timeout:
            The maximum number of seconds waited for the query response.
        :type timeout:
            None or int

        :raises TS3TimeoutError:
        :raises TS3ResponseRecvError:
        :raises TS3QueryError:
        """
        assert self._num_pending_queries

        start_time = time.time()
        resp = None
        while not (isinstance(resp, TS3QueryResponse) and self._num_pending_queries == 0):

            if timeout is not None:
                remaining_time = timeout - (time.time() - start_time)
                if remaining_time <= 0:
                    raise TS3TimeoutError()
            else:
                remaining_time = None

            resp = self._recv(timeout=remaining_time)

        if resp.error["id"] != "0":
            raise TS3QueryError(resp)
        return resp

    # Sending
    # -------------------------

    def send_keepalive(self):
        """
        Sends an empty query to the server to prevent automatic disconnect.
        Make sure to call it at least once in 5 minutes (better each minute).
        """
        self._telnet_conn.write(b" \n\r")
        return None

    def send(self, command, common_parameters=None, unique_parameters=None,
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
        self._telnet_conn.write(query_command)

        # To identify the response when we receive it.
        self._num_pending_queries += 1

        return self._wait_for_resp(timeout=timeout)


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

    def quit(self):
        """
        Closes the connection.
        """
        self.close()
        return None
