#!/usr/bin/python3

# The MIT License (MIT)
# 
# Copyright (c) 2013 Benedikt Schmitt
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


# Classes
# ------------------------------------------------
class TS3Commands(object):
    """
    A little helper class, that creates the *command* string,
    *parameters* dict and the *options* list for all available query commands,
    so that these values can be used to call *TS3BaseConnection.send(...)*.

    The type or values of the parameters are **NOT* validated.
    """

    def _return_proxy(self, cmd, params, opt):
        """
        Called by each command formatter method.
        """
        return (cmd, params, opt)

    # Implementation of the query factories
    # ------------------------------------------------

    def help(self, cmd=None):
        if cmd is not None:
            qcmd = "help " + cmd
        else:
            qcmd = "help"
        return self._return_proxy(qcmd, None, None)
    
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

    def instanceedit(self, params=None):
        return self._return_proxy("instanceedit", params, None)

    def bindinglist(self):
        return self._return_proxy("bindinglist", None, None)

    def use(self, sid=None, port=None, virtual=False):
        params = dict()
        params["sid"] = sid
        params["port"] = port

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
        params["virtualserver_port"] = port
        return self._return_proxy("serveridgetbyport", params, None)

    def serverdelete(self, sid):
        params = dict()
        params["sid"] = sid
        return self._return_proxy("serverdelete", params, None)

    def servercreate(self, name, properties=None):
        params = dict()
        params["name"] = name
        if properties is not None:
            params.update(properties)
        return self._return_proxy("servercreate", params, None)

    def serverstart(self, sid):
        params = dict()
        params["sid"] = sid
        return self._return_proxy("serverstart", params, None)

    def serverstop(self, sid):
        params = dict()
        params["sid"] = sid
        return self._return_proxy("serverstop", params, None)

    def serverprocessstop(self):
        return self._return_proxy("serverprocessstop", None, None)

    def serverinfo(self):
        return self._return_proxy("serverinfo", None, None)

    def serverrequestconnectioninfo(self):
        return self._return_proxy("serverrequestconnectioninfo", None, None)

    def servertemppasswordadd(self, password, description,
                              duration, target_cid, target_channel_pw):
        params = dict()
        params["pw"] = password
        params["desc"] = description
        params["duration"] = duration
        params["tcid"] = target_cid
        params["tcpw"] = target_channel_pw
        return self._return_proxy("servertemppasswordadd", params, None)
        
    def servertemppassworddel(self, password):
        params = dict()
        params["pw"] = password
        return self._return_proxy("servertemppassworddel", params, None)

    def servertemppasswordlist(self):
        return self._return_proxy("servertemppasswordlist", None, None)

    def serveredit(self, properties=None):
        return self._return_proxy("serveredit", properties, None)
            
    def servergrouplist(self):
        return self._return_proxy("servergrouplist", None, None)
    
    def servergroupadd(self, groupName, groupDbType=None):
        params = dict()
        params["name"] = groupName
        params["type"] = groupDbType
        return self._return_proxy("servergroupadd", params, None)

    def servergroupdel(self, groupID, force):
        params = dict()
        params["sgid"] = groupID
        params["force"] = force
        return self._return_proxy("servergroupdel", params, None)

    def servergroupcopy(self, sourceGroupID, targetGroupID,
                        groupName, groupDbType):
        params = dict()
        params["ssgid"] = sourceGroupID
        params["tsgid"] = targetGroupID
        params["name"] = groupName
        params["type"] = groupDbType
        return self._return_proxy("servergroupcopy", params, None)

    def servergrouprename(self, groupID, groupName):
        params = dict()
        params["sgid"] = groupID
        params["name"] = groupName
        return self._return_proxy("servergrouprename", params, None)

    def servergrouppermlist(self, groupID, permsid=False):
        params = dict()
        params["sgid"] = groupID

        opt = list()
        if permsid:
            opt.append("permsid")
        return self._return_proxy("servergrouppermlist", params, opt)

##    def servergroupaddperm(self, ...):
##        pass

##    def servergroupdelperm(self, sgid, permid=None, permsid=None):
##        pass

    def servergroupaddclient(self, groupID, clientDBID):
        params = dict()
        params["sgid"] = groupID
        params["cldbid"] = clientDBID
        return self._return_proxy("servergroupaddclient", params, None)

    def servergroupdelclient(self, groupID, clientDBID):
        params = dict()
        params["sgid"] = groupID
        params["cldbid"] = clientDBID
        return self._return_proxy("servergroupdelclient", params, None)

    def servergroupclientlist(self, groupID, names=False):
        params = dict()
        params["sgid"] = groupID

        opt = list()
        if names:
            opt.append("names")
        return self._return_proxy("servergroupclientlist", params, opt)

    def servergroupsbyclientid(self, clientDBID):
        params = dict()
        params["cldbid"] = clientDBID
        return self._return_proxy("servergroupsbyclientid", params, None)

