#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2013-2016 Benedikt Schmitt <benedikt@benediktschmitt.de>
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

import time
import ts3


__all__ = ["hello_bot"]


def hello_bot(ts3conn, msg=None):
    """
    Waits for new clients and says hello to them, when they join the server.
    """
    if msg is None:
        msg = "Hello :)"

    # Register for the event.
    ts3conn.servernotifyregister(event="server")

    while True:
        event = ts3conn.wait_for_event()

        # Greet new clients.
        if event[0]["reasonid"] == "0":
            print("Client '{}' connected.".format(event[0]["client_nickname"]))
            ts3conn.clientpoke(clid=event[0]["clid"], msg=msg)
    return None


if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from def_param import *

    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        hello_bot(ts3conn)
