#!/usr/bin/python3

# The MIT License (MIT)
# 
# Copyright (c) 2013 Benedikt Schmitt
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
