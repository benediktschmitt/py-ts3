#!/usr/bin/env python3

import time
import ts3


USER = "serveradmin"
PASS = "JB8ZqxfI"
HOST = "localhost"
PORT = 10011
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
            # 9 minutes.
            event = ts3conn.wait_for_event(timeout=550)
        except ts3.query.TS3TimeoutError:
            pass
        else:
            # Greet new clients.
            if event[0]["reasonid"] == "0":
                print("Client '{}' connected.".format(event[0]["client_nickname"]))
                ts3conn.exec_("clientpoke", clid=event[0]["clid"], msg=msg)
    return None


if __name__ == "__main__":
    with ts3.query.TS3ServerConnection(HOST, PORT) as ts3conn:
        ts3conn.exec_("login", client_login_name=USER, client_login_password=PASS)
        ts3conn.exec_("use", sid=SID)
        hello_bot(ts3conn)
