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
import warnings
from urllib.parse import urlparse

# third party
import paramiko

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
    "TS3TransportError",
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


class TS3TransportError(TS3Error):
    """
    Raised if something goes wrong on the transport level, e.g. a connection
    cannot be established or has already been closed.

    :seealso: :class:`TS3Transport`
    """


def running_timeout(timeout):
    """Helper to enforce a 'global' timeout::

        timeout = running_timeout(timeout)
        while True:
            line = conn.recv(timeout())

    :raises TS3TimeoutError:
    """
    start = time.time()

    def remaining():
        """Returns the remaining time until *timeout* seconds have passed."""
        if timeout is None:
            return None

        dt = time.time() - start
        if dt > timeout:
            raise TS3TimeoutError()
        return timeout - dt
    return remaining


class TS3Transport(object):
    """
    The TS3 server supports the *telnet* and *ssh* protocols. This class defines
    an abstract interface which is used by the :class:`TS3BaseConnection` to
    perform requests.

    TS3Transport instances are used for **exactly one connection**.

    .. note::

        The transport adapter is only used internally and not part of the
        public API.
    """

    def connect(self, host, port, timeout, **kargs):
        """
        Connect to the TS3 query service at the specificed address (host, port).

        :raises TS3TimeoutError:
        :raises TS3TransportError:
        """
        raise NotImplementedError()

    def close(self):
        """Closes the connection, never fails."""
        raise NotImplementedError()

    def read_line(self, timeout):
        """
        Blocks until a line has been received (delimted by ``b\n\r``) or the
        timeout expired.

        :raises TS3TimeoutError:
        :raises TS3TransportError:
        """
        raise NotImplementedError()

    def send_line(self, data):
        """
        Send a line of data to the TS3 query service. The delimiter is added
        automatic.

        :raises TS3TransportError:
        """
        raise NotImplementedError()


class TS3TelnetTransport(TS3Transport):
    """An adapter for the telnet protocol using :class:`telnetlib.Telnet`."""

    def fileno(self):
        return self._conn.fileno()

    def connect(self, host, port, timeout, **kargs):
        try:
            self._conn = telnetlib.Telnet(host, port, timeout)
        except OSError as err:
            raise TS3TransportError() from err
        except TimeoutError as err:
            raise TS3TimeoutError() from err
        return None

    def close(self):
        self._conn.close()
        return None

    def read_line(self, timeout):
        try:
            return self._conn.read_until(b"\n\r", timeout=timeout)
        except (EOFError, OSError) as err:
            raise TS3TransportError() from err

    def send_line(self, data):
        try:
            return self._conn.write(data + b"\n\r")
        except OSError as err:
            raise TS3TransportError() from err


class TS3SSHTransport(TS3Transport):
    """An adapter for the SSH protocol using :class:`paramiko.SSHClient`."""

    def fileno(self):
        return self._channel.fileno()

    def connect(self, host, port, timeout, **kargs):
        client = paramiko.SSHClient()

        # Load the host key and warn if not provided.
        if "host_key" in kargs:
            client.load_host_keys(kargs["host_key"])
        elif kargs.get("load_system_host_keys", False):
            client.load_system_host_keys()
        else:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            warnings.warn(
                "You should provide a 'host_key' to improve security "\
                "or set 'load_system_host_keys' to true.",
                 Warning
            )

        client.connect(
            host, port=port,
            username=kargs["username"], password=kargs["password"]
        )

        self._client = client
        self._channel = client.invoke_shell("raw")
        self._rbuffer = b""
        return None

    def close(self):
        self._client.close()
        return None

    def read_line(self, timeout):
        timeout = running_timeout(timeout)
        delimiter = b"\n\r"

        # Wait until the delimiter can be found in the line buffer.
        while True:
            eol = self._rbuffer.find(delimiter)
            if eol != -1:
                break

            self._channel.settimeout(timeout())
            try:
                self._rbuffer += self._channel.recv(4096)
            except socket.timeout as err:
                raise TS3TimeoutError() from err

        # include the delimiter
        eol += len(delimiter)
        line, self._rbuffer = self._rbuffer[:eol], self._rbuffer[eol:]
        return line

    def send_line(self, data):
        self._channel.send(data + b"\n\r")
        return None


