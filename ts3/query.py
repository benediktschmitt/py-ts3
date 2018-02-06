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
:mod:`ts3.query`
================

This module contains a high-level API for the TeamSpeak 3 *Server Query* and
*Client Query plugin*.

.. versionchanged:: 2.0.0

    The :class:`TS3Connection` class has been renamed to
    :class:`TS3ServerConnection`.

.. versionadded:: 2.0.0

    The :class:`TS3ClientConnection` class has been added.
"""

# std
import re
import time
import socket
import telnetlib
import logging

# local
from .common import TS3Error
from .response import TS3Response, TS3QueryResponse, TS3Event
from .query_builder import TS3QueryBuilder


try:
    TimeoutError
except NameError:
    TimeoutError = OSError


__all__ = [
    "TS3InvalidCommandError",
    "TS3QueryError",
    "TS3TimeoutError",
    "TS3RecvError",
    "TS3BaseConnection",
    "TS3ServerConnection",
    "TS3ClientConnection"]


LOG = logging.getLogger(__name__)


class TS3InvalidCommandError(TS3Error, ValueError):
    """
    Raised if a :class:`TS3QueryBuilder` is constructed with an unknown
    command.

    :seealso: :attr:`TS3BaseConnection.COMMAND_SET`
    """

    def __init__(self, cmd, valid_cmds):
        #: The unknown command.
        self.cmd = cmd

        #: A set with all allowed (known) commands.
        self.valid_cmds = valid_cmds
        return None

    def __str__(self):
        tmp = "The command '{}' is unknown.".format(self.cmd)
        return tmp


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


class TS3BaseConnection(object):
    """
    The TS3 query client.

    This class provides only the methods to **handle** the connection to a
    TeamSpeak 3 query service. For a more convenient interface, use the
    :class:`TS3ServerConnection` or :class:`TS3ClientConnection` class.

    Note, that this class supports the *with* statement::

        with TS3BaseConnection() as ts3conn:
            ts3conn.open("localhost")
            ts3conn.exec_("use", sid=1)

        # You can also use an equal try-finally construct.
        ts3conn = TS3BaseConnection()
        try:
            ts3conn.open("localhost")
            ts3conn.exec_("use", sid=1)
        finally:
            ts3conn.close()

    .. warning::

        This class is **not thread safe**!

    .. versionchanged:: 2.0.0

        The *send()* method has been removed, use :meth:`exec_`, :meth:`query`
        instead.
    """

    #: The default port to use when no port is specified.
    DEFAULT_PORT = None

    #: The length of the greeting. This is the number of lines returned by
    #: the query service after successful connection.
    #:
    #: For example, the TS3 Server Query returns these lines upon connection::
    #:
    #:      b'TS3\n\r'
    #:      b'Welcome to the [...] on a specific command.\n\r'
    GREETING_LENGTH = None

    #: A set with all known commands.
    COMMAND_SET = set()

    def __init__(self, host=None, port=None):
        """
        If *host* and *port* are provided, the connection will be established
        before the constructor returns.

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

    def open(self, host, port=None,
             timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """
        Connect to the TS3 query service listening on the address given by the
        *host* and *port* parameters. If *timeout* is provided, this is the
        maximum time in seconds for the connection attempt. If no *port* is
        provided, then the :attr:`DEFAULT_PORT` is used.

        :raises OSError:
            If the client is already connected.
        :raises TimeoutError:
            If the connection can not be created.
        """
        port = port or self.DEFAULT_PORT

        if self.is_connected():
             raise OSError("The client is already connected.")
        else:
            self._telnet_conn = telnetlib.Telnet(host, port, timeout)
            self._telnet_queue = list()

            # Skip the greeting.
            for i in range(self.GREETING_LENGTH):
                self._telnet_conn.read_until(b"\n\r")

            self._num_pending_queries = 0
            self._event_queue = list()

            LOG.info("Created connection to {}:{}.".format(host, port))
        return None

    def close(self):
        """
        Sends the ``quit`` command and closes the telnet connection.
        """
        if self._telnet_conn is not None:
            try:
                self._telnet_conn.write(b"quit\n\r")
            finally:
                self._telnet_conn.close()
                self._telnet_conn = None
                self._telnet_queue = None

                del self._event_queue[:]
                self._num_pending_queries = 0

                LOG.debug("Disconnected client.")
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

            ts3conn.query("servernotifyregister", event="server").exec()
            while True:
                ts3conn.send_keepalive()
                try:
                    event = ts3conn.wait_for_event(timeout=540)
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
        Sends an empty query to the query service in order to prevent automatic
        disconnect. Make sure to call it at least once in 10 minutes.
        """
        self._telnet_conn.write(b"\n\r")
        return None

    def exec_(self, cmd, *options, **params):
        """
        Sends a command to the TS3 server and returns the response. Check out the :meth:`query`
        method if you want to make use of pipelining and more control.

        .. code-block:: python

            # use sid=1
            ts3conn.exec_("use", sid=1)

            # clientlist -uid -away -groups
            resp = ts3conn.exec_("clientlist", "uid", "away", "groups")

        :arg str cmd:
            A TS3 command
        :arg options:
            The options of a command without a leading minus,
            e.g. ``'uid'``, ``'away'``.
        :arg params:
            Some parameters (key, value pairs) which modify the
            command, e.g. ``sid=1``.

        :rtype: TS3QueryResponse
        :returns:
            A object which contains all information about the response.

        :seealso: :meth:`wait_for_resp`
        :versionadded: 2.0.0
        """
        q = self.query(cmd, *options, **params)
        return q.fetch()

    def query(self, cmd, *options, **params):
        """
        .. note::

            The :meth:`query` method is great if you want to **fetch** data
            from the server or want to **pipeline** parameters on the same
            command.

            If you are only interested in getting the command executed, then
            you are probably better off using :meth:`exec_`.

        Returns a new :class:`~ts3.query_builder.TS3QueryBuilder` object with the
        first pipe being initialised with the *options* and *params*::

            # serverlist
            q = ts3conn.query("serverlist")

            # clientlist -uid -away -groups
            q = ts3conn.query("clientlist", "uid", "away", "groups")

            # clientdbfind pattern=ScP
            q = ts3conn.query("clientdbfind", pattern="ScP")

            # clientdbfind pattern=FPMPSC6MXqXq751dX7BKV0JniSo= -uid
            q = ts3conn.query("clientdbfind", "uid", pattern="FPMPSC6MXqXq751dX7BKV0JniSo")

            # clientkick reasonid=5 reasonmsg=Go\saway! clid=1|clid=2|clid=3
            q = ts3conn.query("clientkick", reasonid=5, reasonmsg="Go away!")\\
                .pipe(clid=1).pipe(clid=2).pipe(clid=3)

            # channelmove cid=16 cpid=1 order=0
            q = ts3conn.query("channelmove", cid=16, cpid=1, order=0)

            # sendtextmessage targetmode=2 target=12 msg=Hello\sWorld!
            q = ts3conn.query("sendtextmessage", targetmode=2, target=12, msg="Hello World!")

        Queries are **executed** once the
        :meth:`~ts3.query_builder.TS3QueryBuilder.fetch`,
        :meth:`~ts3.query_builder.TS3QueryBuilder.first`
        or :meth:`~ts3.query_builder.TS3QueryBuilder.all` is invoked::

            # Returns a TS3Response object.
            resp = q.fetch()

            # Returns the first item in the response or *None*.
            resp = q.first()

            # Returns a list with all items in the response rather
            # than a TS3Response object.
            resp = q.all()

        :arg options:
            All initial options in the first pipe.
        :arg params:
            All initial parameters (key value pairs) in the first pipe.

        :rtype: TS3QueryBuilder
        :returns:
            A query builder initialised with the *options* and *params*.

        :versionadded: 2.0.0
        """
        if cmd not in self.COMMAND_SET:
            raise TS3InvalidCommandError(cmd, self.COMMAND_SET)
        return TS3QueryBuilder(ts3conn=self, cmd=cmd).pipe(*options, **params)

    def exec_query(self, query, timeout=None):
        """
        Sends the *query* to the server, waits and returns for the response.

        :arg TS3QueryBuilder query:
            The query which should be executed.

        :rtype: TS3QueryResponse
        :returns:
            A object which contains all information about the response.

        :seealso: :meth:`wait_for_resp`
        :versionadded: 2.0.0
        """
        q = query.compile()
        LOG.debug("Sending query: '%s'.", q)

        q = q.encode()
        self._telnet_conn.write(q)

        # To identify the response when we receive it.
        self._num_pending_queries += 1
        return self._wait_for_resp(timeout=timeout)


class TS3ServerConnection(TS3BaseConnection):
    """
    Use this class to connect to a **TS3 Server**::

        with TS3ServerConnection("localhost") as tsconn:
            ts3conn.exec_("login", client_login_name="serveradmin", client_login_password="MyStupidPassword")
            ts3conn.exec_("use")
            ts3conn.exec_("clientkick", clid=1)

            resp = ts3conn.query("serverlist").all()
    """

    #: The default port of the server query service.
    DEFAULT_PORT = 10011

    #: The typical TS3 Server greeting::
    #:
    #:      b'TS3\n\r'
    #:      b'Welcome to the [...] on a specific command.\n\r'
    GREETING_LENGTH = 2

    #: All server query commands as returned by the *help* command,
    #: excluding *quit*. Use :meth:`close` instead.
    COMMAND_SET = frozenset([
        "help",
        "login",
        "logout",
        "version",
        "hostinfo",
        "instanceinfo",
        "instanceedit",
        "bindinglist",
        "use",
        "serverlist",
        "serveridgetbyport",
        "serverdelete",
        "servercreate",
        "serverstart",
        "serverstop",
        "serverprocessstop",
        "serverinfo",
        "serverrequestconnectioninfo",
        "servertemppasswordadd",
        "servertemppassworddel",
        "servertemppasswordlist",
        "serveredit",
        "servergrouplist",
        "servergroupadd",
        "servergroupdel",
        "servergroupcopy",
        "servergrouprename",
        "servergrouppermlist",
        "servergroupaddperm",
        "servergroupdelperm",
        "servergroupaddclient",
        "servergroupdelclient",
        "servergroupclientlist",
        "servergroupsbyclientid",
        "servergroupautoaddperm",
        "servergroupautodelperm",
        "serversnapshotcreate",
        "serversnapshotdeploy",
        "servernotifyregister",
        "servernotifyunregister",
        "sendtextmessage",
        "logview",
        "logadd",
        "gm",
        "channellist",
        "channelinfo",
        "channelfind",
        "channelmove",
        "channelcreate",
        "channeldelete",
        "channeledit",
        "channelgrouplist",
        "channelgroupadd",
        "channelgroupdel",
        "channelgroupcopy",
        "channelgrouprename",
        "channelgroupaddperm",
        "channelgrouppermlist",
        "channelgroupdelperm",
        "channelgroupclientlist",
        "setclientchannelgroup",
        "channelpermlist",
        "channeladdperm",
        "channeldelperm",
        "clientlist",
        "clientinfo",
        "clientfind",
        "clientedit",
        "clientdblist",
        "clientdbinfo",
        "clientdbfind",
        "clientdbedit",
        "clientdbdelete",
        "clientgetids",
        "clientgetdbidfromuid",
        "clientgetnamefromuid",
        "clientgetnamefromdbid",
        "clientsetserverquerylogin",
        "clientupdate",
        "clientmove",
        "clientkick",
        "clientpoke",
        "clientpermlist",
        "clientaddperm",
        "clientdelperm",
        "channelclientpermlist",
        "channelclientaddperm",
        "channelclientdelperm",
        "permissionlist",
        "permidgetbyname",
        "permoverview",
        "permget",
        "permfind",
        "permreset",
        "privilegekeylist",
        "privilegekeyadd",
        "privilegekeydelete",
        "privilegekeyuse",
        "messagelist",
        "messageadd",
        "messagedel",
        "messageget",
        "messageupdateflag",
        "complainlist",
        "complainadd",
        "complaindelall",
        "complaindel",
        "banclient",
        "banlist",
        "banadd",
        "bandel",
        "bandelall",
        "ftinitupload",
        "ftinitdownload",
        "ftlist",
        "ftgetfilelist",
        "ftgetfileinfo",
        "ftstop",
        "ftdeletefile",
        "ftcreatedir",
        "ftrenamefile",
        "customsearch",
        "custominfo",
        "whoami"
    ])


class TS3ClientConnection(TS3BaseConnection):
    """
    Use this class if you want to connect to a **TS3 Client**::

        with TS3ClientConnection("localhost") as tsconn:
            ts3conn.exec_("auth", apikey="AAAA-BBBB-CCCC-DDDD-EEEE")
            ts3conn.exec_("use")
    """

    #: The default port of the server query service.
    DEFAULT_PORT = 25639

    #: The typical TS3 Server greeting::
    #:
    #:      b'TS3 Client\n\r'
    #:      b'Welcome to the TeamSpeak 3 ClientQuery interface [...].\n\r'
    #:      b'Use the "auth" command to authenticate yourself. [...].\n\r'
    #:      b'selected schandlerid=1\n\r'
    GREETING_LENGTH = 4

    #: All client query commands as returned by the *help* command,
    #: excluding *quit*. Use :meth:`close` instead.
    COMMAND_SET = frozenset([
        "help",
        "quit",
        "use",
        "auth",
        "banadd",
        "banclient",
        "bandelall",
        "bandel",
        "banlist",
        "channeladdperm",
        "channelclientaddperm",
        "channelclientdelperm",
        "channelclientlist",
        "channelclientpermlist",
        "channelconnectinfo",
        "channelcreate",
        "channeldelete",
        "channeldelperm",
        "channeledit",
        "channelgroupadd",
        "channelgroupaddperm",
        "channelgroupclientlist",
        "channelgroupdel",
        "channelgroupdelperm",
        "channelgrouplist",
        "channelgrouppermlist",
        "channellist",
        "channelmove",
        "channelpermlist",
        "channelvariable",
        "clientaddperm",
        "clientdbdelete",
        "clientdbedit",
        "clientdblist",
        "clientdelperm",
        "clientgetdbidfromuid",
        "clientgetids",
        "clientgetnamefromdbid",
        "clientgetnamefromuid",
        "clientgetuidfromclid",
        "clientkick",
        "clientlist",
        "clientmove",
        "clientmute",
        "clientunmute",
        "clientnotifyregister",
        "clientnotifyunregister",
        "clientpermlist",
        "clientpoke",
        "clientupdate",
        "clientvariable",
        "complainadd",
        "complaindelall",
        "complaindel",
        "complainlist",
        "currentschandlerid",
        "ftcreatedir",
        "ftdeletefile",
        "ftgetfileinfo",
        "ftgetfilelist",
        "ftinitdownload",
        "ftinitupload",
        "ftlist",
        "ftrenamefile",
        "ftstop",
        "hashpassword",
        "messageadd",
        "messagedel",
        "messageget",
        "messagelist",
        "messageupdateflag",
        "permoverview",
        "sendtextmessage",
        "serverconnectinfo",
        "serverconnectionhandlerlist",
        "servergroupaddclient",
        "servergroupadd",
        "servergroupaddperm",
        "servergroupclientlist",
        "servergroupdelclient",
        "servergroupdel",
        "servergroupdelperm",
        "servergrouplist",
        "servergrouppermlist",
        "servergroupsbyclientid",
        "servervariable",
        "setclientchannelgroup",
        "tokenadd",
        "tokendelete",
        "tokenlist",
        "tokenuse",
        "verifychannelpassword",
        "verifyserverpassword",
        "whoami"
    ])
