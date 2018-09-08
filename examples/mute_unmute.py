#!/usr/bin/env python3

import time
import ts3


APIKEY = "C2OL-77SJ-M45X-BZ6E-1PBJ-FE2M"
URI = "telnet://localhost:25639"


def mute_unmute(ts3conn):
    """Mutes the client for 10 seconds using the TS3 Client Query API."""
    ts3conn.exec_("clientupdate", client_input_muted=True, client_output_muted=True)
    time.sleep(10)
    ts3conn.exec_("clientupdate", client_input_muted=False, client_output_muted=False)
    return None


if __name__ == "__main__":
    with ts3.query.TS3ClientConnection(URI) as ts3conn:
        ts3conn.exec_("auth", apikey=APIKEY)
        ts3conn.exec_("use")
        mute_unmute(ts3conn)