class TS3BaseConnection(object):
    """
    The TS3 query client.

    This class provides only the methods to **handle** the connection to a
    TeamSpeak 3 query service. For a more convenient interface, use the
    :class:`TS3ServerConnection` or :class:`TS3ClientConnection` class.

    Note, that this class supports the *with* statement::

        with TS3BaseConnection("ssh://serveradmin:Z0YxRb7u@localhost:10022") as ts3conn:
            ts3conn.exec_("use", sid=1)

        # You can also use an equal try-finally construct.
        ts3conn = TS3BaseConnection()
        try:
            ts3conn.open_uri("telnet://serveradmin:Z0YxRb7u@localhost:10011")
            ts3conn.exec_("use", sid=1)
        finally:
            ts3conn.close()

    .. warning::

        *   This class is **not thread safe**.
        *   Do **not reuse** already connected instances.

    .. versionchanged:: 2.0.0

        *   The *send()* method has been removed, use :meth:`exec_`,
            :meth:`query` instead.
        *   SSH support
        *   The :meth:`open_uri` method.
    """

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

    def __init__(self, uri=None, tp_args=None):
        """
        If *host* and *port* are provided, the connection will be established
        before the constructor returns.

        .. seealso:: :meth:`open`
        """
        self._transport = None

        # A buffer for the lines in a query response.
        self._resp_buffer = None

        # The number of queries for which we have not received a response yet.
        self._num_pending_queries = 0

        # The undelivered events. These events are returned, the next time
        # *wait_for_event()* is called.
        self._event_queue = list()

        #: The hostname of the query service to which this client is connected.
        self._host = None

        if uri is not None:
            self.open_uri(uri, tp_args=tp_args)
        return None

    # *Simple* get and set methods
    # ------------------------------------------------

    def is_connected(self):
        """
        :return:
            True, if the client is currently connected.
        :rtype:
            bool
        """
        return self._transport is not None

    @property
    def host(self):
        """The hostname of the host of the query service."""
        return self._host

    # Networking
    # ------------------------------------------------

    def open(self, host, port, timeout=None, protocol="telnet", tp_args=None):
        """
        Connect to the TS3 query service.

        .. code-block:: python

            # Connect using telnet.
            ts3conn.open("localhost", 10011)

            # Connect using ssh.
            ts3conn.open("localhost", 10022, protocol="ssh", tp_args={
                "username": "serveradmin", "password": "123456"
            })

        :arg str host:
            The hostname
        :arg int port:
            The listening port of the service.
        :arg int timeout:
            If not *None*, an exception is raised if the connection cannot be
            established within *timeout* seconds.
        :arg str protocol:
            The protocol to be used. The TS3 server supports *ssh* and *telnet*,
            while the client only supports *telnet*.
        :arg dict tp_args:
            A dictionary with parameters that are passed to the
            :meth:`~TS3Transport.connect` method of the used transport. The
            SSH protocol for example requires a *username* and *password*.

        :raises TS3TransportError:
            If the client is already connected or the connection cannot be
            established.
        :raises TS3TimeoutError:
            If the connection cannot be established within the specified
            *timeout*.

        :seealso: :meth:`open_uri`
        """
        if self.is_connected():
            raise TS3TransportError("Already connected.")

        # Choose the transport adapter.
        if protocol == "telnet":
            tp = TS3TelnetTransport()
        elif protocol == "ssh":
            tp = TS3SSHTransport()
        else:
            raise ValueError("The protocol must be 'ssh' or 'telnet'.")

        # Conenct to the query service.
        tp_args = tp_args or dict()
        tp.connect(host, port, timeout, **tp_args)

        # Skip the greeting.
        for i in range(self.GREETING_LENGTH):
            tp.read_line(timeout=timeout)

        self._transport = tp
        self._num_pending_queries = 0
        self._resp_buffer = list()
        self._event_queue = list()
        self._host = host

        LOG.info("Created connection to {}:{}.".format(host, port))
        return self

    def open_uri(self, uri, timeout=None, tp_args=None):
        """
        The same as :meth:`open`, but the host, port, username, password, ...
        are encoded compact in a URI.

        .. code-block:: python

            >>> ts3conn.open_uri("telnet://my.server.com:10011")
            >>> ts3conn.open_uri("ssh://serveradmin@123456@my.server.com:10022")
        """
        p = urlparse(uri)
        host = p.hostname
        port = p.port
        protocol = p.scheme

        tp_args = tp_args or dict()
        tp_args["username"] = p.username
        tp_args["password"] = p.password
        return self.open(host, port, timeout, protocol, tp_args)

    def close(self, timeout=None):
        """
        Sends the ``quit`` command and closes the telnet connection.
        """
        if self.is_connected():
            try:
                self._transport.close()
            finally:
                self._transport = None
                self._num_pending_queries = 0
                self._resp_buffer = list()
                self._event_queue = list()
                self._host = None

                LOG.debug("Disconnected client.")
        return None

    def fileno(self):
        """
        :return:
            The fileno() of the socket object used internally.
        :rtype:
            int
        """
        return self._transport.fileno()

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
        timeout = running_timeout(timeout)

        while True:
            try:
                data = self._transport.read_line(timeout=timeout())
            # Catch socket and telnet errors
            except TS3TransportError as err:
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
                    self._resp_buffer.append(data)
                    data = b"".join(self._resp_buffer)
                    self._resp_buffer = list()

                    resp = TS3QueryResponse(data)
                    self._num_pending_queries -= 1
                    return resp
                else:
                    self._resp_buffer.append(data)
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
        timeout = running_timeout(timeout)
        while not self._event_queue:
            self._recv(timeout=timeout())
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

        timeout = running_timeout(timeout)
        while True:
            resp = self._recv(timeout=timeout())
            if isinstance(resp, TS3QueryResponse):
                break

        if resp.error["id"] != "0":
            raise TS3QueryError(resp)
        return resp

    # Sending
    # -------------------------

    def send_keepalive(self):
        """
        Sends an empty query to the query service in order to prevent automatic
        disconnect. Make sure to call it at least once in 5 minutes.
        """
        self.exec_("version")
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
        self._transport.send_line(q)

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

    def open(self, host, port, timeout=None, protocol="telnet", tp_args=None):
        super().open(host, port, timeout, protocol, tp_args)

        # Try to log in. Only SSH requires authentication during the connection
        # handshake.
        username = tp_args.get("username")
        password = tp_args.get("password")
        if username and password:
            self.exec_(
                "login", client_login_name=username,
                client_login_password=password
            )
            LOG.info("Logged in as '%s'.", username)
        return None


class TS3ClientConnection(TS3BaseConnection):
    """
    Use this class if you want to connect to a **TS3 Client**::

        with TS3ClientConnection("localhost") as tsconn:
            ts3conn.exec_("auth", apikey="AAAA-BBBB-CCCC-DDDD-EEEE")
            ts3conn.exec_("use")
    """

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
