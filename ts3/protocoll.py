#!/usr/bin/python3


# Classes
# ------------------------------------------------
class TS3Commands(object):
    """
    Returns the string described in the documentation to execute the command.
    Consider this as the implementation of the protocoll.

    Each method returns:

        return self._return_proxy(str, dict|None, list|None)
        return self._return_proxy(command, parameters, options)

    Example:

        return self._return_proxy("help", None, None)
        return self._return_proxy("use", {"port": 21293}, ["virtual"])
        
    """

    def _return_proxy(self, cmd, params, opt):
        """
        Called by each command formatter method.
        """
        return (cmd, params, opt)

    # Implementation of the query factories
    # ------------------------------------------------ 

    def help(self, cmd=None):
        return self._return_proxy("help", None, [cmd])
    
    def quit(self):
        return self._return_proxy("quit", None, None)

    def login(self, user, password):
        params = dict()
        params["client_login_name"] = user
        params["client_login_password"] = password
        return self._return_proxy("login", params, None)

    def logout(self):        
        return self._return_proxy("logout", None, None)
    
    def version(self):
        return self._return_proxy("version", None, None)

    def hostinfo(self):
        return self._return_proxy("hostinfo", None, None)

    def instanceinfo(self):
        return self._return_proxy("instanceinfo", None, None)

##    def instanceedit(self, params=None):
##        return self._return_proxy("instanceedit", params, None)

    def bindinglist(self):
        return self._return_proxy("bindinglist", None, None)

    def use(self, sid=None, port=None, virtual=False):
        params = dict()
        if sid is not None:
            params["sid"] = int(sid)
        if port is not None:
            params["port"] = int(port)
        
        opt = list()
        if virtual:
            opt.append("virtual")
        return self._return_proxy("use", params, opt)
    
    def serverlist(self, uid=False, short=False,
                   all_=False, onlyoffline=False):
        opt = list()
        if uid:
            opt.append("uid")
        if short:
            opt.append("short")
        if all_:
            opt.append("all")
        if onlyoffline:
            opt.append("onlyoffline")
        return self._return_proxy("serverlist", None, opt)

    def serveridgetbyport(self, port):
        params = dict()
        params["virtualserver_port"] = int(port)
        return self._return_proxy("serveridgetbyport", params, None)

    def serverdelete(self, sid):
        params = dict()
        params["sid"] = int(sid)
        return self._return_proxy("serverdelete", params, None)

    def servercreate(self, name, properties=None):
        params = dict()
        params["virtualserver_name"] = name
        if properties is not None:
            params.update(properties)
        return self._return_proxy("servercreate", params, None)

    def serverstart(self, sid):
        params = dict()
        params["sid"] = int(sid)
        return self._return_proxy("serverstart", params, None)

    def serverstop(self, sid):
        params = dict()
        params["sid"] = int(sid)
        return self._return_proxy("serverstop", params, None)

    def serverprocessstop(self):
        return self._return_proxy("serverprocessstop", None, None)

    def serverinfo(self):
        return self._return_proxy("serverinfo", None, None)

    def serverrequestconnectioninfo(self):
        return self._return_proxy("serverrequestconnectioninfo", None, None)

    def servertemppasswordadd(self, password, description,
                              duration, tcid, tcpw):
        params = dict()
        params["pw"] = password
        params["desc"] = description
        params["duration"] = int(duration)
        params["tcid"] = int(tcid)
        params["tcpw"] = tcpw
        return self._return_proxy("servertemppasswordadd", params, None)
        
    def servertemppassworddel(self, password):
        params = dict()
        params["pw"] = password
        return self._return_proxy("servertemppassworddel", params, None)

    def servertemppasswordlist(self):
        return self._return_proxy("servertemppasswordlist", None, None)

