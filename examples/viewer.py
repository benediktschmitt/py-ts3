#!/usr/bin/python3


# Modules
# ------------------------------------------------
import sys
sys.path.insert(1,"../")

import ts3
from pprint import pprint


# Functions
# ------------------------------------------------

class ChannelTree(object):
    """
    Note, that the used algorithms and data structures are not very efficient,
    but it works.
    """

    def __init__(self, channel):
        self.childs = list()
        self.root = None
        return None

    def is_child(self, channel)


def is_child(channel, tree):
    """
    Returns true, if the channel is a child of any other channel in the tree.
    """
    if not tree:
        return False
    elif channel["pid"] == tree[0]["cid"]:
        return True
    else:
        for sub_tree in tree[1]:
            if is_child(chanel, sub_tree):
                return True
        return False

                  
def insert_channel(channel, tree):
    """
    Builds a tree of the channel.
    """
    if not tree:
        return [cha
    

          
def view(ts3conn):
    """
    Prints a list with the channel tree and the clients in the channels.
    """
    ts3conn.channellist()
    channellist = ts3conn.last_resp.parsed

    ts3conn.clientlist()
    clientlist = ts3conn.last_resp.parsed

    tree = build_channel_tree(channellist)
    

# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from _def_param import *
    
    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(USER, PASS)
        ts3conn.use(SID)
        view(ts3conn)

