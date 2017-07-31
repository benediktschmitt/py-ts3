.. _changelog:

Changelog
=========

*   **2.0.0**

    *   **added** Support for the TS3 Client Query API

        https://github.com/benediktschmitt/py-ts3/issues/48

    *   **renamed** :class:`TS3Connection` to :class:`TS3ServerConnection`
    *   **added** :class:`TS3ClientConnection`
    *   **renamed** :class:`TS3Commands` to :class:`TS3ServerCommands`
    *   **added** :class:`TS3ClientCommands`
    *   **added** *properties* parameter to :meth:`TS3Connection.send`    

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