##    def serveredit(self, properties=None):
##        return self._return_proxy("serveredit", properties, None)
            
    def servergrouplist(self):
        return self._return_proxy("servergrouplist", None, None)
    
    def servergroupadd(self, name, type_=None):
        params = dict()
        params["name"] = name
        params["type"] = int(type_)
        return self._return_proxy("servergroupadd", params, None)

    def servergroupdel(self, sgid, force):
        params = dict()
        params["sgid"] = int(sgid)
        params["force"] = int(force)
        return self._return_proxy("servergroupdel", params, None)

    def servergroupcopy(self, ssgid, tsgid, name, type_):
        params = dict()
        params["ssgid"] = int(ssgid)
        params["tsgid"] = int(tsgid)
        params["name"] = name
        params["type"] = int(type_)
        return self._return_proxy("servergroupcopy", params, None)

    def servergrouprename(self, sgid, name):
        params = dict()
        params["sgid"] = int(sgid)
        params["name"] = name
        return self._return_proxy("servergrouprename", params, None)

    def servergrouppermlist(self, sgid, permsid=False):
        params = dict()
        params["sgid"] = int(sgid)

        opt = list()
        if permsid:
            opt.append("permsid")
        return self._return_proxy("servergrouppermlist", params, opt)

##    def servergroupaddperm(self, ...):
##        pass

##    def servergroupdelperm(self, sgid, permid=None, permsid=None):
##        pass

    def servergroupaddclient(self, sgid, cldbid):
        params = dict()
        params["sgid"] = int(sgid)
        params["cldbid"] = int(cldbid)
        return self._return_proxy("servergroupaddclient", params, None)

    def servergroupdelclient(self, sgid, cldbid):
        params = dict()
        params["sgid"] = int(sgid)
        params["cldbid"] = int(cldbid)
        return self._return_proxy("servergroupdelclient", params, None)

    def servergroupclientlist(self, sgid, names=False):
        params = dict()
        params["sgid"] = int(sgid)

        opt = list()
        if names:
            opt.append("names")
        return self._return_proxy("servergroupclientlist", params, opt)

    def servergroupsbyclientid(self, cldbid):
        params = dict()
        params["cldbid"] = int(cldbid)
        return self._return_proxy("servergroupsbyclientid", params, None)

##    def servergroupautooaddperm(self, ...):
##        pass

##    def servergroupautodelperm(self, ...):
##        pass

    def serversnapshotcreate(self):
        return self._return_proxy("serversnapshotcreate", None, None)

##    def serversnapshotdeploy(self, snapshot):
##        return self._return_proxy("serversnapshotdeploy " + snapshot, None, None)

    def servernotifyregister(self, event, id_=None):
        params = dict()
        params["event"] = event
        if id_ is not None:
            params["id"] = int(id_)
        return self._return_proxy("servernotifyregister", params, None)

    def servernotifyunregister(self):
        return self._return_proxy("servernotifyunregister", None, None)

    def sendtextmessage(self, targetmode, target, msg):
        params = dict()
        params["targetmode"] = int(targetmode)
        params["target"] = int(target)
        params["msg"] = msg
        return self._return_proxy("sendtextmessage", params, None)
    
    def logview(self, lines=None, reverse=None,
                instance=None, begin_pos=None):
        params = dict()
        if lines is not None:
            params["lines"] = int(lines)
        if reverse is not None:
            params["reverse"] = int(reverse)
        if instance is not None:
            params["instance"] = int(instance)
        if begin_pos is not None:
            params["begin_pos"] = int(begin_pos)
        return self._return_proxy("logview", params, None)

    def logadd(self, loglevel, logmsg):
        params = dict()
        params["loglevel"] = int(loglevel)
        params["logmsg"] = int(logmsg)
        return self._return_proxy("logadd", params, None)

    def gm(self, msg):
        params = dict()
        params["msg"] = msg
        return self._return_proxy("gm", params, None)

    def channellist(self, topic=False, flags=False, voice=False, limits=False,
                    icon=False, secondsempty=False):
        opt = list()
        if topic:
            opt.append("topic")
        if flags:
            opt.append("flags")
        if voice:
            opt.append("voice")
        if limits:
            opt.append("limits")
        if icon:
            opt.append("icon")
        if secondsempty:
            opt.append("secondsempty")
        return self._return_proxy("channellist", None, opt)

    def channelinfo(self, cid):
        params = dict()
        params["cid"] = int(cid)
        return self._return_proxy("channelinfo", params, None)

    def channelfind(self, pattern=None):
        params = dict()
        if pattern is not None:
            params["pattern"] = pattern
        return self._return_proxy("channelfind", params, None)

    def channelmove(self, cid, cpid, order=None):
        params = dict()
        params["cid"] = int(cid)
        params["cpid"] = int(cpid)
        if order is not None:
            params["order"] = int(order)
        return self._return_proxy("channelmove", params, None)

    def channelcreate(self, name, properties=None):
        params = dict()
        params["channel_name"] = name
        if properties is not None:
            params.update(properties)
        print(params)
        return self._return_proxy("channelcreate", params, None)
        
    def channeldelete(self, cid, force):
        params = dict()
        params["cid"] = int(cid)
        params["force"] = int(force)
        return self._return_proxy("channeldelete", params, None)

    def channeledit(self, cid, properties=None):
        params = dict()
        params["cid"] = int(cid)
        if properties is not None:
            params.update(properties)
        return self._return_proxy("channeledit", params, None)
        
    def channelgrouplist(self):
        return self._return_proxy("channelgrouplist", None, None)

    def channelgroupadd(self, name, type_):
        params = dict()
        params["name"] = name
        params["type"] = int(type_)
        return self._return_proxy("channelgroupadd", params, None)

    def channelgroupdel(self, cgid, force):
        params = dict()
        params["cgid"] = int(cgid)
        params["force"] = int(force)
        return self._return_proxy("channelgroupdel", params, None)

    def channelgroupcopy(self, scgid, tcgid, name, type_):
        params = dict()
        params["scgid"] = int(scgid)
        params["tcgid"] = int(tcgid)
        params["name"] = name
        params["type"] = int(type_)
        return self._return_proxy("channelgroupcopy", params, None)

    def channelgrouprename(self, cgid, name):
        params = dict()
        params["cgid"] = int(cgid)
        params["name"] = name
        return self._return_proxy("channelgrouprename", params, None)

