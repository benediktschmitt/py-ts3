#!/usr/bin/env python3

"""
This script uploads an XKCD comic to the default channel and downloads it again.
"""

import time
import webbrowser
import ts3

# Telnet or SSH ?
URI = "telnet://serveradmin:Z0YxRb7u@localhost:10011"
URI = "ssh://serveradmin:Z0YxRb7u@localhost:10022"

SID = 1


with ts3.query.TS3ServerConnection(URI) as ts3conn:
    ts3conn.exec_("use", sid=SID)

    # Get the default channel.
    resp = ts3conn.query("channellist").options("flags").all()
    cid = [item["cid"] for item in resp if item["channel_flag_default"] == "1"]
    cid = cid[0]

    # Use the convenient high-level API provided by py-ts3.
    ts3ft = ts3.filetransfer.TS3FileTransfer(ts3conn)

    # Upload the comic.
    with open("./xkcd_python.png", "rb") as file:
        ts3ft.init_upload(input_file=file, name="/comic.png", cid=cid)
    print("upload complete.")

    # Download the comic.
    with open("./xkcd_python_(copy).png", "wb") as file:
        ts3ft.init_download(output_file=file, name="/comic.png", cid=cid)
    print("download complete.")

    # Display the downloaded file.
    webbrowser.open("./xkcd_python_(copy).png")