##    def servergroupautooaddperm(self, ...):
##        pass

##    def servergroupautodelperm(self, ...):
##        pass

    def serversnapshotcreate(self):
        return self._return_proxy("serversnapshotcreate", None, None)

##    def serversnapshotdeploy(self, snapshot):
##        return self._return_proxy("serversnapshotdeploy " + snapshot, None, None)

    def servernotifyregister(self, event, channelID=None):
        params = dict()
        params["event"] = event
        params["id"] = channelID
        return self._return_proxy("servernotifyregister", params, None)

    def servernotifyunregister(self):
        return self._return_proxy("servernotifyunregister", None, None)

    def sendtextmessage(self, targetmode, target, msg):
        params = dict()
        params["targetmode"] = targetmode
        params["target"] = target
        params["msg"] = msg
        return self._return_proxy("sendtextmessage", params, None)
    
    def logview(self, lines=None, reverse=None,
                instance=None, begin_pos=None):
        params = dict()
        params["line"] = lines
        params["reverse"] = reverse
        params["instance"] = instance
        params["begin_pos"] = begin_pos
        return self._return_proxy("logview", params, None)

    def logadd(self, loglevel, logmsg):
        params = dict()
        params["loglevel"] = loglevel
        params["logmsg"] = logmsg
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
        params["cid"] = cid
        return self._return_proxy("channelinfo", params, None)

    def channelfind(self, pattern=None):
        params = dict()
        params["pattern"] = pattern
        return self._return_proxy("channelfind", params, None)

    def channelmove(self, cid, cpid, order=None):
        params = dict()
        params["cid"] = cid
        params["cpid"] = cpid
        params["order"] = order
        return self._return_proxy("channelmove", params, None)

    def channelcreate(self, name, properties=None):
        params = dict()
        params["channel_name"] = name
        if properties is not None:
            params.update(properties)
        return self._return_proxy("channelcreate", params, None)
        
    def channeldelete(self, cid, force):
        params = dict()
        params["cid"] = cid
        params["force"] = force
        return self._return_proxy("channeldelete", params, None)

    def channeledit(self, cid, properties=None):
        params = dict()
        params["cid"] = cid
        if properties is not None:
            params.update(properties)
        return self._return_proxy("channeledit", params, None)
        
    def channelgrouplist(self):
        return self._return_proxy("channelgrouplist", None, None)

    def channelgroupadd(self, name, type_):
        params = dict()
        params["name"] = name
        params["type"] = type_
        return self._return_proxy("channelgroupadd", params, None)

    def channelgroupdel(self, cgid, force):
        params = dict()
        params["cgid"] = cgid
        params["force"] = force
        return self._return_proxy("channelgroupdel", params, None)

    def channelgroupcopy(self, scgid, tcgid, name, type_):
        params = dict()
        params["scgid"] = scgid
        params["tcgid"] = tcgid
        params["name"] = name
        params["type"] = type_
        return self._return_proxy("channelgroupcopy", params, None)

    def channelgrouprename(self, cgid, name):
        params = dict()
        params["cgid"] = cgid
        params["name"] = name
        return self._return_proxy("channelgrouprename", params, None)

##    def channelgroupaddperm(...):
##        params = dict()
##        params["cgid"] = cgid

    def channelgrouppermlist(self, cgid, permsid=False):
        params = dict()
        params["cgid"] = cgid

        opt = list()
        if permsid:
            opt.append("permsid")
        return self._return_proxy("channelgrouppermlist", params, opt)

##    def channelgroupdelperm(self, ...):
##        pass

    def channelgroupclientlist(self, cid=None, cldbid=None, cgid=None):
        params = dict()
        params["cid"] = cid
        params["cldbid"] = cldbid
        params["cgid"] = cgid
        return self._return_proxy("channelgroupclientlist", params, None)

    def setclientchannelgroup(self, cgid, cid, cldbid):
        params = dict()
        params["cgid"] = cgid
        params["cid"] = cid
        params["cldbid"] = cldbid
        return self._return_proxy("setclientchannelgroup", params, None)
        
    def channelpermlist(self, cid, permsid=False):
        params = dict()
        params["cid"] = cid

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
        params["clid"] = clid
        return self._return_proxy("clientinfo", params, None)

    def clientfind(self, pattern):
        params = dict()
        params["pattern"] = pattern
        return self._return_proxy("clientfind", params, None)

