#!/usr/bin/env python3

import time
import ts3


APIKEY = "JCVP-QUME-ZBQJ-N1NZ-6ETL-YCDJ"
HOST = "localhost"
PORT = 25639


def mute_unmute(ts3conn):
    """Mutes the client for 10 seconds using the TS3 Client Query API."""
    ts3conn.exec_("clientupdate", client_input_muted=True, client_output_muted=True)
    time.sleep(10)
    ts3conn.exec_("clientupdate", client_input_muted=False, client_output_muted=False)
    return None


if __name__ == "__main__":
    APIKEY = "JCVP-QUME-ZBQJ-N1NZ-6ETL-YCDJ"

    with ts3.query.TS3ClientConnection(HOST) as ts3conn:
        ts3conn.exec_("auth", apikey=APIKEY)
        ts3conn.exec_("use")
        mute_unmute(ts3conn)