##    def channelgroupaddperm(self, ...):
##        pass

    def channelgrouppermlist(self, cgid, permsid=False):
        params = dict()
        params["cgid"] = int(cgid)

        opt = list()
        if permsid:
            opt.append("permsid")
        return self._return_proxy("channelgrouppermlist", params, opt)

##    def channelgroupdelperm(self, ...):
##        pass

    def channelgroupclientlist(self, cid=None, cldbid=None, cgid=None):
        params = dict()
        if cid is not None:
            params["cid"] = int(cid)
        if cldbid is not None:
            params["cldbid"] = int(cldbid)
        if cgid is not None:
            params["cgid"] = int(cgid)
        return self._return_proxy("channelgroupclientlist", params, None)

    def setclientchannelgroup(self, cgid, cid, cldbid):
        params = dict()
        params["cgid"] = int(cgid)
        params["cid"] = int(cid)
        params["cldbid"] = int(cldbid)
        return self._return_proxy("setclientchannelgroup", params, None)
        
    def channelpermlist(self, cid, permsid=False):
        params = dict()
        params["cid"] = int(cid)

        opt = list()
        if permsid:
            opt.append("permsid")
        return self._return_proxy("channelpermlist", params, opt)

##    def channeladdperm(self, ...):
##        pass
    
