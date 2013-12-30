#!/usr/bin/python3


# Modules
# ------------------------------------------------
import ts3


# Classes
# ------------------------------------------------
class ChannelTree(object):
    """
    Node of a channel tree.
    """

    def __init__(self, channel):
        self.root = channel
        self.childs = list()
        return None

    @classmethod
    def init_node(cls, channel):
        return cls(channel)

    @classmethod
    def init_root(cls, servername=None):
        if servername is None:
            servername = str()
        obj = cls(None)
        obj.servername = servername        
        return obj

    @classmethod
    def build_tree(cls, channellist, servername=None):
        """
        Transforms the channellist in a ChannelTree.
        """
        tree = cls.init_root(servername)
                   
        for channel in channellist:
            ctree = cls.init_node(channel)
            tree.insert(ctree)
        return tree

    def insert(self, ctree):
        """
        Inserts the channel tree *ctree* recursivly in the channel tree.
        Returns true, if the tree has been inserted.
        """
        # We assumed on previous insertions, that a channel is a direct child
        # of the root, if we could not find the parent. Correct this, if ctree
        # is the parent from one of these orpheans
        if self.root is None:
            i = 0
            while i < len(self.childs):
                child = self.childs[i]
                if ctree.root["cid"] == child.root["pid"]:
                    ctree.childs.append(child)
                    self.childs.pop(i)
                else:
                    i += 1

        # We are currently not at the root and the channel is a direct child
        # of this one. We can append it and the work is done.
        elif ctree.root["pid"] == self.root["cid"]:
            self.childs.append(ctree)
            return True

        # Try to insert the ctree now recursive.
        for child in self.childs:
            if child.insert(ctree):
                return True

        # If we could not find a parent in the whole tree, assume, that the
        # channel tree is a child of the root.
        if self.root is None:
            self.childs.append(ctree)
        return False

    def sort_childs(self):
        """
        Sorts the child channels by the channel_order attribute.
        """
        self.childs.sort(key=lambda c: c.root["channel_order"])
        return None

    def print(self, clients=None, indent=0):
        """
        Prints the channel and its subchannels recursive.
        You can provide a dictionary *clients*, that maps the channel id to
        the clients in the channel.
        """
        if self.root is None:
            print(" "*indent + "|-", self.servername)
        else:
            print(" "*indent + "|-", self.root["channel_name"])
            if clients is not None:
                for client in clients[self.root["cid"]]:
                    print(" "*(indent + 3) + "| ", client["client_nickname"])

        self.sort_childs()
        for child in self.childs:
            child.print(clients, indent + 3)
        return None

        
# Functions
# ------------------------------------------------
def view(ts3conn):
    """
    Prints a simple channel tree with the clients.
    """
    # Get the name of the virtual server
    ts3conn.serverinfo()
    serverinfo = ts3conn.last_resp.parsed[0]
    servername = serverinfo["virtualserver_name"]
    
    # Get the channellist
    ts3conn.channellist()
    channellist = ts3conn.last_resp.parsed

    # and the clientlist.
    ts3conn.clientlist()
    clientlist = ts3conn.last_resp.parsed

    # Map the channel id to the clients in the channel.
    channel_to_clients = {channel["cid"]: [client for client in clientlist \
                                           if client["cid"] == channel["cid"]]
                          for channel in channellist}

    # Create the channel tree and print it.    
    channel_tree = ChannelTree.build_tree(channellist, servername)
    channel_tree.print(channel_to_clients)
    return None
    

# Main
# ------------------------------------------------
if __name__ == "__main__":
    # USER, PASS, HOST, ...
    from _def_param import *
    
    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(USER, PASS)
        ts3conn.use(SID)
        view(ts3conn)
