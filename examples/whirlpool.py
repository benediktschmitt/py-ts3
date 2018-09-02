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


# Modules
# ------------------------------------------------
import time
import random
import ts3
import ts3.definitions


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
            targetmode=ts3.definitions.TextMessageTargetMode.SERVER,
            target=0, msg="Whirpool in {}s".format(i))
        time.sleep(1)

    # Fetch the clientlist and the channellist.
    clientlist = ts3conn.clientlist()
    channellist = ts3conn.channellist()

    # Ignore query clients
    clientlist = [client for client in clientlist \
                  if client["client_type"] != "1"]

    # Whirpool with one channel or no users is boring.
    if len(channellist) == 1 or not clientlist:
        return None

    # We need this try-final construct to make sure, that all
    # clients will be in the same channel at the end of the
    # whirlpool as to the beginning.
    try:
        end_time = time.time() + duration
        while end_time > time.time():
            for client in clientlist:
                clid = client["clid"]
                cid = random.choice(channellist)["cid"]
                try:
                    ts3conn.clientmove(clid=clid, cid=cid)
                except ts3.query.TS3QueryError as err:
                    # Only ignore 'already member of channel error'
                    if err.resp.error["id"] != "770":
                        raise
            time.sleep(relax_time)
    finally:
        # Move all clients back
        for client in clientlist:
            try:
                ts3conn.clientmove(clid=client["clid"], cid=client["cid"])
            except ts3.query.TS3QueryError as err:
                if err.resp.error["id"] != "770":
                    raise
    return None


# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from def_param import *

    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        whirlpool(ts3conn)
