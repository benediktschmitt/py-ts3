#!/usr/bin/env python3

import time
import random
import ts3
from ts3.definitions import TextMessageTargetMode


USER = "serveradmin"
PASS = "JB8ZqxfI"
HOST = "localhost"
PORT = 10011
SID = 1


def whirlpool(ts3conn, duration=10, relax_time=0.5):
    """
    Moves all clients randomly in other channels for *duration* seconds.
    After the whirpool event, all clients will be in the same channel as
    before. Between the whirlpool cycles, the programm will sleep for
    *relax_time* seconds.
    """
    # Countdown till whirlpool
    for i in range(5, 0, -1):
        ts3conn.exec_(
            "sendtextmessage", targetmode=TextMessageTargetMode.SERVER,
            target=0, msg="Whirpool in {}s".format(i)
        )
        time.sleep(1)

    # Fetch the ids of all channels.
    channels = ts3conn.query("channellist").all()
    cids = [channel["cid"] for channel in channels]

    # Fetch the ids of all clients and ignore query clients.
    clients = ts3conn.query("clientlist").all()
    clids = [client["clid"] for client in clients if client["client_type"] != "1"]

    # Whirpool with one channel or no users is boring.
    if len(cids) == 1 or not clids:
        return None

    # Keep track of the current positions,
    # so that we can move all clients back when the whirpool stops.
    old_pos = {client["clid"]: client["cid"] for client in clients}

    # We need this try-final construct to make sure, that all
    # clients will be in the same channel at the end of the
    # whirlpool as to the beginning.
    try:
        end_time = time.time() + duration
        while end_time > time.time():

            # Move clients randomly around and ignore
            # 'already member of channel' errors.
            for clid in clids:
                try:
                    ts3conn.exec_("clientmove", clid=clid, cid=random.choice(cids))
                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "770":
                        raise

            time.sleep(relax_time)
    finally:
        # Move all clients back, this time using *no* pipelining.
        for clid in clids:
            try:
                ts3conn.exec_("clientmove", clid=clid, cid=old_pos[clid])
            except ts3.query.TS3QueryError as err:
                if err.resp.error["id"] != "770":
                    raise
    return None


if __name__ == "__main__":
    with ts3.query.TS3ServerConnection(HOST, PORT) as ts3conn:
        ts3conn.exec_("login", client_login_name=USER, client_login_password=PASS)
        ts3conn.exec_("use", sid=SID)
        whirlpool(ts3conn)
