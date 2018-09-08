#!/usr/bin/env python3

import time
import ts3

# Telnet or SSH ?
URI = "ssh://serveradmin:Z0YxRb7u@localhost:10022"
URI = "telnet://serveradmin:Z0YxRb7u@localhost:10011"

SID = 1


def hello_bot(ts3conn, msg=None):
    """
    Waits for new clients and says hello to them, when they join the server.
    """
    if msg is None:
        msg = "Hello :)"

    # Register for the event.
    ts3conn.exec_("servernotifyregister", event="server")

    while True:
        ts3conn.send_keepalive()

        try:
            # This method blocks, but we must sent the keepalive message at
            # least once in 10 minutes. So we set the timeout parameter to
            # 1 minutes, just to be ultra safe.
            event = ts3conn.wait_for_event(timeout=60)
        except ts3.query.TS3TimeoutError:
            pass
        else:
            # Greet new clients.
            if event[0]["reasonid"] == "0":
                print("Client '{}' connected.".format(event[0]["client_nickname"]))
                ts3conn.exec_("clientpoke", clid=event[0]["clid"], msg=msg)
    return None


if __name__ == "__main__":
    with ts3.query.TS3ServerConnection(URI) as ts3conn:
        ts3conn.exec_("use", sid=SID)
        hello_bot(ts3conn)
