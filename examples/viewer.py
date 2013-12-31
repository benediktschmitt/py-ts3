#!/usr/bin/python3


# Modules
# ------------------------------------------------
import ts3
from pprint import pprint


# Data
# ------------------------------------------------
__all__ = ["ChannelTreeNode"]


# Classes
# ------------------------------------------------
class ChannelTreeNode(object):
    """
    Represents a channel or the virtual server in the channel tree of a virtual
    server.

    Common
    ------
    
    self.childs = List with the child *Channels*.

    self.root = The *Channel* object, that is the root of the whole channel
                tree.

    Channel
    -------
    
    Represents a real channel.
    
    self.info =  Dictionary with all informations about the channel obtained by
                 ts3conn.channelinfo

    self.parent = The parent channel, represented by another *Channel* object.

    self.clients = List with dictionaries, that contains informations about the
                   clients in this channel.

    Root Channel:
    -------------
    Represents the virtual server itself.

    self.info = Dictionary with all informations about the virtual server
                obtained by ts3conn.serverinfo

    self.parent = None
    
    self.clients = None
    """

    def __init__(self, info, parent, root, clients=None):
        """
        Inits a new channel node.

        If root is None, root is set to *self*.
        """
        self.info = info
        self.childs = list()
        
        # Init a root channel
        if root is None:
            self.parent = None
            self.clients = None
            self.root = self
            
        # Init a real channel
        else:
            self.parent = parent
            self.root = root
            self.clients = clients if clients is not None else list()
        return None
    
    @classmethod
    def init_root(cls, info):
        """
        Creates a the root node of a channel tree.
        """
        return cls(info, None, None, None)

    def is_root(self):
        """
        Returns true, if this node is the root of a channel tree (the virtual
        server).
        """
        return self.parent is None

    def is_channel(self):
        """
        Returns true, if this node represents a real channel.
        """
        return self.parent is not None

    @classmethod
    def build_tree(cls, ts3conn, sid):
        """
        Returns the channel tree from the virtual server identified with
        *sid*, using the *TS3Connection* ts3conn.
        """
        ts3conn.use(sid, virtual=True)

        ts3conn.serverinfo()
        serverinfo = ts3conn.last_resp.parsed[0]
        
        ts3conn.channellist()
        channellist = ts3conn.last_resp.parsed

        ts3conn.clientlist()
        clientlist = ts3conn.last_resp.parsed
        # channel id -> clients
        clientlist = {cid: [client for client in clientlist \
                            if client["cid"] == cid]
                      for cid in map(lambda e: e["cid"], channellist)}

        root = cls.init_root(serverinfo)
        for channel in channellist:
            ts3conn.channelinfo(channel["cid"])
            channelinfo = ts3conn.last_resp.parsed[0]
            # This makes sure, that *cid* is in the dictionary.
            channelinfo.update(channel)
            
            channel = cls(
                info=channelinfo, parent=root, root=root,
                clients=clientlist[channel["cid"]])
            root.insert(channel)

        root.sort()
        return root

    def insert(self, channel):
        """
        Inserts the channel in the tree.
        """
        self.root._insert(channel)
        return None

    def _insert(self, channel):
        """
        Inserts the channel recursivly in the channel tree.
        Returns true, if the tree has been inserted.
        """
        # We assumed on previous insertions, that a channel is a direct child
        # of the root, if we could not find the parent. Correct this, if ctree
        # is the parent from one of these orpheans.
        if self.is_root():
            i = 0
            while i < len(self.childs):
                child = self.childs[i]
                if channel.info["cid"] == child.info["pid"]:
                    channel.childs.append(child)
                    self.childs.pop(i)
                else:
                    i += 1

        # This is not the root and the channel is a direct child of this one. 
        elif channel.info["pid"] == self.info["cid"]:
            self.childs.append(channel)
            return True

        # Try to insert the channel recursive.
        for child in self.childs:
            if child._insert(channel):
                return True

        # If we could not find a parent in the whole tree, assume, that the
        # channel is a child of the root.
        if self.is_root():
            self.childs.append(channel)
        return False

    def sort(self):
        """
        Sorts the channels in the tree recursive using the *channel_order*
        attribute.
        
        XXX: This method does not work correct, so exit.
        """
##        self.childs.sort(key=lambda c: int(c.info["channel_order"]))
##        for child in self.childs:
##            child.sort()
        return None

    def print(self, indent=0, restore_order=False):
        """
        Prints the channel and it's subchannels recursive. If restore_order is
        true, the child channels will be sorted before printing them.
        """
        if restore_order:
            self.sort()
            
        if self.is_root():
            print(" "*(indent*3) + "|-", self.info["virtualserver_name"])
        else:
            print(" "*(indent*3) + "|-", self.info["channel_name"])
            for client in self.clients:
                # Ignore query clients
                if client["client_type"] == "1":
                    continue
                print(" "*(indent*3+3) + "->", client["client_nickname"])

        for child in self.childs:
            child.print(indent=indent + 1)
        return None

    
# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from _def_param import *
    
    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(USER, PASS)

        tree = ChannelTreeNode.build_tree(ts3conn, 1)
        tree.print()
