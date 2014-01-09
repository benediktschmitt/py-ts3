#!/usr/bin/python3


# Modules
# ------------------------------------------------
import time
import random

# local
import ts3
import ts3.definitions as ts3def


# Data
# ------------------------------------------------
__all__ = ["whirlpool"]


# Functions
# ------------------------------------------------
def whirlpool(ts3conn, duration=10, relax_time=0.5):
    """
    Moves all clients randomly in other channels for *duration* seconds.
    After the whirpool event, all clients will be in the same channel as
    before. Between the whirlpool cycles, the programm will sleep for
    *relax_time* seconds.
    """
    # Countdown till whirlpool
    for i in range(5, 0, -1):
        ts3conn.sendtextmessage(
            targetmode=ts3def.TextMessageTargetMode.SERVER,
            target=0, msg="Whirpool in {}s".format(i))
        time.sleep(1)

    # Fetch the clientlist and the channellist.
    ts3conn.clientlist()
    clientlist = ts3conn.last_resp.parsed

    ts3conn.channellist()
    channellist = ts3conn.last_resp.parsed

    # Whirpool with one channel is boring.
    if len(channellist) == 1:
        return None

    end_time = time.time() + duration
    while end_time > time.time():
        for client in clientlist:
            clid = client["clid"]
            cid = random.choice(channellist)["cid"]
            ts3conn.clientmove(clid, cid)
        time.sleep(relax_time)

    # Move all clients back
    for client in clientlist:
        ts3conn.clientmove(client["clid"], client["cid"])
        ts3conn.last_resp
    return None


# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from def_param import *
    
    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(USER, PASS)
        ts3conn.use(SID)
        whirlpool(ts3conn)
