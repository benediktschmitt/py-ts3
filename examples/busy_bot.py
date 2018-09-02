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

import time

import ts3
__all__ = ["Busybot_bot.py"]


def busy_bot(ts3conn, msg=None):
    """
    Sends the busy message each time when the client tries to send a text message to him
    """
    if msg is None:
        msg = "Stop texting me! Im busy!"

    # Register for the event.
    ts3conn.servernotifyregister(event="chat", specifier="composing")

    while True:
        ts3conn.send_keepalive()

        try:
            # This method blocks, but we must sent the keepalive message at
            # least once in 5 minutes to avoid the sever side idle client
            # disconnect. So we set the timeout parameter simply to 1 minute.
            event = ts3conn.wait_for_event(timeout=60)
        except ts3.query.TS3TimeoutError:
            pass
        else:
            if event.event == "notifyclientchatcomposing":
                ts3conn.sendtextmessage(targetmode=1, target=event[0]["clid"], msg=msg)
    return None


if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from def_param import *

    with ts3.query.TS3Connection(HOST, PORT, newline=b"\r\n", motd_line_count=2) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        # For TeaSpeak we have to become visible
        ts3conn.send("join")
        busy_bot(ts3conn)
