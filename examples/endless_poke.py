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
import ts3


# Data
# ------------------------------------------------
__all__ = ["endless_poke"]


# Functions
# ------------------------------------------------
def endless_poke(ts3conn, nickname, msg=None, num=100, delay=1):
    """
    Pokes all clients where *nickname* matches *num* times with the message
    *msg*. Sleeping *delay* seconds between the single pokes. If *num* is -1,
    the client is poked forever.
    """
    if msg is None:
        msg = "Stop annoying me!"

    # Get the client ids
    clients = ts3conn.clientfind(pattern=nickname)
    clients = [client["clid"] for client in clients]

    # Break, if there's no client.
    if not clients:
        return None

    # Poke them
    i = 0
    while num == -1 or i < num:
        for clid in clients:
            ts3conn.clientpoke(msg=msg, clid=clid)
        time.sleep(delay)
    return None


# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from def_param import *

    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        endless_poke(ts3conn, "Ben", delay=0.25)
