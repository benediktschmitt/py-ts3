#!/usr/bin/python3
# Benedikt Schmitt <benedikt@benediktschmitt.de>


# Modules
# ------------------------------------------------
import time
import random
from pprint import pprint

# local
import query
import definitions


# Data
# ------------------------------------------------
# Login data
USER = "serveradmin"
PASS = "8PFedd2R"
# The virtualserver used for the commands
VS_ID = 1


# Functions
# ------------------------------------------------
def kick_inactive_clients(timeout=60, msg=None):
    """
    Kicks all clients from the server, that are longer than
    *timeout* seconds inactive.
    """
    if msg is None:
        msg = "You've been too long inactive."
        
    with query.TS3Connection("localhost") as ts3conn:
        ts3conn.send(
            "login", {"client_login_name": "serveradmin",
                      "client_login_password": "8PFedd2R"
                      }
            )
        if ts3conn.last_response.error["id"] != "0":
            print("login failed:", ts3conn.last_response.error["msg"])
            return None

        # Continue, if the login was successful.
        print("login successful")

        # Get the whole clients list.
        ts3conn.send("use {}".format(VS_ID))
        ts3conn.send("clientlist", options=["info"])
        clientlist = ts3conn.last_response.parsed        
        for client in clientlist:
            # Get more information about the client.
            ts3conn.send("clientinfo", {"clid": client["clid"]})
            client_info = ts3conn.last_response.parsed[0]

            # Kick the client, if necessairy.
            idle_time = int(client_info["client_idle_time"])
            idle_time /= 1000
            if idle_time > timeout:
                print("{} has been too long inactive."\
                      .format(client_info["client_nickname"]))
                ts3conn.send(
                    "clientkick",
                    {"clid": client["clid"],
                     "reasonid": definitions.ReasonIdentifier.KICK_SERVER,
                     "reasonmsg": msg}
                    )
    return None


def whirlpool(duration=30):
    """
    Moves all clients randomly in other channels for *duration* seconds.
    """
    with query.TS3Connection("localhost") as ts3conn:
        ts3conn.send(
            "login", {"client_login_name": "serveradmin",
                      "client_login_password": "8PFedd2R"
                      }
            )
        if ts3conn.last_response.error["id"] != "0":
            print("login failed:", ts3conn.last_response.error["msg"])
            return None

        # Continue, if the login was successful.
        print("login successful")

        # Get the whole clients list.
        ts3conn.send("use {}".format(VS_ID))

        # Print a countdown.
        for i in range(5, 0, -1):
            ts3conn.send(
                "sendtextmessage",
                {"targetmode": definitions.TextMessageTargetMode.SERVER,
                 "target": 0,
                 "msg": "Whirpool in {}s".format(i)
                 })
            time.sleep(1)

        # Start doing stupid things...
        ts3conn.send("clientlist", options=["info"])
        clientlist = ts3conn.last_response.parsed

        ts3conn.send("channellist")
        channellist = ts3conn.last_response.parsed

        # Whirpool with one channel is boring.
        if len(channellist) == 1:
            return None
        
        pprint(clientlist)
        pprint(channellist)
        end_time = time.time() + duration
        while end_time > time.time():
            for client in clientlist:
                ts3conn.send(
                    "clientmove",
                    {"clid": client["clid"],
                     "cid": random.choice(channellist)["cid"]
                     })
                ts3conn.last_response
            time.sleep(0.5)

        # Move all clients back
        for client in clientlist:
            ts3conn.send(
                "clientmove",
                {"clid": client["clid"],
                 "cid": client["cid"]
                 })
            ts3conn.last_response
    return None


def annoying_foo(nickname, msg=None, num=100, delay=1):
    """
    Pokes the client with the *nickname* *num* times with the message *msg*.
    Sleeping *delay* seconds between the single pokes.
    """
    if msg is None:
        msg = "Stop annoying me!"
        
    with query.TS3Connection("localhost") as ts3conn:
        ts3conn.send(
            "login", {"client_login_name": "serveradmin",
                      "client_login_password": "8PFedd2R"
                      }
            )
        if ts3conn.last_response.error["id"] != "0":
            print("login failed:", ts3conn.last_response.error["msg"])
            return None

        # Continue, if the login was successful.
        print("login successful")

        # Get the clients id
        ts3conn.send("use {}".format(VS_ID))

        ts3conn.send(
            "clientfind",
            {"pattern": nickname})
        clients = ts3conn.last_response.parsed
        if clients:
            clid = clients[0]["clid"]
            for i in range(num):
                ts3conn.send(
                    "clientpoke",
                    {"clid": clid, "msg": msg})
                time.sleep(delay)
        return None

    
# Main
# ------------------------------------------------
if __name__ == "__main__":
##    kick_inactive_clients()
##    whirlpool(3)
    annoying_foo("Ben")
