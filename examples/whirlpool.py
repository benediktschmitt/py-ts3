#!/usr/bin/python3


# Modules
# ------------------------------------------------
import ts3
import random


# Functions
# ------------------------------------------------
def whirlpool(ts3conn, duration=30, relax_time=0.5):
    """
    Moves all clients randomly in other channels for *duration* seconds.
    After the whirpool event, all clients will be in the same channel as
    before. Between the whirlpool cycles, the programm will sleep for
    *relax_time* seconds.
    """
    # Countdown till whirlpool
    for i in range(5, 0, -1):
        ts3conn.sendtextmessage(
            targetmode=ts3.TextMessageTargetMode.SERVER,
            target=0, msg="Whirpool in {}s".format(i))

    # Fetch the clientlist and the channellist.
    ts3conn.clientlist()
    clientlist = ts3conn.last_response.parsed

    ts3conn.channellist()
    channellist = ts3conn.last_response.parsed

    # Whirpool with one channel is boring.
    if len(channellist) == 1:
        return None

    end_time = time.time() + duration
    while end_time > time.time():
        for client in clientlist:
            clid = client["clid"]
            cid = random.choice(channellist)["cid"]
            ts3conn.clientmove(clid, cid)
            # Todo: Can I remove this ?
            ts3conn.last_response
        time.sleep(relax_time)

    # Move all clients back
    for client in clientlist:
        ts3conn.clientmove(client["clid"], client["cid"])
        # Todo: Can I remove this?
        ts3conn.last_response
    return None


# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from _def_param import *
    
    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(USER, PASS)
        ts3conn.use(SID)
        whirlpool(ts3conn)