##    def channeldelperm(self, ...):
##        pass

    def clientlist(self, uid=False, away=False, voice=False,
                   times=False, groups=False, info=False, icon=False,
                   country=False, ip=False):
        opt = list()
        if uid:
            opt.append("uid")
        if away:
            opt.append("away")
        if voice:
            opt.append("voice")
        if times:
            opt.append("times")
        if groups:
            opt.append("groups")
        if info:
            opt.append("info")
        if icon:
            opt.append("icon")
        if country:
            opt.append("country")
        if ip:
            opt.append("ip")
        return self._return_proxy("clientlist", None, opt)

    def clientinfo(self, clid):
        params = dict()
        params["clid"] = int(clid)
        return self._return_proxy("clientinfo", params, None)

    def clientfind(self, pattern):
        params = dict()
        params["pattern"] = pattern
        return self._return_proxy("clientfind", params, None)

    def clientedit(self, clid, properties=None):
        params = dict()
        params["clid"] = int(clid)
        if properties is not None:
            params.update(properties)
        return self._return_proxy("clientedit", params, None)
    
    def clientdblist(self, start=None, duration=None, count=False):
        params = dict()
        if start is not None:
            # Todo: Is this an int?
            params["start"] = int(start)
        if duration is not None:
            # Todo: Is this an int?
            params["duration"] = int(duration)

        opt = list()
        if count:
            opt.append("count")
        return self._return_proxy("clientdblist", params, opt)

    def clientdbinfo(self, cldbid):
        params = dict()
        params["cldbid"] = int(cldbid)
        return self._return_proxy("clientdbinfo", params, None)

    def clientdbfind(self, pattern, uid=False):
        params = dict()
        params["pattern"] = pattern

        opt = list()
        if uid:
            opt.append("uid")
        return self._return_proxy("clientdbfind", params, opt)

    def clientdbedit(self, cldbid, properties=None):
        params = dict()
        params["cldbid"] = int(cldbid)
        if properties is not None:
            params.update(properties)
        return self._return_proxy("clientdbedit", params, None)

    def clientdbdelete(self, cldbid):
        params = dict()
        params["cldbid"] = int(cldbid)
        return self._return_proxy("clientdbdelete", params, None)

    def clientgetids(self, cluid):
        params = dict()
        params["cluid"] = cluid
        return self._return_proxy("clientgetids", params, None)

    def clientgetdbidfromuid(self, cluid):
        params = dict()
        params["cluid"] = cluid
        return self._return_proxy("clientgetdbidfromuid", params, None)

    def clientgetnamefromuid(self, cluid):
        params = dict()
        params["cluid"] = cluid
        return self._return_proxy("clientgetnamefromuid", params, None)
    
    def clientgetnamefromdbid(self, cldbid):
        params = dict()
        params["cldbid"] = int(cldbid)
        return self._return_proxy("clientgetnamefromdbid", params, None)

    def clientsetserverquerylogin(self, client_login_name):
        params = dict()
        params["client_login_name"] = client_login_name
        return self._return_proxy("clientsetserverquerylogin", params, None)

    def clientupdate(self, properties=None):
        params = dict()
        if properties is not None:
            params.update(properties)
        return self._return_proxy("clientupdate", params, None)

    def clientmove(self, clid, cid, cpw=None):
        params = dict()
        # Todo: Support for multiple clids.
        params["clid"] = clid
        params["cid"] = cid
        if cpw is not None:
            params["cpw"] = cpw
        return self._return_proxy("clientmove", params, None)

    def clientkick(self, clid, reasonid, reasonmsg=None):
        params = dict()
        # Todo: Support for multiple clients.
        params["clid"] = clid
        params["reasonid"] = int(reasonid)
        if reasonmsg is not None:
            params["reasonmsg"] = reasonmsg        
        return self._return_proxy("clientkick", params, None)
    
    def clientpoke(self, clid, msg):
        params = dict()
        # Todo: Support for multiple clients
        params["clid"] = clid
        params["msg"] = msg    
        return self._return_proxy("clientpoke", params, None)

    def clientpermlist(self, cldbid, permsid=False):
        params = dict()
        params["cldbid"] = int(cldbid)

        opt = list()
        if permsid:
            opt.append("permsid")
        return self._return_proxy("clientpermlist", params, opt)

##    def clientaddperm(self, ...):
##        pass

##    def clientdelperm(self, ...):
##        pass

    def channelclientpermlist(self, cid, cldbid, permsid=False):
        params = dict()
        params["cid"] = int(cid)
        params["cldbid"] = int(cldbid)

        opt = list()
        if permsid:
            opt.append("permsid")
        return self._return_proxy("channelclientpermlist", params, opt)

##    def channelclientaddperm(self, ...):
##        pass

##    def channelclientdelperm(self, ...):
##        pass

    def permissionlist(self):
        return self._return_proxy("permissionlist", None, None)

    def permidgetbyname(self, permsid):
        params = dict()
        # Todo: Add support for multiple permsids.
        params["permsid"] = permsid
        return self._return_proxy("permidgetbyname", params, None)