##    def clientedit(self, clid, properties=None):
##        params = dict()
##        params["clid"] = clid
##        if properties is not None:
##            params.update(properties)
##        return self._return_proxy("clientedit", params, None)
    
    def clientdblist(self, start=None, duration=None, count=False):
        params = dict()
        params["start"] = start
        params["duration"] = duration

        opt = list()
        if count:
            opt.append("count")
        return self._return_proxy("clientdblist", params, opt)

    def clientdbinfo(self, cldbid):
        params = dict()
        params["cldbid"] = cldbid
        return self._return_proxy("clientdbinfo", params, None)

    def clientdbfind(self, pattern, uid=False):
        params = dict()
        params["pattern"] = pattern

        opt = list()
        if uid:
            opt.append("uid")
        return self._return_proxy("clientdbfind", params, opt)

##    def clientdbedit(self, cldbid, properties=None):
##        params = dict()
##        params["cldbid"] = cldbid
##        if properties is not None:
##            params.update(properties)
##        return self._return_proxy("clientdbedit", params, None)

    def clientdbdelete(self, cldbid):
        params = dict()
        params["cldbid"] = cldbid
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
        params["cldbid"] = cldbid
        return self._return_proxy("clientgetnamefromdbid", params, None)

    def clientsetserverquerylogin(self, client_login_name):
        params = dict()
        params["client_login_name"] = client_login_name
        return self._return_proxy("clientsetserverquerylogin", params, None)

