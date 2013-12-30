#!/usr/bin/python3


# Modules
# ------------------------------------------------
import ts3
import time


# Functions
# ------------------------------------------------
def endless_poke(ts3conn, nickname, msg=None, num=100, delay=1):
    """
    Pokes all clients where *nickname* matches *num* times with the message
    *msg*. Sleeping *delay* seconds between the single pokes. If *num* is -1,
    the client is poked till infinity times.
    """
    if msg is None:
        msg = "Stop annoying me!"

    # Get the clients id
    ts3conn.clientfind(nickname)
    clients = ts3conn.last_resp.parsed
    clients = [client["clid"] for client in clients]
    
    # Poke them
    i = 0
    while num == -1 or i < num:
        ts3conn.clientpoke(clients, msg)
        if ts3conn.last_resp.error["id"] != "0":
            print("Error while poking:", ts3conn.last_resp.error["msg"])
            return None
        time.sleep(delay)
    return None


# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from _def_param import *
    
    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(USER, PASS)
        ts3conn.use(SID)
        endless_poke(ts3conn, "GENIUS", msg="Was machst du?", delay=0.25)
