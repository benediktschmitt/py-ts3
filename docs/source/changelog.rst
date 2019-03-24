.. _changelog:

Changelog
=========

*   **2.0.0b3**

    *   *changed* :meth:`TS3BaseConnection.send_keepalive` now sends the
        *version* command instead of an empty line.
        (`issue 77 <https://github.com/benediktschmitt/py-ts3/issues/77>`_)
        (`issue 84 <https://github.com/benediktschmitt/py-ts3/issues/84>`_)

*   **2.0.0b2**

    *   **added** SSH support
        (`issue 70 <https://github.com/benediktschmitt/py-ts3/issues/70>`_)
    *   **added** :meth:`TS3BaseConnection.open_uri`
    *   **changed** The constructor of :class:`TS3BaseConnection` accepts now a
        URI instead of a host and port to keep things simple, especially with
        the new SSH parameters.
    *   **fixed** timeout handling
    *   **fixed** error propagation

    **Update Guide**

    .. code-block:: python

        # Old code
        with TS3ServerConnection("localhost") as ts3conn:
            pass

        # New code (1)
        with TS3ServerConnection("telnet://localhost:10011") as ts3conn:
            pass

        # New code (2)
        with TS3ServerConnection("ssh://serveradmin:abc123@localhost:10011") as ts3conn:
            pass

*   **2.0.0b1**

    *   **added** Support for the TS3 Client Query API
        (`issue 48 <https://github.com/benediktschmitt/py-ts3/issues/48>`_)
    *   **renamed** :class:`TS3Connection` to :class:`TS3ServerConnection`
    *   **added** :class:`TS3ClientConnection`
    *   **removed** the monstrous :mod:`commands` module, use :class:`TS3QueryBuilder` instead.
    *   **removed** the :mod:`TS3Escape` class, use the :class:`TS3QueryBuilder` and the
        :func:`escape` and :func:`unescape` functions instead.

    Version 2.0.0 introduces support for the client query API and pipelining
    query commands. This come at the costs and benefits of having a new
    query API.

    **Update Guide**

    .. code-block:: python

        # Old code
        ts3conn.login(client_login_name="serveradmin", client_login_password="abc")
        ts3conn.clientlist(away=True, uid=True)
        ts3conn.clientkick(reasonmsg="Haha.", clid=42)

        # New code
        ts3conn.exec_("login", client_login_name="serveradmin", client_login_password="abc")
        ts3conn.exec_("clientlist", "away", "uid")
        ts3conn.exec_("clientkick", reasonmsg="Haha", clid=42)

        query = ts3conn.query("clientkick", reasonmsg="Haha").pipe(clid=42).pipe(clid=43)
        resp = query.fetch()

    In short:

        #.  The **command** is the first parameter of *exec_()*
        #.  The **options** are simple string arguments after the command.
        #.  The **parameters** are given as keyword arguments.

    **Update or not?**

    Version 1.0.0 is quite stable. If you don't need the client query API or support
    for pipelining, then there is no reason to update, but you should fix the version
    in your *requirements.txt* file.

    If you start a new project, use version 2.0.0. It has only a slightly different
    API but offers more features, while keeping the readability.

*   **1.0.4**

    *   **added** fallbackhost parameter to some TS3FileTransfer methods
    *   **fixed** UnicodeDecodeError caused by Android clients

        https://github.com/benediktschmitt/py-ts3/issues/34

*   **1.0.0**

    All threads have been removed and the event handling has been reworked.
    Please take a look at the examples and the GitHub README for the new
    event queue.

    *   **removed** *TS3ResponseRecvError*

        Use the *TS3TimeoutError* and *TS3RecvError* exceptions now.

    *   **added** *TS3TimeoutError* exception
    *   **added** *TS3RecvError* exception

    *   **removed** *TS3BaseConnection.keepalive()*

        This method has been removed, because of the bad use of threads.
        You are now responsible to sent the *keepalive* message
        by calling *TS3BaseConnection.send_keepalive()* at least once in
        10 minutes.

    *   **added** *TS3BaseConnection.send_keepalive()*
    *   **removed** *TS3BaseConnection.on_event()*

        use the new *TS3BaseConnection.wait_for_event()* now.

    *   **removed** *TS3BaseConnection.wait_for_resp()*

        This method is an inplementation detail.

    *   **removed** *TS3BaseConnection.stop_recv()*

        This method is no longer needed.

    *   **removed** *TS3BaseConnection.recv_in_thread()*

        This method is no longer needed.

    *   **removed** *TS3BaseConnection.last_resp*