##    def clientupdate(self, properties=None):
##        params = dict()
##        if properties is not None:
##            params.update(properties)
##        return self._return_proxy("clientupdate", params, None)

    def clientmove(self, clid, cid, cpw=None):
        params = dict()
        params["clid"] = clid
        params["cid"] = cid
        params["cpw"] = cpw
        return self._return_proxy("clientmove", params, None)

    def clientkick(self, clid, reasonid, reasonmsg=None):
        params = dict()
        params["clid"] = clid
        params["reasonid"] = reasonid
        params["reasonmsg"] = reasonmsg        
        return self._return_proxy("clientkick", params, None)
    
    def clientpoke(self, clid, msg):
        params = dict()
        params["clid"] = clid
        params["msg"] = msg    
        return self._return_proxy("clientpoke", params, None)

    def clientpermlist(self, cldbid, permsid=False):
        params = dict()
        params["cldbid"] = cldbid

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
        params["cid"] = cid
        params["cldbid"] = cldbid

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
        params["permsid"] = permsid
        return self._return_proxy("permidgetbyname", params, None)

    def permoverview(self, cid, cldbid, permid=None, permsid=None):
        params = dict()
        params["cid"] = cid
        params["cldbid"] = cldbid
        params["permid"] = permid
        params["permsid"] = permsid
        return self._return_proxy("permoverview", params, None)

    def permget(self, permid=None, permsid=None):
        params = dict()
        params["permid"] = permid
        params["permsid"] = permsid
        return self._return_proxy("permget", params, None)

    def permfind(self, permid=None, permsid=None):
        params = dict()
        params["permid"] = permid
        params["permsid"] = permsid
        return self._return_proxy("permfind", params, None)

    def permreset(self):
        return self._return_proxy("permreset", None, None)

    def privilegekeylist(self):
        return self._return_proxy("privilegekeylist", None, None)

    def privilegekeyadd(self, tokentype, group_id, channel_id,
                        tokendescription=None, tokencustomset=None):
        params = dict()
        params["tokentype"] = tokentype
        params["tokenid1"] = group_id
        params["tokenid2"] = channel_id
        params["tokendescription"] = tokendescription
        params["tokencustomset"] = tokencustomset
        return self._return_proxy("privilegekeyadd", params, None)

    def privilegekeydelete(self, token):
        params = dict()
        params["token"] = token
        return self._return_proxy("privilegekeydelete", params, None)

    def privilegekeyuse(self, token):
        params = dict()
        params["token"] = token
        return self._return_proxy("privilegekeyuse", params, None)

    def messagelist(self):        
        return self._return_proxy("messagelist", None, None)

    def messageadd(self, cluid, subject, message):
        params = dict()
        params["cluid"] = cluid
        params["subject"] = subject
        params["message"] = message      
        return self._return_proxy("messageadd", params, None)

    def messagedel(self, msgid):
        params = dict()
        params["msgid"] = msgid   
        return self._return_proxy("messagedel", params, None)

    def messageget(self, msgid):
        params = dict()
        params["msgid"] = msgid
        return self._return_proxy("messageget", params, None)

    def messageupdateflag(self, msgid, flag):
        params = dict()
        params["msgid"] = msgid
        params["flag"] = flag
        return self._return_proxy("messageupdateflag", params, None)

    def complainlist(self, tcldbid=None):
        params = dict()
        params["tcldbid"] = tcldbid
        return self._return_proxy("complainlist", params, None)

    def complainadd(self, tcldbid, message):
        params = dict()
        params["tcldbid"] = tcldbid
        params["message"] = message
        return self._return_proxy("complainadd", params, None)

    def complaindelall(self, tcldbid):
        params = dict()
        params["tcldbid"] = tcldbid
        return self._return_proxy("complaindelall", params, None)

    def complaindel(self, tcldbid, fcldbid):
        params = dict()
        params["tcldbid"] = tcldbid
        params["fcldbid"] = fcldbid
        return self._return_proxy("complaindel", params, None)

    def banclient(self, clid, time=None, banreason=None):
        params = dict()
        params["clid"] = clid
        params["time"] = time
        params["banreason"] = banreason
        return self._return_proxy("banclient", params, None)

    def banlist(self):
        return self._return_proxy("banlist", None, None)

    def banadd(self, ip=None, name=None, uid=None, time=None, banreason=None):
        params = dict()
        params["ip"] = ip
        params["name"] = name
        params["uid"] = uid
        params["time"] = time
        params["banreason"] = banreason
        return self._return_proxy("banadd", params, None)

    def bandel(self, banid):
        params = dict()
        params["banid"] = banind
        return self._return_proxy("bandel", params, None)
        
    def bandelall(self):
        return self._return_proxy("bandelall", None, None)

    def ftinitupload(self, clientftfid, name, cid, cpw,
                     size, overwrite, resume):
        params = dict()
        params["clientftfid"] = clientftfid
        params["name"] = name
        params["cid"] = cid
        params["cpw"] = cpw
        params["size"] = size
        params["overwrite"] = overwrite
        params["resume"] = resume
        return self._return_proxy("ftinitupload", params, None)

    def ftinitdownload(self, clientftfid, name, cid, cpw, seekpos):
        params = dict()
        params["clientftfid"] = clientftfid
        params["name"] = name
        params["cid"] = cid
        params["cpw"] = cpw
        params["seekpos"] = seekpos
        return self._return_proxy("ftinitdownload", params, None)

    def ftlist(self):
        return self._return_proxy("ftlist", None, None)

    def ftgetfilelist(self, cid, cpw, path):
        params = dict()
        params["cid"] = cid
        params["cpw"] = cpw
        params["path"] = path
        return self._return_proxy("ftgetfilelist", params, None)

##    def ftgetfileinfo(self, cid, cpw, name):
##        params = dict()
##        # Todo: Support multiple files
##        params["cid"] = cid
##        params["cpw"] = cpw
##        params["name"] = name
##        return self._return_proxy("ftgetfileinfo", params, None)

    def ftstop(self, serverftfid, delete):
        params = dict()
        params["serverftfid"] = serverftfid
        params["delete"] = delete
        return self._return_proxy("ftstop", params, None)

##    def ftdeletefile(self, cid, cpw, name):
##        pass
        
    def ftcreatedir(self, cid, cpw, dirname):
        params = dict()
        params["cid"] = cid
        params["cpw"] = cpw
        params["dirname"] = dirname
        return self._return_proxy("ftcreatedir", params, None)

    def ftrenamefile(self, cid, cpw, oldname, newname, tcid=None, tcpw=None):
        params = dict()
        params["cid"] = cid
        params["cpw"] = cpw
        params["oldname"] = oldname
        params["newname"] = newname
        params["tcid"] = tcid
        params["tcpw"] = tcpw
        return self._return_proxy("ftrenamefile", params, None)

    def customsearch(self, ident, pattern):
        params = dict()
        params["ident"] = ident
        params["pattern"] = pattern
        return self._return_proxy("customsearch", params, None)

    def custominfo(self, cldbid):
        params = dict()
        params["cldbid"] = cldbid
        return self._return_proxy("custominfo", params, None)

    def whoami(self):
        return self._return_proxy("whoami", None, None)
