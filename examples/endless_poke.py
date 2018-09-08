#!/usr/bin/env python3

import time
import ts3

# Telnet or SSH ?
URI = "ssh://serveradmin:Z0YxRb7u@localhost:10022"
URI = "telnet://serveradmin:Z0YxRb7u@localhost:10011"

SID = 1


def endless_poke(ts3conn, nickname, msg=None, num=100, delay=1):
    """
    Pokes all clients where *nickname* matches *num* times with the message
    *msg*. Sleeping *delay* seconds between the single pokes. If *num* is -1,
    the client is poked forever.
    """
    if msg is None:
        msg = "Stop annoying me!"

    # Get the client ids
    clients = ts3conn.query("clientfind", pattern=nickname).all()
    clients = [client["clid"] for client in clients]

    # Break, if there's no client.
    if not clients:
        return None

    # Poke them
    i = 0
    while num == -1 or i < num:
        for clid in clients:
            ts3conn.exec_("clientpoke", msg=msg, clid=clid)
        time.sleep(delay)
    return None


if __name__ == "__main__":
    with ts3.query.TS3ServerConnection(URI) as ts3conn:
        ts3conn.exec_("use", sid=SID)
        endless_poke(ts3conn, "Ben", delay=0.25)
