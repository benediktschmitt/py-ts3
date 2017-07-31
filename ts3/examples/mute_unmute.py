#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2013-2017 Benedikt Schmitt <benedikt@benediktschmitt.de>
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


__all__ = [
    "mute_unmute"
]


def mute_unmute(ts3conn):
    """Mutes the client for 10 seconds."""
    ts3conn.clientupdate(client_input_muted=True, client_output_muted=True)
    time.sleep(10)
    ts3conn.clientupdate(client_input_muted=False, client_output_muted=False)
    return None


if __name__ == "__main__":
    APIKEY = "XUCG-45BE-B80G-RIOO-OGV0-0NM8"
    HOST = "localhost"

    with ts3.query.TS3ClientConnection(HOST) as ts3conn:
        ts3conn.auth(apikey=APIKEY)
        ts3conn.use()
        mute_unmute(ts3conn)
