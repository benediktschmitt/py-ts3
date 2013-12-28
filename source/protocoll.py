#!/usr/bin/python3


"""
Implementation of the TS3 server query protocoll.
This module should help to build valid ts3 query commands.
"""


# Classes
# ------------------------------------------------
class TS3Commands(object):
    """
    Returns the string described in the documentation to execute the command.
    Consider this as the implementation of the protocoll.

    Each method returns a triple:
        (command, parameters, options)
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
        opt = list()
        if sid is not None:
            sid = int(sid)
            params["sid"] = sid
        if port is not None:
            port = int(port)
            params["port"] = port
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
        params["name"] = str(name)
        params["type"] = int(type_)
        return self._return_proxy("servergroupcopy", params, None)

    # --------------------------------------------
    
##    def servergrouprename(self, sgid, name):
##        sgid = int(sgid)
##        name = common.escape(name)
##        qcmd = "servergrouprename sgid={0} name={1}".format(sgid, name)
##        return self._return_proxy(qcmd)

##    def servergrouppermlist(self, sgid, permsid=False):
##        sgid = int(sgid)
##        qcmd = "servergrouppermlist sgid={0}".format(sgid)
##        if permsid:
##            qcmd += " -permsid"
##        return self._return_proxy(qcmd)

##    def servergroupaddperm(self, ):
##        cmd = ""
##        return self._return_proxy(qcmd)

##    def servergroupdelperm(self, sgid, permid=None, permsid=None):
##        sgid = int(sgid)            
##        cmd = "servergroupdelperm sgid={0} ".format(sgid)
##        if permid is not None:
##            permid = int(permid)
##            cmd += " permid={}".format(permid)
##        if permsid is not None:
##            permid = Escape.escape(permsid)
##            cmd += " permsid={}".format(permsid)
##        return self._return_proxy(qcmd)

##    def servergroupaddclient(self, sgid, cldbid):
##        sgid = int(sgid)
##        cldbid = int(cldbid)
##        qcmd = "servergroupaddclient sgid={} cldbid={}"\
##               .format(sgid, cldbid)
##        return self._return_proxy(qcmd)

##    def servergroupdelclient(self, sgid, cldbid):
##        sgid = int(sgid)
##        cldbid = int(cldbid)
##        qcmd = "servergroupdelclient sgid={} cldbid={}"\
##               .format(sgid, cldbid)
##        return self._return_proxy(qcmd)

##    def servergroupclientlist(self, sgid, names=False):
##        sgid = int(sgid)
##        qcmd = "servergroupclientlist sgid={}".format(sgid)
##        if names:
##            qcmd += " -names"
##        return self._return_proxy(qcmd)

##    def servergroupsbyclientid(self, cldbid):
##        cldbid = int(cldbid)
##        qcmd = "servergroupsbyclientid cldbid={}".format(cldbid)
##        return self._return_proxy(qcmd)

##    def servergroupautooaddperm(self, ...):
##        pass

##    def servergroupautodelperm(self, ...):
##        pass

##    def serversnapshotcreate(self):
##        qcmd = "serversnapshotcreate"
##        return self._return_proxy(qcmd)

##    def serversnapshotdeploy(self, snapshot):
##        # Snapshot should already be escaped, so don't change it.
##        qcmd = "serversnapshotdeploy virtualserver_snapshot={}"\
##               .format(snapshot)
##        return self._return_proxy(qcmd)

##    def servernotifyregister(self, event, id_=None):
##        event = common.escape(event)
##        cmd = "servernotifyregister event={0}".format(event)
##        if id_ is not None:
##            id_ = int(id_)
##            cmd += " id={}".format(id_)
##        return self._return_proxy(qcmd)

##    def servernotifyunregister(self):
##        cmd = "servernotifyunregister"
##        return self._return_proxy(qcmd)

##    def sendtextmessage(self, targetmode, target, msg):
##        targetmode = int(targetmode)
##        target = int(target)
##        msg = Escape.escape(msg)
##        cmd = "sendtextmessage targetmode={0} target={1} msg={2}"\
##              .format(targetmode, target, msg)
##        return self._return_proxy(qcmd)

##    def logview(self, lines=None, reverse=None,
##                instance=None, begin_pos=None):
##        cmd = "logview"
##        if lines is not None:
##            lines = int(lines)
##            cmd += " lines={}".format(lines)
##        if reverse is not None:
##            reverse = int(reverse)
##            cmd += " reverse={}".format(reverse)
##        if instance is not None:
##            instance = int(instance)
##            cmd += " instance={}".format(instance)
##        if begin_pos is not None:
##            begin_pos = int(begin_pos)
##            cmd += " beginpos={}".format(begin_pos)
##        return self._return_proxy(qcmd)

##    def logadd(self, loglevel, logmsg):
##        loglevel = int(loglevel)
##        logmsg = Escape.escape(logmsg)
##        cmd = "logadd loglevel={0} logmsg={1}"\
##              .format(loglevel, logmsg)
##        return self._return_proxy(qcmd)

##    def gm(self, msg):
##        msg = Escape.escape(msg)
##        cmd = "gm msg={0}".format(msg)
##        return self._return_proxy(qcmd)

##    def channellist(self, topic=False, flags=False,
##                    voice=False, limits=False, icon=False):
##        cmd = "channellist"
##        if topic:
##            cmd += " -topic"
##        if flags:
##            cmd += " -flags"
##        if voice:
##            cmd += " -voice"
##        if limits:
##            cmd += " -limits"
##        if icon:
##            cmd += " -icon"
##        return self._return_proxy(qcmd)

##    def channelinfo(self, cid):
##        cid = int(cid)
##        cmd = "channelinfo cid={0}".format(cid)
##        return self._return_proxy(qcmd)

##    def channelfind(self, pattern=None):
##        cmd = "channelfind"
##        if pattern is not None:
##            # Todo: Escape the pattern string?
##            cmd += " pattern={}".format(pattern)
##        return self._return_proxy(qcmd)

##    def channelmove(self, cid, cpid, order=None):
##        cid = int(cid)
##        cpid = int(cpid)
##        cmd = "channelmove cid={0} cpid={1}"\
##              .format(cid, cpid)
##        if order is not None:
##            order = int(order)
##            cmd += " order={}".format(order)
##        return self._return_proxy(qcmd)

##    def channelcreate(self, name, properties=None):
##        name = Escape.escape(name)
##        properties = Escape.properties_to_str(properties)
##        cmd = "channelcreate name={0} {1}"\
##              .format(name, properties)
##        return self._return_proxy(qcmd)
        
##    def channeldelete(self, cid, force):
##        cid = int(cid)
##        force = int(force)
##        cmd = "channeldelete cid={0} force={1}"\
##              .format(cid, force)
##        return self._return_proxy(qcmd)

##    def channeledit(self, cid, properties=None):
##        cid = int(cid)
##        properties = Escape.properties_to_str(properties)
##        cmd = "channeledit cid={0} {1}"\
##              .format(cid, properties)
##        return self._return_proxy(qcmd)
        
##    def channelgrouplist(self):
##        cmd = "channelgrouplist"
##        return self._return_proxy(qcmd)

##    def channelgroupadd(self, name, type_):
##        name = Escape.escape(name)
##        type_ = int(type_)
##        cmd = "channelgroupadd name={0} type={1}"\
##              .format(name, type_)
##        return self._return_proxy(qcmd)

##    def channelgroupdel(self, cgid, force):
##        cgid = int(cgid)
##        force = int(force)
##        cmd = "channelgroupdelete cgid={0} force={1}"\
##              .format(cgid, force)
##        return self._return_proxy(qcmd)

##    def channelgroupcopy(self, scgid, tcgid, name, type_):
##        scgid = int(scgid)
##        tcgid = int(tcgid)
##        name = Escape.escape(name)
##        type_ = int(type_)
##        cmd = "channelgroupcopy scgid={0} tcgid={1} name={2} type={3}"\
##              .format(scgid, tcgid, name, type_)
##        return self._return_proxy(qcmd)

##    def channelgrouprename(self, cgid, name):
##        cgid = int(cgid)
##        name = Escape.escape(name)
##        cmd = "channelgrouprename cgid={} name={}"\
##              .format(cigd, name)
##        return self._return_proxy(qcmd)

##    def channelgroupaddperm(self, ...):
##        pass

##    def channelgrouppermlist(self, cgid, permsid=False):
##        cgid = int(cgid)
##        cmd = "channelgrouppermlist cgid={0}".format(cgid)
##        if permsid:
##            cmd += " -permsid"
##        return self._return_proxy(qcmd)

##    def channelgroupdelperm(self, ...):
##        pass

##    def channelgroupclientlist(self, cid=None, cldbid=None, cgid=None):
##        cmd = "channelgroupclientlist"
##        if cid is not None:
##            cid = int(cid)
##            cmd += " cid={}".format(cid)
##        if cldbid is not None:
##            cldbid = int(cldbid)
##            cmd += " cldbid={}".format(cldbid)
##        if cgid is not None:
##            cgid = int(cgid)
##            cmd += " cgid={}".format(cgid)
##        return self._return_proxy(qcmd)

##    def setclientchannelgroup(self, cgid, cid, cldbid):
##        cgid = int(cgid)
##        cid = int(cid)
##        cldbid = int(cldbid)
##        cmd = "setclientchannelgroup cgid={0} cid={1} cldbid={2}"\
##              .format(cgid, cid, cldbid)
##        return self._return_proxy(qcmd)

##    def channelpermlist(self, cid, permsid=False):
##        cid = int(cid)
##        cmd = "channelpermlist cid={0}".format(cid)
##        if permsid:
##            cmd += " -permsid"
##        return self._return_proxy(qcmd)

##    def channeladdperm(self, ...):
##        pass
    
##    def channeldelperm(self, ...):
##        pass

##    def clientlist(self, uid=False, away=False, voice=False,
##                   times=False, groups=False, info=False, icon=False,
##                   country=False):
##        cmd = "clientlist"
##        if uid:
##            cmd += " -uid"
##        if away:
##            cmd += " -away"
##        if voice:
##            cmd += " -voice"
##        if times:
##            cmd += " -times"
##        if groups:
##            cmd += " -groups"
##        if info:
##            cmd += " -info"
##        if icon:
##            cmd += " -icon"
##        if country:
##            cmd += " -country"
##        return self._return_proxy(qcmd)

##    def clientinfo(self, clid):
##        clid = int(clid)
##        cmd = "clientinfo clid={0}".format(clid)
##        return self._return_proxy(qcmd)

##    def clientfind(self, pattern):
##        # Todo: Escape the pattern?
##        pattern = Escape.escape(pattern)
##        cmd = "clientfind pattern={}".format(pattern)
##        return self._return_proxy(qcmd)

##    def clientedit(self, clid, properties=None):
##        clid = int(clid)
##        properties = Escape.properties_to_str(properties)
##        cmd = "clientedit clid={0} {1}"\
##              .format(clientid, properties)
##        return self._return_proxy(qcmd)
    
##    def clientdblist(self, start=None, duration=None, count=False):
##        cmd = "clientdblist"
##        if start is not None:
##            start = int(start)
##            cmd += " start={}".format(start)
##        if duration is not None:
##            duration = int(duration)
##            cmd += " duration={}".format(duration)
##        if count:
##            cmd += " -count"
##        return self._return_proxy(qcmd)

##    def clientdbinfo(self, cldbid):
##        cldbid = int(cldbid)
##        cmd = "clientdbinfo cldbid={0}".format(cldbid)
##        return self._return_proxy(qcmd)

##    def clientdbfind(self, pattern, uid=False):
##        # Todo: Escape this pattern?
##        pattern = Escape.escape(pattern)
##        cmd = "clientdbfind pattern={0}".format(pattern)
##        if uid:
##            cmd += " -uid"
##        return self._return_proxy(qcmd)

##    def clientdbedit(self, cldbid, properties=None):
##        cldbid = int(cldbid)
##        properties = Escape.properties_to_str(properties)
##        cmd = "clientdbedit cldbid={0} {1}"\
##              .format(cldbid, properties)
##        return self._return_proxy(qcmd)

##    def clientdbdelete(self, cldbid):
##        cldbid = int(cldbid)
##        cmd = "clientdbdelete cldbid={0}".format(cldbid)
##        return self._return_proxy(qcmd)

##    def clientgetids(self, cluid):
##        # Todo: Is escaping reasonable?
##        cluid = Escape.escape(cluid)
##        cmd = "clientgetids cluid={0}"\
##              .format(cluid)
##        return self._return_proxy(qcmd)

##    def clientgetdbidfromuid(self, cluid):
##        # Todo: Is escaping reasonable?
##        cluid = Escape.escape(cluid)
##        cmd = "clientgetdbidfromuid cluid={0}"\
##              .format(cluid)
##        return self._return_proxy(qcmd)

##    def clientgetnamefromuid(self, cluid):
##        # Todo: Is escaping reasonable?
##        cluid = Escape.escape(cluid)
##        cmd = "clientgetnamefromuid cluid={0}"\
##              .format(cluid)
##        return self._return_proxy(qcmd)

##    def clientgetnamefromdbid(self, cldbid):
##        cldbid = int(cldbid)
##        cmd = "clientgetnamefromdbid cldbid={0}"\
##              .format(cldbid)
##        return self._return_proxy(qcmd)

##    def clientsetserverquerylogin(self, client_login_name):
##        client_login_name = Escape.escape(client_login_name)
##        cmd = "clientsetserverquerylogin client_login_name={0}"\
##              .format(client_login_name)
##        return self._return_proxy(qcmd)

##    def clientupdate(self, properties):
##        properties = Escape.properties_to_str(properties)
##        cmd = "clientupdate {0}".format(properties)
##        return self._return_proxy(qcmd)

##    def clientmove(self, clid, cid, cpw=None):
##        if isinstance(clid, int):
##            clid = [clid]
##        clid = "|".join("clid={}".format(int(e)) for e in clid)
##        cid = int(cid)
##        
##        cmd = "clientmove clid={0} cid={1}"\
##              .format(clid, cid)
##        if cpw is not None:
##            cpw = Escape.escape(cpw)
##            cmd += " cpw={0}".format(cpw)
##        return self._return_proxy(qcmd)
##
##    def clientkick(self, clid, reasonid, reasonmsg=None):
##        if isinstance(clid, int):
##            clid = [clid]
##        clid = "|".join("clid={}".format(int(e)) for e in clid)
##        reasonid = int(reasonid)
##
##        cmd = "clientkick clid =

##    def clientpoke(self, clid, msg):
##        clid = int(clid)
##        msg = Escape.escape(msg)
##        cmd = "clientpoke clid={0} msg={1}"\
##              .format(clid, msg)
##        return self._return_proxy(qcmd)

##    def clientpermlist(self, cldbid, permsid=False):
##        cldbid = int(cldbid)
##        cmd = "clientpermlist cldbid={0}".format(cldbid)
##        if permsid:
##            cmd += " -permsid"
##        return self._return_proxy(qcmd)

##    def clientaddperm(self, ...):
##        pass

##    def clientdelperm(self, ...):
##        pass

##    def channelclientpermlist(self, cid, cldbid, permsid=False):
##        cid = int(cid)
##        cldbid = int(cldbid)
##        cmd = "channelclientpermlist cid={} cldbid={}"\
##              .format(cid, cldbid)
##        if permsid:
##            cmd += " -permsid"
##        return self._return_proxy(qcmd)

##    def channelclientaddperm(self, ...):
##        pass

##    def channelclientdelperm(self, ...):
##        pass

##    def permissionlist(self):
##        cmd = "permissionlist"
##        return self._return_proxy(qcmd)
