#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2013-2015 Benedikt Schmitt <benedikt@benediktschmitt.de>
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


# Modules
# ------------------------------------------------
from __future__ import absolute_import
from collections import OrderedDict


# Data
# ------------------------------------------------
__all__ = [u"TS3Commands"]


# Classes
# ------------------------------------------------
class TS3Commands(object):
    u"""
    Provides a convenient interface to build the parameters for
    :meth:`query.TS3BaseConnection.send`.

    .. hint::

        Some query commands accept multiple parameters like
        :meth:`channeladdperm` (*permid*, *permsid*). I did not found a nice
        way to implement that feature. If you think you know a nice way how to
        overload the methods, so that they can handle this feature too, you're
        welcome to create a issue or pull request on GitHub.

    .. note::

        All methods in this class accept only **keyword arguments** to improve
        the readability and to avoid wrong parameter orders compared to the
        official documentation.
    """

    def _return_proxy(self, command, cparameters, uparameters, options):
        u"""
        Each method ends with::

            return self._return_proxy(...)

        So that this method can be overwritten to catch all commands.

        :arg command: The query command
        :type command: string

        :arg cparameters: The common parameters of the query.
        :type cparameters: None or a dictionary

        :arg uparameters: The diffrent unique parameters for the subqueries.
        :type uparameters: None or a list of dictionaries

        :arg options: The options of the command.
        :type options: None or a list of strings.
        """
        return (command, cparameters, uparameters, options)

    def banadd(self, **_3to2kwargs):
        if 'banreason' in _3to2kwargs: banreason = _3to2kwargs['banreason']; del _3to2kwargs['banreason']
        else: banreason = None
        if 'time' in _3to2kwargs: time = _3to2kwargs['time']; del _3to2kwargs['time']
        else: time = None
        if 'uid' in _3to2kwargs: uid = _3to2kwargs['uid']; del _3to2kwargs['uid']
        else: uid = None
        if 'name' in _3to2kwargs: name = _3to2kwargs['name']; del _3to2kwargs['name']
        else: name = None
        if 'ip' in _3to2kwargs: ip = _3to2kwargs['ip']; del _3to2kwargs['ip']
        else: ip = None
        u"""
        Usage::

            banadd [ip={regexp}] [name={regexp}] [uid={clientUID}] [time={timeInSeconds}] [banreason={text}]

        Adds a new ban rule on the selected virtual server. All parameters are optional
        but at least one of the following must be set: ip, name, or uid.

        Example::

           banadd ip=1.2.3.4 banreason=just\s4\sfun
           banid=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.banadd(ip="127.0.0.1")
            ...
            >>> ts3cmd.banadd(name="Ben")
            ...
            >>> ts3cmd.banadd(name="Ben", time=3600, banreason="I hate you!")
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"ip"] = ip
        cparams[u"name"] = name
        cparams[u"uid"] = uid
        cparams[u"time"] = time
        cparams[u"banreason"] = banreason
        return self._return_proxy(u"banadd", cparams, uparams, options)

    def banclient(self, **_3to2kwargs):
        if 'banreason' in _3to2kwargs: banreason = _3to2kwargs['banreason']; del _3to2kwargs['banreason']
        else: banreason = None
        if 'time' in _3to2kwargs: time = _3to2kwargs['time']; del _3to2kwargs['time']
        else: time = None
        clid = _3to2kwargs['clid']; del _3to2kwargs['clid']
        u"""
        Usage::

            banclient clid={clientID} [time={timeInSeconds}] [banreason={text}]

        Bans the client specified with ID clid from the server. Please note that this
        will create two separate ban rules for the targeted clients IP address and his
        unique identifier.

        Example::

           banclient clid=4 time=3600
           banid=2
           banid=3
           error id=0 msg=ok

        Example::

            >>> ts3cmd.banclient(clid=42, time=900, banreason="HAHA")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"clid"] = clid
        cparams[u"time"] = time
        cparams[u"banreason"] = banreason
        return self._return_proxy(u"banclient", cparams, uparams, options)

    def bandel(self, **_3to2kwargs):
        banid = _3to2kwargs['banid']; del _3to2kwargs['banid']
        u"""
        Usage::

            bandel banid={banID}

        Deletes the ban rule with ID banid from the server.

        Example::

           bandel banid=3
           error id=0 msg=ok

        Example::

            >>> ts3cmd.bandel(8)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"banid"] = banid
        return self._return_proxy(u"bandel", cparams, uparams, options)

    def bandelall(self):
        u"""
        Usage::

            bandelall

        Deletes all active ban rules from the server.

        Example::

           bandelall
           error id=0 msg=ok

        Example::

            >>> ts3cmd.bandelall()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"bandelall", cparams, uparams, options)

    def banlist(self):
        u"""
        Usage::

            banlist

        Displays a list of active bans on the selected virtual server.

        Example::

           banlist
           banid=7 ip=1.2.3.4 created=1259444002242 invokername=Sven invokercldbid=56
           invokeruid=oHhi9WzXLNEFQOwAu4JYKGU+C+c= reason enforcements=0
           error id=0 msg=ok

        Example::

            >>> ts3cmd.banlist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"banlist", cparams, uparams, options)

    def bindinglist(self):
        u"""
        Usage::

            bindinglist

        Displays a list of IP addresses used by the server instance on multi-homed
        machines.

        Example::

           bindinglist
           ip=0.0.0.0
           error id=0 msg=ok

        Example:

            >>> ts3cmd.bindinglist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"bindinglist", cparams, uparams, options)

    def channeladdperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        permvalue = _3to2kwargs['permvalue']; del _3to2kwargs['permvalue']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channeladdperm cid={channelID} ( permid={permID}|permsid={permName} permvalue={permValue} )...

        Adds a set of specified permissions to a channel. Multiple permissions can be
        added by providing the two parameters of each permission. A permission can be
        specified by permid or permsid.

        Example::

           channeladdperm cid=16 permsid=i_client_needed_join_power permvalue=50
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channeladdperm(
            ...     cid=12, permsid="i_client_needed_join_power", permvalue=50)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        uparams[0][u"permvalue"] = permvalue
        return self._return_proxy(u"channeladdperm", cparams, uparams, options)

    def channelclientaddperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        permvalue = _3to2kwargs['permvalue']; del _3to2kwargs['permvalue']
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channelclientaddperm cid={channelID} cldbid={clientDBID} ( permid={permID}|permsid={permName} permvalue={permValue} )...

        Adds a set of specified permissions to a client in a specific channel. Multiple
        permissions can be added by providing the two parameters of each permission. A
        permission can be specified by permid or permsid.

        Example::

           channelclientaddperm cid=12 cldbid=3 permsid=i_icon_id permvalue=100
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelclientaddperm(
            ...     cid=12, cldbid=3, permsid="i_icon_id", permvalue=100)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        uparams[0][u"permvalue"] = permvalue
        return self._return_proxy(u"channelclientaddperm", cparams, uparams, options)

    def channelclientdelperm(self, **_3to2kwargs):
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channelclientdelperm cid={channelID} cldbid={clientDBID} permid={permID}|permsid={permName}...

        Removes a set of specified permissions from a client in a specific channel.
        Multiple permissions can be removed at once. A permission can be specified
        by permid or permsid.

        Example::

           channelclientdelperm cid=12 cldbid=3 permsid=i_icon_id|permsid=b_icon_manage
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelclientdelperm(
            ...     cid=12, cldbid=3, permsid="i_icon_id")
            ...
            >>> ts3cmd.channelclientdelperm(
            ...     cid=12, cldbid=3, permsid="b_icon_manage")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        return self._return_proxy(u"channelclientdelperm", cparams, uparams, options)

    def channelclientpermlist(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = False
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channelclientpermlist cid={channelID} cldbid={clientDBID} [-permsid]

        Displays a list of permissions defined for a client in a specific channel.

        Example::

           channelclientpermlist cid=12 cldbid=3
           cid=12 cldbid=3 permid=4353 permvalue=1 permnegated=0 permskip=0|permid=17276 permvalue=50 permnegated=0 permskip=0|permid=21415 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelclientpermlist(cid=12, cldbid=3)
            ...
            >>> ts3cmd.channelclientpermlist(cid=12, cldbid=2, permsid=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cldbid"] = cldbid

        if permsid:
            option.append(u"permsid")
        return self._return_proxy(u"channelclientpermlist", cparams, uparams, options)

    def channelcreate(self, **channel_properties):
        channel_name = channel_properties['channel_name']; del channel_properties['channel_name']
        u"""
        Usage::

            channelcreate channel_name={channelName} [channel_properties...]

        Creates a new channel using the given properties and displays its ID.

        Example::

           channelcreate channel_name=My\sChannel channel_topic=My\sTopic
           cid=16
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelcreate(
            ...     channel_name="My Channel", channel_topic="My Topic")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"channel_name"] = channel_name
        cparams.update(channel_properties)
        return self._return_proxy(u"channelcreate", cparams, uparams, options)

    def channeldelete(self, **_3to2kwargs):
        force = _3to2kwargs['force']; del _3to2kwargs['force']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channeldelete cid={channelID} force={1|0}

        Deletes an existing channel by ID. If force is set to 1, the channel will be
        deleted even if there are clients within.

        Example::
           channeldelete cid=16 force=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channeldelete(cid=16, force=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"force"] = force
        return self._return_proxy(u"channeldelete", cparams, uparams, options)

    def channeldelperm(self, **_3to2kwargs):
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channeldelperm cid=123 permid={permID}|permsid={permName}...

        Removes a set of specified permissions from a channel. Multiple permissions
        can be removed at once. A permission can be specified by permid or permsid.

        Example::

           channeldelperm cid=16 permsid=i_icon_id|permsid=i_client_needed_talk_power
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channeldelperm(cid=16, permsid="i_icon_id")
            ...
            >>> ts3cmd.channeldelperm(
            ...     cid=16, permsid="i_client_needed_talk_power")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        return self._return_proxy(u"channeldelperm", cparams, uparams, options)

    def channeledit(self, **channel_properties):
        cid = channel_properties['cid']; del channel_properties['cid']
        u"""
        Usage::

            channeledit cid={channelID} [channel_properties...]

        Changes a channels configuration using given properties.

        Example::

           channeledit cid=15 channel_codec_quality=3 channel_description=My\stext
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channeledit(
            ...     cid=15,
            ...     channel_codec_quality=3,
            ...     channel_description="My text"
            ...     )
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams.update(channel_properties)
        return self._return_proxy(u"channeledit", cparams, uparams, options)

    def channelfind(self, **_3to2kwargs):
        if 'pattern' in _3to2kwargs: pattern = _3to2kwargs['pattern']; del _3to2kwargs['pattern']
        else: pattern = None
        u"""
        Usage::

            channelfind [pattern={channelName}]

        Displays a list of channels matching a given name pattern.

        Example::

           channelfind pattern=default
           cid=15 channel_name=Default\sChannel
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelfind(pattern="default")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"pattern"] = pattern
        return self._return_proxy(u"channelfind", cparams, uparams, options)

    def channelgroupadd(self, **_3to2kwargs):
        if 'type_' in _3to2kwargs: type_ = _3to2kwargs['type_']; del _3to2kwargs['type_']
        else: type_ = None
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        u"""
        Usage::

            channelgroupadd name={groupName} [type={groupDbType}]

        Creates a new channel group using a given name and displays its ID. The
        optional type parameter can be used to create ServerQuery groups and template
        groups.

        Example::

           channelgroupadd name=Channel\sAdmin
           cgid=13
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgroupadd(name="Channel Admin")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"name"] = name
        cparams[u"type"] = type_
        return self._return_proxy(u"channelgroupadd", cparams, uparams, options)

    def channelgroupaddperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        permvalue = _3to2kwargs['permvalue']; del _3to2kwargs['permvalue']
        cgid = _3to2kwargs['cgid']; del _3to2kwargs['cgid']
        u"""
        Usage::

            channelgroupaddperm cgid={groupID} permid={permID} permvalue={permValue}
            channelgroupaddperm cgid={groupID} permsid={permName} permvalue={permValue}

        Adds a set of specified permissions to a channel group. Multiple permissions
        can be added by providing the two parameters of each permission. A permission
        can be specified by permid or permsid.

        Example::

           channelgroupaddperm cgid=78 permsid=b_icon_manage permvalue=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgroupaddperm(
            ...     cgid=78, permsid="b_icon_manage", permvalue=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cgid"] = cgid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        uparams[0][u"permvalue"] = permvalue
        return self._return_proxy(u"channelgroupaddperm", cparams, uparams, options)

    def channelgroupclientlist(self, **_3to2kwargs):
        if 'cgid' in _3to2kwargs: cgid = _3to2kwargs['cgid']; del _3to2kwargs['cgid']
        else: cgid = None
        if 'cldbid' in _3to2kwargs: cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        else: cldbid = None
        if 'cid' in _3to2kwargs: cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        else: cid = None
        u"""
        Usage::

            channelgroupclientlist [cid={channelID}] [cldbid={clientDBID}] [cgid={groupID}]

        Displays all the client and/or channel IDs currently assigned to channel
        groups. All three parameters are optional so you're free to choose the most
        suitable combination for your requirements.

        Example::

           channelgroupclientlist cid=2 cgid=9
           cid=2 cldbid=9 cgid=9|cid=2 cldbid=24 cgid=9|cid=2 cldbid=47 cgid=9
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgroupclientlist(cid=2, cgid=9)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cldbid"] = cldbid
        cparams[u"cgid"] = cgid
        return self._return_proxy(u"channelgroupclientlist", cparams, uparams, options)

    def channelgroupcopy(self, **_3to2kwargs):
        type_ = _3to2kwargs['type_']; del _3to2kwargs['type_']
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        tcgid = _3to2kwargs['tcgid']; del _3to2kwargs['tcgid']
        scgid = _3to2kwargs['scgid']; del _3to2kwargs['scgid']
        u"""
        Usage::

            channelgroupcopy scgid={sourceGroupID} tcgid={targetGroupID} name={groupName} type={groupDbType}

        Creates a copy of the channel group specified with ssgid. If tsgid is set to 0,
        the server will create a new group. To overwrite an existing group, simply set
        tsgid to the ID of a designated target group. If a target group is set, the
        name parameter will be ignored.

        The type parameter can be used to create ServerQuery and template groups.

        Example::

           channelgroupcopy scgid=4 tcgid=0 name=My\sGroup\s(Copy) type=1
           cgid=13
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgroupcopy(
            ...     scgid=4, tcgid=0, name="My Group (Copy)", type_=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"scgid"] = scgid
        cparams[u"tcgid"] = tcgid
        cparams[u"name"] = name
        cparams[u"type"] = type_
        return self._return_proxy(u"channelgroupcopy", cparams, uparams, options)

    def channelgroupdel(self, **_3to2kwargs):
        force = _3to2kwargs['force']; del _3to2kwargs['force']
        cgid = _3to2kwargs['cgid']; del _3to2kwargs['cgid']
        u"""
        Usage::

            channelgroupdel cgid={groupID} force={1|0}

        Deletes a channel group by ID. If force is set to 1, the channel group will be
        deleted even if there are clients within.

        Example::

           channelgroupdel cgid=13
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgroupdel(cgid=13, force=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cgid"] = cgid
        cparams[u"force"] = force
        return self._return_proxy(u"channelgroupdel", cparams, uparams, options)

    def channelgroupdelperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        cgid = _3to2kwargs['cgid']; del _3to2kwargs['cgid']
        u"""
        Usage::

            channelgroupdelperm cgid={groupID} permid={permID}|...
            channelgroupdelperm cgid={groupID} permsid={permName}|...

        Removes a set of specified permissions from the channel group. Multiple
        permissions can be removed at once. A permission can be specified by
        permid or permsid.

        Example::

           channelgroupdelperm cgid=16 permid=17276|permid=21415
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgroupdelperm(
            ...     cgid=16, permsid="i_ft_needed_file_upload_power")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cgid"] = cgid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        return self._return_proxy(u"channelgroupdelperm", cparams, uparams, options)

    def channelgrouplist(self):
        u"""
        Usage::

            channelgrouplist

        Displays a list of channel groups available on the selected virtual server.

        Example::

           channelgrouplist
           cgid=1 name=Channel\sAdmin type=2 iconid=100 savedb=1|cgid=2 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgrouplist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"channelgrouplist", cparams, uparams, options)

    def channelgrouppermlist(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = False
        cgid = _3to2kwargs['cgid']; del _3to2kwargs['cgid']
        u"""
        Usage::

            channelgrouppermlist cgid={groupID} [-permsid]

        Displays a list of permissions assigned to the channel group specified
        with cgid.

        Example::

           channelgrouppermlist cgid=13
           permid=8470 permvalue=1 permnegated=0 permskip=0|permid=8475 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgrouppermlist(cgid=13, permsid=False)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cgid"] = cgid

        if permsid:
            options.append(u"permsid")
        return self._return_proxy(u"channelgrouppermlist", cparams, uparams, options)

    def channelgrouprename(self, **_3to2kwargs):
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        cgid = _3to2kwargs['cgid']; del _3to2kwargs['cgid']
        u"""
        Usage::

            channelgrouprename cgid={groupID} name={groupName}

        Changes the name of a specified channel group.

        Example::

           channelgrouprename cgid=13 name=New\sName
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelgrouprename(cgid=13, name="New name")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cgid"] = cgid
        cparams[u"name"] = name
        return self._return_proxy(u"channelgrouprename", cparams, uparams, options)

    def channelinfo(self, **_3to2kwargs):
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channelinfo cid={channelID}

        Displays detailed configuration information about a channel including ID,
        topic, description, etc.

        Example::

           channelinfo cid=1
           channel_name=Default\sChannel channel_topic=No\s[b]topic[\/b]\shere channel_description=Welcome ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelinfo(cid=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        return self._return_proxy(u"channelinfo", cparams, uparams, options)

    def channellist(self, **_3to2kwargs):
        if 'secondsempty' in _3to2kwargs: secondsempty = _3to2kwargs['secondsempty']; del _3to2kwargs['secondsempty']
        else: secondsempty = False
        if 'icon' in _3to2kwargs: icon = _3to2kwargs['icon']; del _3to2kwargs['icon']
        else: icon = False
        if 'limits' in _3to2kwargs: limits = _3to2kwargs['limits']; del _3to2kwargs['limits']
        else: limits = False
        if 'voice' in _3to2kwargs: voice = _3to2kwargs['voice']; del _3to2kwargs['voice']
        else: voice = False
        if 'flags' in _3to2kwargs: flags = _3to2kwargs['flags']; del _3to2kwargs['flags']
        else: flags = False
        if 'topic' in _3to2kwargs: topic = _3to2kwargs['topic']; del _3to2kwargs['topic']
        else: topic = False
        u"""
        Usage::

            channellist [-topic] [-flags] [-voice] [-limits] [-icon] [-secondsempty]

        Displays a list of channels created on a virtual server including their ID,
        order, name, etc. The output can be modified using several command options.

        Example::

           channellist -topic
           cid=15 pid=0 channel_order=0 channel_name=Default\sChannel channel_topic=No\s[b]topic[\/b] total_clients=2|cid=16 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channellist(topic=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        if topic:
            options.append(u"topic")
        if flags:
            options.append(u"flags")
        if voice:
            options.append(u"voice")
        if limits:
            options.append(u"limits")
        if icon:
            options.append(u"icon")
        if secondsempty:
            options.append(u"secondsempty")
        return self._return_proxy(u"channellist", cparams, uparams, options)

    def channelmove(self, **_3to2kwargs):
        if 'order' in _3to2kwargs: order = _3to2kwargs['order']; del _3to2kwargs['order']
        else: order = None
        cpid = _3to2kwargs['cpid']; del _3to2kwargs['cpid']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channelmove cid={channelID} cpid={channelParentID} [order={channelSortOrder}]

        Moves a channel to a new parent channel with the ID cpid. If order is
        specified, the channel will be sorted right under the channel with the
        specified ID. If order is set to 0, the channel will be sorted right below
        the new parent.

        Example::
           channelmove cid=16 cpid=1 order=0
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelmove(cid=16, cpid=1, order=0)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cpid"] = cpid
        cparams[u"order"] = order
        return self._return_proxy(u"channelmove", cparams, uparams, options)

    def channelpermlist(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = False
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            channelpermlist cid={channelID} [-permsid]

        Displays a list of permissions defined for a channel.

        Example::

           channelpermlist cid=2
           cid=2 permid=4353 permvalue=1 permnegated=0 permskip=0|permid=17276...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.channelpermlist(cid=2)
            ...
            >>> ts3cmd.channelpermlist(cid=2, permsid=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid

        if permsid:
            options.append(u"permsid")
        return self._return_proxy(u"channelpermlist", cparams, uparams, options)

    def clientaddperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        permskip = _3to2kwargs['permskip']; del _3to2kwargs['permskip']
        permvalue = _3to2kwargs['permvalue']; del _3to2kwargs['permvalue']
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            clientaddperm cldbid={clientDBID} permid={permID} permvalue={permValue} permskip={1|0}|...
            clientaddperm cldbid={clientDBID} permsid={permName} permvalue={permValue} permskip={1|0}|...

        Adds a set of specified permissions to a client. Multiple permissions can be
        added by providing the three parameters of each permission. A permission can
        be specified by permid or permsid.

        Example::

           clientaddperm cldbid=16 permsid=i_client_talk_power permvalue=5 permskip=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientaddperm(
            ...     cldbid=16, permsid="i_client_talk_power", permvalue=5,
            ...     permskip=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        uparams[0][u"permvalue"] = permvalue
        uparams[0][u"permskip"] = permskip
        return self._return_proxy(u"clientaddperm", cparams, uparams, options)

    def clientdbdelete(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            clientdbdelete cldbid={clientDBID}

        Deletes a clients properties from the database.

        Example::

           clientdbdelete cldbid=56
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientdbdelete(cldbid=56)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"clientdbdelete", cparams, uparams, options)

    def clientdbedit(self, **client_properties):
        cldbid = client_properties['cldbid']; del client_properties['cldbid']
        u"""
        Usage::

            clientdbedit cldbid={clientDBID} [client_properties...]

        Changes a clients settings using given properties.

        Example::

           clientdbedit cldbid=56 client_description=Best\sguy\sever!
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientdbedit(
            ...     cldbid=56, client_description="Best guy ever!")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid
        cparams.update(client_properties)
        return self._return_proxy(u"clientdbedit", cparams, uparams, options)

    def clientdbfind(self, **_3to2kwargs):
        if 'uid' in _3to2kwargs: uid = _3to2kwargs['uid']; del _3to2kwargs['uid']
        else: uid = False
        pattern = _3to2kwargs['pattern']; del _3to2kwargs['pattern']
        u"""
        Usage::

            clientdbfind pattern={clientName|clientUID} [-uid]

        Displays a list of client database IDs matching a given pattern. You can either
        search for a clients last known nickname or his unique identity by using the
        -uid option.

        Example::

           clientdbfind pattern=sven
           cldbid=56
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientdbfind("sven")
            ...
            >>> ts3cmd.clientdbfind("sven", uid=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"pattern"] = pattern

        if uid:
            options.append(u"uid")
        return self._return_proxy(u"clientdbfind", cparams, uparams, options)

    def clientdbinfo(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            clientdbinfo cldbid={clientDBID}

        Displays detailed database information about a client including unique ID, creation date, etc.

        Example::

            clientdbinfo cldbid=2
            client_unique_identifier=5rRxyxEjd+Kk/MvPRfqZdSI0teA= client_nickname=dante696 client_database_id=2 client_created=1279002103 ...
            error id=0 msg=ok

        Example::

            >>> ts3cmd.clientdbinfo(cldbid=2)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"clientdbinfo", cparams, uparams, options)

    def clientdblist(self, **_3to2kwargs):
        if 'count' in _3to2kwargs: count = _3to2kwargs['count']; del _3to2kwargs['count']
        else: count = False
        if 'duration' in _3to2kwargs: duration = _3to2kwargs['duration']; del _3to2kwargs['duration']
        else: duration = None
        if 'start' in _3to2kwargs: start = _3to2kwargs['start']; del _3to2kwargs['start']
        else: start = None
        u"""
        Usage::

            clientdblist [start={offset}] [duration={limit}] [-count]

        Displays a list of client identities known by the server including their
        database ID, last nickname, etc.

        Example::

           clientdblist
           cldbid=7 client_unique_identifier=DZhdQU58qyooEK4Fr8Ly738hEmc=
           client_nickname=MuhChy client_created=1259147468 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientdblist()
            ...
            >>> ts3cmd.clientdblist(count=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"start"] = start
        cparams[u"duration"] = duration

        if count:
            options.append(u"count")
        return self._return_proxy(u"clientdblist", cparams, uparams, options)

    def clientdelperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            channeldelperm cldbid={clientDBID} permid={permID}|permsid={permName}...

        Removes a set of specified permissions from a client. Multiple permissions
        can be removed at once. A permission can be specified by permid or permsid.

        Example::

           clientdelperm cldbid=16 permsid=i_icon_id|permsid=b_icon_manage
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientdelperm(cldbid=16, permsid="i_icon_id")
            ...
            >>> ts3cmd.clientdelperm(cldbid=16, permsid="b_icon_manage")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        return self._return_proxy(u"clientdelperm", cparams, uparams, options)

    def clientedit(self, **client_properties):
        clid = client_properties['clid']; del client_properties['clid']
        u"""
        Usage::

            clientedit clid={clientID} [client_properties...]

        Changes a clients settings using given properties.

        Example::

           clientedit clid=10 client_description=Best\sguy\sever!
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientedit(clid=10, client_description="Best guy ever!")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"clid"] = clid
        cparams.update(client_properties)
        return self._return_proxy(u"clientedit", cparams, uparams, options)

    def clientfind(self, **_3to2kwargs):
        pattern = _3to2kwargs['pattern']; del _3to2kwargs['pattern']
        u"""
        Usage::

            clientfind pattern={clientName}

        Displays a list of clients matching a given name pattern.

        Example::

           clientfind pattern=sven
           clid=7 client_nickname=Sven
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientfind(pattern="sven")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"pattern"] = pattern
        return self._return_proxy(u"clientfind", cparams, uparams, options)

    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################

    def clientgetdbidfromuid(self, **_3to2kwargs):
        cluid = _3to2kwargs['cluid']; del _3to2kwargs['cluid']
        u"""
        Usage::

            clientgetdbidfromuid cluid={clientUID}

        Displays the database ID matching the unique identifier specified by cluid.

        Example::

           clientgetdbidfromuid cluid=dyjxkshZP6bz0n3bnwFQ1CkwZOM=
           cluid=dyjxkshZP6bz0n3bnwFQ1CkwZOM= cldbid=32
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientgetdbidfromuid(cluid="dyjxkshZP6bz0n3bnwFQ1CkwZOM")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cluid"] = cluid
        return self._return_proxy(u"clientgetdbidfromuid", cparams, uparams, options)

    def clientgetids(self, **_3to2kwargs):
        cluid = _3to2kwargs['cluid']; del _3to2kwargs['cluid']
        u"""
        Usage::

            clientgetids cluid={clientUID}

        Displays all client IDs matching the unique identifier specified by cluid.

        Example::

           clientgetids cluid=dyjxkshZP6bz0n3bnwFQ1CkwZOM=
           cluid=dyjxkshZP6bz0n3bnwFQ1CkwZOM= clid=1 name=Janko
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientgetids(cluid="dyjxkshZP6bz0n3bnwFQ1CkwZOM")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cluid"] = cluid
        return self._return_proxy(u"clientgetids", cparams, uparams, options)

    def clientgetnamefromdbid(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            clientgetnamefromdbid cldbid={clientDBID}

        Displays the unique identifier and nickname matching the database ID specified
        by cldbid.

        Example::

           clientgetnamefromdbid cldbid=32
           cluid=dyjxkshZP6bz0n3bnwFQ1CkwZOM= cldbid=32 name=Janko
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientgetnamefromdbid(cldbid=32)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"clientgetnamefromdbid", cparams, uparams, options)

    def clientgetnamefromuid(self, **_3to2kwargs):
        cluid = _3to2kwargs['cluid']; del _3to2kwargs['cluid']
        u"""
        Usage::

            clientgetnamefromuid cluid={clientUID}

        Displays the database ID and nickname matching the unique identifier specified
        by cluid.

        Example::

           clientgetnamefromuid cluid=dyjxkshZP6bz0n3bnwFQ1CkwZOM=
           cluid=dyjxkshZP6bz0n3bnwFQ1CkwZOM= cldbid=32 name=Janko
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientgetnamefromuid(
            ...     cluid="dyjxkshZP6bz0n3bnwFQ1CkwZOM")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cluid"] = cluid
        return self._return_proxy(u"clientgetnamefromuid", cparams, uparams, options)

    def clientgetuidfromclid(self, **_3to2kwargs):
        clid = _3to2kwargs['clid']; del _3to2kwargs['clid']
        u"""
        Usage::

            clientgetuidfromclid clid={clientID}

        Displays the unique identifier matching the clientID specified by clid.

        Example::

           clientgetuidfromclid clid=8
           clid=8 cluid=yXM6PUfbCcPU+joxIFek1xOQwwQ= nickname=MuhChy1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientgetuidfromclid(clid=8)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"clid"] = clid
        return self._return_proxy(u"clientgetuidfromclid", cparams, uparams, options)

    def clientinfo(self, **_3to2kwargs):
        clid = _3to2kwargs['clid']; del _3to2kwargs['clid']
        u"""
        Usage::

            clientinfo clid={clientID}

        Displays detailed configuration information about a client including unique ID,
        nickname, client version, etc.

        Example::

           clientinfo clid=6
           client_unique_identifier=P5H2hrN6+gpQI4n\/dXp3p17vtY0= client_nickname=Rabe
           client_version=3.0.0-alpha24\s[Build:\s8785]...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientinfo(clid=6)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"clid"] = clid
        return self._return_proxy(u"clientinfo", cparams, uparams, options)

    def clientkick(self, **_3to2kwargs):
        if 'reasonmsg' in _3to2kwargs: reasonmsg = _3to2kwargs['reasonmsg']; del _3to2kwargs['reasonmsg']
        else: reasonmsg = None
        reasonid = _3to2kwargs['reasonid']; del _3to2kwargs['reasonid']
        clid = _3to2kwargs['clid']; del _3to2kwargs['clid']
        u"""
        Usage::

            clientkick reasonid={4|5} [reasonmsg={text}] clid={clientID}...

        Kicks one or more clients specified with clid from their currently joined
        channel or from the server, depending on reasonid. The reasonmsg parameter
        specifies a text message sent to the kicked clients. This parameter is optional
        and may only have a maximum of 40 characters.

        Available reasonid values are:
            * 4: Kick the client from his current channel into the default channel
            * 5: Kick the client from the server

        Example::

           clientkick reasonid=4 reasonmsg=Go\saway! clid=5|clid=6
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientkick(reasonid=4, reasonmsg="Go away!", clid=5)
            ...
            >>> ts3cmd.clientkick(reasonid=4, reasonmsg="Go away!", clid=6)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"reasonid"] = reasonid
        cparams[u"reasonmsg"] = reasonmsg

        uparams.append(OrderedDict())
        uparams[0][u"clid"] = clid
        return self._return_proxy(u"clientkick", cparams, uparams, options)

    def clientlist(self, **_3to2kwargs):
        if 'ip' in _3to2kwargs: ip = _3to2kwargs['ip']; del _3to2kwargs['ip']
        else: ip = False
        if 'country' in _3to2kwargs: country = _3to2kwargs['country']; del _3to2kwargs['country']
        else: country = False
        if 'info' in _3to2kwargs: info = _3to2kwargs['info']; del _3to2kwargs['info']
        else: info = False
        if 'groups' in _3to2kwargs: groups = _3to2kwargs['groups']; del _3to2kwargs['groups']
        else: groups = False
        if 'times' in _3to2kwargs: times = _3to2kwargs['times']; del _3to2kwargs['times']
        else: times = False
        if 'voice' in _3to2kwargs: voice = _3to2kwargs['voice']; del _3to2kwargs['voice']
        else: voice = False
        if 'away' in _3to2kwargs: away = _3to2kwargs['away']; del _3to2kwargs['away']
        else: away = False
        if 'uid' in _3to2kwargs: uid = _3to2kwargs['uid']; del _3to2kwargs['uid']
        else: uid = False
        u"""
        Usage::

            clientlist [-uid] [-away] [-voice] [-times] [-groups] [-info] [-country] [-ip]

        Displays a list of clients online on a virtual server including their ID,
        nickname, status flags, etc. The output can be modified using several command
        options. Please note that the output will only contain clients which are
        currently in channels you're able to subscribe to.

        Example::

           clientlist -away
           clid=5 cid=7 client_database_id=40 client_nickname=ScP client_type=0
           client_away=1 client_away_message=not\shere|clid=6...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientlist(away=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        if uid:
            options.append(u"uid")
        if away:
            options.append(u"away")
        if voice:
            options.append(u"voice")
        if times:
            options.append(u"times")
        if groups:
            options.append(u"groups")
        if info:
            options.append(u"info")
        if country:
            options.append(u"country")
        if ip:
            options.append(u"ip")
        return self._return_proxy(u"clientlist", cparams, uparams, options)

    def clientmove(self, **_3to2kwargs):
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        clid = _3to2kwargs['clid']; del _3to2kwargs['clid']
        u"""
        Usage::

            clientmove cid={channelID} [cpw={channelPassword}] clid={clientID}...

        Moves one or more clients specified with clid to the channel with ID cid. If
        the target channel has a password, it needs to be specified with cpw. If the
        channel has no password, the parameter can be omitted.

        Example::

           clientmove cid=3 clid=5|clid=6
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientmove(cid=3, clid=5)
            ...
            >>> ts3cmd.clientmove(cid=3, clid=6)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cpw"] = cpw

        uparams.append(OrderedDict())
        uparams[0][u"clid"] = clid
        return self._return_proxy(u"clientmove", cparams, uparams, options)

    def clientpermlist(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = False
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            clientpermlist cldbid={clientDBID} [-permsid]

        Displays a list of permissions defined for a client.

        Example::
           clientpermlist cldbid=2
           cldbid=2 permid=4353 permvalue=1 permnegated=0 permskip=0|permid=17276...
           error id=0 msg=ok

        Example::

            >>> ts3example.clientpermlist(cldbid=2)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid

        if permsid:
            options.append(u"permsid")
        return self._return_proxy(u"clientpermlist", cparams, uparams, options)

    def clientpoke(self, **_3to2kwargs):
        clid = _3to2kwargs['clid']; del _3to2kwargs['clid']
        msg = _3to2kwargs['msg']; del _3to2kwargs['msg']
        u"""
        Usage::

            clientpoke msg={txt} clid={clientID}

        Sends a poke message to the client specified with clid.

        Example::

           clientpoke msg=Wake\sup! clid=5
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientpoke(msg="Wake up", clid=5)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"msg"] = msg
        cparams[u"clid"] = clid
        return self._return_proxy(u"clientpoke", cparams, uparams, options)

    def clientsetserverquerylogin(self, **_3to2kwargs):
        client_login_name = _3to2kwargs['client_login_name']; del _3to2kwargs['client_login_name']
        u"""
        Usage::

            clientsetserverquerylogin client_login_name={username}

        Updates your own ServerQuery login credentials using a specified username. The
        password will be auto-generated.

        Example::

           clientsetserverquerylogin client_login_name=admin
           client_login_password=+r\/TQqvR
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientsetserverquerylogin(client_login_name="admin")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"client_login_name"] = client_login_name
        return self._return_proxy(u"clientsetserverquerylogin", cparams, uparams, options)

    def clientupdate(self, **client_properties):
        u"""
        Usage::

            clientupdate [client_properties...]

        Change your ServerQuery clients settings using given properties.

        Example::

           clientupdate client_nickname=ScP\s(query)
           error id=0 msg=ok

        Example::

            >>> ts3cmd.clientupdate(client_nickname="ScP (query)")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams.update(client_properties)
        return self._return_proxy(u"clientupdate", cparams, uparams, options)

    def complainadd(self, **_3to2kwargs):
        message = _3to2kwargs['message']; del _3to2kwargs['message']
        tcldbid = _3to2kwargs['tcldbid']; del _3to2kwargs['tcldbid']
        u"""
        Usage::

            complainadd tcldbid={targetClientDBID} message={text}

        Submits a complaint about the client with database ID tcldbid to the server.

        Example::

           complainadd tcldbid=3 message=Bad\sguy!
           error id=0 msg=ok

        Example::

            >>> ts3cmd.complainadd(tcldbid=3, message="Bad guy!")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"tcldbid"] = tcldbid
        cparams[u"message"] = message
        return self._return_proxy(u"complainadd", cparams, uparams, options)

    def complaindel(self, **_3to2kwargs):
        fcldbid = _3to2kwargs['fcldbid']; del _3to2kwargs['fcldbid']
        tcldbid = _3to2kwargs['tcldbid']; del _3to2kwargs['tcldbid']
        u"""
        Usage::

            complaindel tcldbid={targetClientDBID} fcldbid={fromClientDBID}

        Deletes the complaint about the client with database ID tcldbid submitted by
        the client with database ID fcldbid from the server.

        Example::

           complaindel tcldbid=3 fcldbid=4
           error id=0 msg=ok

        Example::

            >>> ts3cmd.complaindel(tcldbid=3, fcldbid=4)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"tcldbid"] = tcldbid
        cparams[u"fcldbid"] = fcldbid
        return self._return_proxy(u"complaindel", cparams, uparams, options)

    def complaindelall(self, **_3to2kwargs):
        tcldbid = _3to2kwargs['tcldbid']; del _3to2kwargs['tcldbid']
        u"""
        Usage::

            complaindelall tcldbid={targetClientDBID}

        Deletes all complaints about the client with database ID tcldbid from
        the server.

        Example::

           complaindelall tcldbid=3
           error id=0 msg=ok

        Example::

            >>> ts3cmd.complaindelall(tcldbid=3)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"tcldbid"] = tcldbid
        return self._return_proxy(u"complaindelall", cparams, uparams, options)

    def complainlist(self, **_3to2kwargs):
        if 'tcldbid' in _3to2kwargs: tcldbid = _3to2kwargs['tcldbid']; del _3to2kwargs['tcldbid']
        else: tcldbid = None
        u"""
        Usage::

            complainlist [tcldbid={targetClientDBID}]

        Displays a list of complaints on the selected virtual server. If tcldbid is
        specified, only complaints about the targeted client will be shown.

        Example::

           complainlist tcldbid=3
           tcldbid=3 tname=Julian fcldbid=56 fname=Sven message=Bad\sguy!...
           error id=0 msg=ok

        Example::

            >>> ts3.complainlist(tcldbid=3)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"tcldbid"] = tcldbid
        return self._return_proxy(u"complainlist", cparams, uparams, options)

    def custominfo(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            custominfo cldbid={clientDBID}

        Displays a list of custom properties for the client specified with cldbid.

        Example::

           custominfo cldbid=3
           cldbid=3 ident=forum_account value=ScP|ident=forum_id value=123
           error id=0 msg=ok

        Example::

            >>> ts3cmd.custominfo(cldbid=3)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"custominfo", cparams, uparams, options)

    def customsearch(self, **_3to2kwargs):
        pattern = _3to2kwargs['pattern']; del _3to2kwargs['pattern']
        ident = _3to2kwargs['ident']; del _3to2kwargs['ident']
        u"""
        Usage::

            customsearch ident={ident} pattern={pattern}

        Searches for custom client properties specified by ident and value. The value
        parameter can include regular characters and SQL wildcard characters (e.g. %).

        Example::

           customsearch ident=forum_account pattern=%ScP%
           cldbid=2 ident=forum_account value=ScP
           error id=0 msg=ok

        Example::

            >>> ts3cmd.customsearch(ident="forum_account", pattern="%ScP")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"ident"] = ident
        cparams[u"pattern"] = pattern
        return self._return_proxy(u"customsearch", cparams, uparams, options)

    def ftcreatedir(self, **_3to2kwargs):
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        dirname = _3to2kwargs['dirname']; del _3to2kwargs['dirname']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            ftcreatedir cid={channelID} cpw={channelPassword} dirname={dirPath}

        Creates new directory in a channels file repository.

        Example::

           ftcreatedir cid=2 cpw= dirname=\/My\sDirectory
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftcreatedir(cid=2, dirname="/My Directory")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cpw"] = cpw if cpw is not None else u""
        cparams[u"dirname"] = dirname
        return self._return_proxy(u"ftcreatedir", cparams, uparams, options)

    def ftdeletefile(self, **_3to2kwargs):
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            ftdeletefile cid={channelID} cpw={channelPassword} name={filePath}...

        Deletes one or more files stored in a channels file repository.

        Example::

           ftdeletefile cid=2 cpw= name=\/Pic1.PNG|name=\/Pic2.PNG
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftdeletefile(cid=2, name="/Pic1.PNG")
            ...
            >>> ts3cmd.ftdeletefile(cid=2, name="/Pic2.PNG")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cpw"] = cpw if cpw is not None else unicode()

        uparams.append(OrderedDict())
        uparams[0][u"name"] = name
        return self._return_proxy(u"ftdeletefile", cparams, uparams, options)

    def ftgetfileinfo(self, **_3to2kwargs):
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        u"""
        Usage::

            ftgetfileinfo cid={channelID} cpw={channelPassword} name={filePath}...

        Displays detailed information about one or more specified files stored in a
        channels file repository.

        Example::

           ftgetfileinfo cid=2 cpw= name=\/Pic1.PNG|cid=2 cpw= name=\/Pic2.PNG
           cid=2 path=\/ name=Stuff size=0 datetime=1259415210 type=0|name=Pic1.PNG
           size=563783 datetime=1259425462 type=1|name=Pic2.PNG...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftgetfileinfo(cid=2, name="/Pic1.PNG")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        uparams.append(OrderedDict())
        uparams[0][u"cid"] = cid
        uparams[0][u"cpw"] = cpw if cpw is not None else unicode()
        uparams[0][u"name"] = name
        return self._return_proxy(u"ftgetfileinfo", cparams, uparams, options)

    def ftgetfilelist(self, **_3to2kwargs):
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        path = _3to2kwargs['path']; del _3to2kwargs['path']
        u"""
        Usage::

            ftgetfilelist cid={channelID} cpw={channelPassword} path={filePath}

        Displays a list of files and directories stored in the specified channels file
        repository.

        Example::

           ftgetfilelist cid=2 cpw= path=\/
           cid=2 path=\/ name=Stuff size=0 datetime=1259415210 type=0|name=Pic1.PNG
           size=563783 datetime=1259425462 type=1|name=Pic2.PNG...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftgetfilelist(cid=2, path="/")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cpw"] = cpw if cpw is not None else unicode()
        cparams[u"path"] = path
        return self._return_proxy(u"ftgetfilelist", cparams, uparams, options)

    def ftinitdownload(self, **_3to2kwargs):
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        seekpos = _3to2kwargs['seekpos']; del _3to2kwargs['seekpos']
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        clientftfid = _3to2kwargs['clientftfid']; del _3to2kwargs['clientftfid']
        u"""
        Usage::

            ftinitdownload clientftfid={clientFileTransferID} name={filePath}
                           cid={channelID} cpw={channelPassword}
                           seekpos={seekPosition}

        Initializes a file transfer download. clientftfid is an arbitrary ID to
        identify the file transfer on client-side. On success, the server generates
        a new ftkey which is required to start downloading the file through
        TeamSpeak 3's file transfer interface.

        Example::

           ftinitdownload clientftfid=1 name=\/image.iso cid=5 cpw= seekpos=0
           clientftfid=1 serverftfid=7 ftkey=NrOga\/4d2GpYC5oKgxuclTO37X83ca\/1 port=...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftinitdownload(
            ...     clientftfid=1, name="/image.iso", cid=5, seekpos=0)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"clientftfid"] = clientftfid
        cparams[u"name"] = name
        cparams[u"cid"] = cid
        cparams[u"cpw"] = cpw if cpw is not None else unicode()
        cparams[u"seekpos"] = seekpos
        return self._return_proxy(u"ftinitdownload", cparams, uparams, options)

    def ftinitupload(self, **_3to2kwargs):
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        resume = _3to2kwargs['resume']; del _3to2kwargs['resume']
        overwrite = _3to2kwargs['overwrite']; del _3to2kwargs['overwrite']
        size = _3to2kwargs['size']; del _3to2kwargs['size']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        clientftfid = _3to2kwargs['clientftfid']; del _3to2kwargs['clientftfid']
        u"""
        Usage::

            ftinitupload clientftfid={clientFileTransferID} name={filePath}
                         cid={channelID} cpw={channelPassword} size={fileSize}
                         overwrite={1|0} resume={1|0}

        Initializes a file transfer upload. clientftfid is an arbitrary ID to identify
        the file transfer on client-side. On success, the server generates a new ftkey
        which is required to start uploading the file through TeamSpeak 3's file
        transfer interface.

        Example::

           ftinitupload clientftfid=1 name=\/image.iso cid=5 cpw= size=673460224 overwrite=1 resume=0
           clientftfid=1 serverftfid=6 ftkey=itRNdsIOvcBiBg\/Xj4Ge51ZSrsShHuid port=...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftinitupload(
            ...     clientftfid=1, name="/image.iso", cid=5, size=673460224,
            ...     overwrite=1, resume=0)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"clientftfid"] = clientftfid
        cparams[u"name"] = name
        cparams[u"cid"] = cid
        cparams[u"cpw"] = cpw if cpw is not None else unicode()
        cparams[u"size"] = size
        cparams[u"overwrite"] = overwrite
        cparams[u"resume"] = resume
        return self._return_proxy(u"ftinitupload", cparams, uparams, options)

    def ftlist(self):
        u"""
        Usage::

            ftlist

        Displays a list of running file transfers on the selected virtual server. The
        output contains the path to which a file is uploaded to, the current transfer
        rate in bytes per second, etc.

        Example::

           ftlist
           clid=2 path=files\/virtualserver_1\/channel_5 name=image.iso size=673460224
           sizedone=450756 clientftfid=2 serverftfid=6 sender=0 status=1 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftlist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"ftlist", cparams, uparams, options)

    def ftrenamefile(self, **_3to2kwargs):
        if 'tcpw' in _3to2kwargs: tcpw = _3to2kwargs['tcpw']; del _3to2kwargs['tcpw']
        else: tcpw = None
        if 'tcid' in _3to2kwargs: tcid = _3to2kwargs['tcid']; del _3to2kwargs['tcid']
        else: tcid = None
        if 'cpw' in _3to2kwargs: cpw = _3to2kwargs['cpw']; del _3to2kwargs['cpw']
        else: cpw = None
        newname = _3to2kwargs['newname']; del _3to2kwargs['newname']
        oldname = _3to2kwargs['oldname']; del _3to2kwargs['oldname']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            ftrenamefile cid={channelID} cpw={channelPassword}
                         [tcid={targetChannelID}] [tcpw={targetChannelPassword}]
        	         oldname={oldFilePath} newname={newFilePath}

        Renames a file in a channels file repository. If the two parameters tcid and
        tcpw are specified, the file will be moved into another channels file
        repository.

        Example::

           ftrenamefile cid=2 cpw= tcid=3 tcpw= oldname=\/Pic3.PNG newname=\/Pic3.PNG
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftrenamefile(
            ...     cid=2, tcid=3, oldname="/Pic3.PNG", newname="/Pic3.PNG")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cpw"] = cpw if cpw is not None else unicode()
        cparams[u"tcid"] = tcid
        cparams[u"tcpw"] = tcpw
        cparams[u"oldname"] = oldname
        cparams[u"newname"] = newname
        return self._return_proxy(u"ftrenamefile", cparams, uparams, options)

    def ftstop(self, **_3to2kwargs):
        delete = _3to2kwargs['delete']; del _3to2kwargs['delete']
        serverftfid = _3to2kwargs['serverftfid']; del _3to2kwargs['serverftfid']
        u"""
        Usage::

            ftstop serverftfid={serverFileTransferID} delete={1|0}

        Stops the running file transfer with server-side ID serverftfid.

        Example::

           ftstop serverftfid=2 delete=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.ftstop(serverftfid=2, delete=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"serverftfid"] = serverftfid
        cparams[u"delete"] = delete
        return self._return_proxy(u"ftstop", cparams, uparams, options)

    def gm(self, **_3to2kwargs):
        msg = _3to2kwargs['msg']; del _3to2kwargs['msg']
        u"""
        Usage::

            gm msg={text}

        Sends a text message to all clients on all virtual servers in the TeamSpeak 3
        Server instance.

        Example::

           gm msg=Hello\sWorld!
           error id=0 msg=ok

        Example::

            >>> ts3cmd.gm(msg="Hello World")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"msg"] = msg
        return self._return_proxy(u"gm", cparams, uparams, options)

    def help(self, **_3to2kwargs):
        if 'cmd' in _3to2kwargs: cmd = _3to2kwargs['cmd']; del _3to2kwargs['cmd']
        else: cmd = None
        u"""
        TeamSpeak 3 Server :: ServerQuery
        (c) TeamSpeak Systems GmbH

        ServerQuery is a command-line interface built into the TeamSpeak 3 Server which
        allows powerful scripting and automation tools to be built based on the exact
        same instruction set and functionality provided by the TeamSpeak 3 Client. For
        example, you can use scripts to automate the management of virtual servers or
        nightly backups. In short, you can perform operations more efficiently by using
        ServerQuery scripts than you can by using a user interface.

        Command Overview::

           help                        | read help files
           login                       | authenticate with the server
           logout                      | deselect virtual server and log out
           quit                        | close connection
           use                         | select virtual server
           banadd                      | create a ban rule
           banclient                   | ban a client
           bandelall                   | delete all ban rules
           bandel                      | delete a ban rule
           banlist                     | list ban rules on a virtual server
           bindinglist                 | list IP addresses used by the server instance
           channeladdperm              | assign permission to channel
           channelclientaddperm        | assign permission to channel-client combi
           channelclientdelperm        | remove permission from channel-client combi
           channelclientpermlist       | list channel-client specific permissions
           channelcreate               | create a channel
           channeldelete               | delete a channel
           channeldelperm              | remove permission from channel
           channeledit                 | change channel properties
           channelfind                 | find channel by name
           channelgroupadd             | create a channel group
           channelgroupaddperm         | assign permission to channel group
           channelgroupclientlist      | find channel groups by client ID
           channelgroupcopy            | copy a channel group
           channelgroupdel             | delete a channel group
           channelgroupdelperm         | remove permission from channel group
           channelgrouplist            | list channel groups
           channelgrouppermlist        | list channel group permissions
           channelgrouprename          | rename a channel group
           channelinfo                 | display channel properties
           channellist                 | list channels on a virtual server
           channelmove                 | move channel to new parent
           channelpermlist             | list channel specific permissions
           clientaddperm               | assign permission to client
           clientdbdelete              | delete client database properties
           clientdbedit                | change client database properties
           clientdbfind                | find client database ID by nickname or UID
           clientdbinfo                | display client database properties
           clientdblist                | list known client UIDs
           clientdelperm               | remove permission from client
           clientedit                  | change client properties
           clientfind                  | find client by nickname
           clientgetdbidfromuid        | find client database ID by UID
           clientgetids                | find client IDs by UID
           clientgetnamefromdbid       | find client nickname by database ID
           clientgetnamefromuid        | find client nickname by UID
           clientgetuidfromclid        | find client UID by client ID
           clientinfo                  | display client properties
           clientkick                  | kick a client
           clientlist                  | list clients online on a virtual server
           clientmove                  | move a client
           clientpermlist              | list client specific permissions
           clientpoke                  | poke a client
           clientsetserverquerylogin   | set own login credentials
           clientupdate                | set own properties
           complainadd                 | create a client complaint
           complaindelall              | delete all client complaints
           complaindel                 | delete a client complaint
           complainlist                | list client complaints on a virtual server
           custominfo                  | display custom client properties
           customsearch                | search for custom client properties
           ftcreatedir                 | create a directory
           ftdeletefile                | delete a file
           ftgetfileinfo               | display details about a file
           ftgetfilelist               | list files stored in a channel filebase
           ftinitdownload              | init a file download
           ftinitupload                | init a file upload
           ftlist                      | list active file transfers
           ftrenamefile                | rename a file
           ftstop                      | stop a file transfer
           gm                          | send global text message
           hostinfo                    | display server instance connection info
           instanceedit                | change server instance properties
           instanceinfo                | display server instance properties
           logadd                      | add custom entry to log
           logview                     | list recent log entries
           messageadd                  | send an offline message
           messagedel                  | delete an offline message from your inbox
           messageget                  | display an offline message from your inbox
           messagelist                 | list offline messages from your inbox
           messageupdateflag           | mark an offline message as read
           permfind                    | find permission assignments by ID
           permget                     | display client permission value for yourself
           permidgetbyname             | find permission ID by name
           permissionlist              | list permissions available
           permoverview                | display client permission overview
           permreset                   | delete all server and channel groups and restore default permissions
           privilegekeyadd             | creates a new privilege key
           privilegekeydelete          | delete an existing privilege key
           privilegekeylist            | list all existing privilege keys on this server
           privilegekeyuse             | use a privilege key
           sendtextmessage             | send text message
           servercreate                | create a virtual server
           serverdelete                | delete a virtual server
           serveredit                  | change virtual server properties
           servergroupaddclient        | add client to server group
           servergroupadd              | create a server group
           servergroupaddperm          | assign permissions to server group
           servergroupautoaddperm      | globally assign permissions to server groups
           servergroupbyclientid       | get all server groups of specified client
           servergroupclientlist       | list clients in a server group
           servergroupcopy             | create a copy of an existing server group
           servergroupdelclient        | remove client from server group
           servergroupdel              | delete a server group
           servergroupdelperm          | remove permissions from server group
           servergroupautodelperm      | globally remove permissions from server group
           servergrouplist             | list server groups
           servergrouppermlist         | list server group permissions
           servergrouprename           | rename a server group
           servergroupsbyclientid      | find server groups by client ID
           serveridgetbyport           | find database ID by virtual server port
           serverinfo                  | display virtual server properties
           serverlist                  | list virtual servers
           servernotifyregister        | register for event notifications
           servernotifyunregister      | unregister from event notifications
           serverprocessstop           | shutdown server process
           serverrequestconnectioninfo | display virtual server connection info
           serversnapshotcreate        | create snapshot of a virtual server
           serversnapshotdeploy        | deploy snapshot of a virtual server
           serverstart                 | start a virtual server
           servertemppasswordadd       | create a new temporary server password
           servertemppassworddel       | delete an existing temporary server password
           servertemppasswordlist      | list all existing temporary server passwords
           serverstop                  | stop a virtual server
           setclientchannelgroup       | set a clients channel group
           tokenadd                    | create a privilege key (token)
           tokendelete                 | delete a privilege key (token)
           tokenlist                   | list privilege keys (tokens) available
           tokenuse                    | use a privilege key (token)
           version                     | display version information
           whoami                      | display current session info

        Example::

            >>> ts3cmd.help()
            ...
            >>> ts3cmd.help(cmd="whoami")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u""] = cmd
        return self._return_proxy(u"help", cparams, uparams, options)

    def hostinfo(self):
        u"""
        Usage::

            hostinfo

        Displays detailed configuration information about the server instance including
        uptime, number of virtual servers online, traffic information, etc.

        Example::

           hostinfo
           virtualservers_running_total=3 virtualservers_total_maxclients=384 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.hostinfo()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"hostinfo", cparams, uparams, options)

    def instanceedit(self, **instance_properties):
        u"""
        Usage::

            instanceedit [instance_properties...]

        Changes the server instance configuration using given properties.

        Example::

           instanceedit serverinstance_filetransfer_port=1337
           error id=0 msg=ok

        Example::

            >>> ts3cmd.instanceedit(serverinstance_filetransfer_port=1337)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams.update(instance_properties)
        return self._return_proxy(u"instanceedit", cparams, uparams, options)

    def instanceinfo(self):
        u"""
        Usage::

            instanceinfo

        Displays the server instance configuration including database revision number,
        the file transfer port, default group IDs, etc.

        Example::

           instanceinfo
           serverinstance_database_version=12 serverinstance_filetransfer_port=30033
           serverinstance_template_guest_serverquery_group=1...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.instanceinfo()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"instanceinfo", cparams, uparams, options)

    def logadd(self, **_3to2kwargs):
        logmsg = _3to2kwargs['logmsg']; del _3to2kwargs['logmsg']
        loglevel = _3to2kwargs['loglevel']; del _3to2kwargs['loglevel']
        u"""
        Usage::

            logadd loglevel={1-4} logmsg={text}

        Writes a custom entry into the servers log. Depending on your permissions,
        you'll be able to add entries into the server instance log and/or your virtual
        servers log. The loglevel parameter specifies the type of the entry.

        Example::

           logadd loglevel=4 logmsg=Informational\smessage!
           error id=0 msg=ok

        Example::

            >>> ts3cmd.logadd(loglevel=4, logmsg="Informational message!")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"loglevel"] = loglevel
        cparams[u"logmsg"] = logmsg
        return self._return_proxy(u"logadd", cparams, uparams, options)

    def login(self, **_3to2kwargs):
        client_login_password = _3to2kwargs['client_login_password']; del _3to2kwargs['client_login_password']
        client_login_name = _3to2kwargs['client_login_name']; del _3to2kwargs['client_login_name']
        u"""
        Usage:

            login client_login_name={username} client_login_password={password}
            login {username} {password}

        Authenticates with the TeamSpeak 3 Server instance using given ServerQuery
        login credentials.

        Example::
           login client_login_name=xyz client_login_password=xyz
           error id=0 msg=ok

           login xyz xyz
           error id=0 msg=ok

        Example::

            >>> ts3cmd.login(
            ...     client_login_name="xyz", client_login_password="xyz")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"client_login_name"] = client_login_name
        cparams[u"client_login_password"] = client_login_password
        return self._return_proxy(u"login", cparams, uparams, options)

    def logout(self):
        u"""
        Usage::

            logout

        Deselects the active virtual server and logs out from the server instance.

        Example::

           logout
           error id=0 msg=ok

        Example::

            >>> ts3cmd.logout()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"logout", cparams, uparams, options)

    def logview(self, **_3to2kwargs):
        if 'begin_pos' in _3to2kwargs: begin_pos = _3to2kwargs['begin_pos']; del _3to2kwargs['begin_pos']
        else: begin_pos = None
        if 'instance' in _3to2kwargs: instance = _3to2kwargs['instance']; del _3to2kwargs['instance']
        else: instance = None
        if 'reverse' in _3to2kwargs: reverse = _3to2kwargs['reverse']; del _3to2kwargs['reverse']
        else: reverse = None
        if 'lines' in _3to2kwargs: lines = _3to2kwargs['lines']; del _3to2kwargs['lines']
        else: lines = None
        u"""
        Usage::

            logview [lines={1-100}] [reverse={1|0}] [instance={1|0}] [begin_pos={n}]

        Displays a specified number of entries from the servers logfile. If instance
        is set to 1, the server will return lines from the master logfile (ts3server_0)
        instead of the selected virtual server logfile.

        Example::

           logview
           last_pos=403788 file_size=411980 l=\p\slistening\son\s0.0.0.0:9987 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.logview()
            ...
            >>> ts3cmd.logview(lines=100, begin_pos=10)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"lines"] = lines
        cparams[u"reverse"] = reverse
        cparams[u"instance"] = instance
        cparams[u"begin_pos"] = begin_pos
        return self._return_proxy(u"logview", cparams, uparams, options)

    def messageadd(self, **_3to2kwargs):
        message = _3to2kwargs['message']; del _3to2kwargs['message']
        subject = _3to2kwargs['subject']; del _3to2kwargs['subject']
        cluid = _3to2kwargs['cluid']; del _3to2kwargs['cluid']
        u"""
        Usage::

            messageadd cluid={clientUID} subject={subject} message={text}

        Sends an offline message to the client specified by cluid.

        Example::

           messageadd cluid=oHhi9WzXLNEFQOwAu4JYKGU+C+c= subject=Hi! message=Hello?!?
           error id=0 msg=ok

        Example::

            >>> ts3cmd.messageadd(
            ...     cluid="oHhi9WzXLNEFQOwAu4JYKGU+C+c=", subject="Hi!",
            ...     message="Hello?!?")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cluid"] = cluid
        cparams[u"subject"] = subject
        cparams[u"message"] = message
        return self._return_proxy(u"messageadd", cparams, uparams, options)

    def messagedel(self, **_3to2kwargs):
        msgid = _3to2kwargs['msgid']; del _3to2kwargs['msgid']
        u"""
        Usage::

            messagedel msgid={messageID}

        Deletes an existing offline message with ID msgid from your inbox.

        Example::

           messagedel msgid=4
           error id=0 msg=ok

        Example::

            >>> ts3cmd.messagedel(msgid=4)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"msgid"] = msgid
        return self._return_proxy(u"messagedel", cparams, uparams, options)

    def messageget(self, **_3to2kwargs):
        msgid = _3to2kwargs['msgid']; del _3to2kwargs['msgid']
        u"""
        Usage::

            messageget msgid={messageID}

        Displays an existing offline message with ID msgid from your inbox. Please note
        that this does not automatically set the flag_read property of the message.

        Example::

           messageget msgid=4
           msgid=4 cluid=xwEzb5ENOaglVHu9oelK++reUyE= subject=Hi! message=Hello?!?
           error id=0 msg=ok

        Example::

            >>> ts3cmd.messageget(msgid=4)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"msgid"] = msgid
        return self._return_proxy(u"messageget", cparams, uparams, options)

    def messagelist(self):
        u"""
        Usage::

            messagelist

        Displays a list of offline messages you've received. The output contains the
        senders unique identifier, the messages subject, etc.

        Example::

           messagelist
           msgid=4 cluid=xwEzb5ENOaglVHu9oelK++reUyE= subject=Test flag_read=0...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.messagelist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"messagelist", cparams, uparams, options)

    def messageupdateflag(self, **_3to2kwargs):
        flag = _3to2kwargs['flag']; del _3to2kwargs['flag']
        msgid = _3to2kwargs['msgid']; del _3to2kwargs['msgid']
        u"""
        Usage::

            messageupdateflag msgid={messageID} flag={1|0}

        Updates the flag_read property of the offline message specified with msgid. If
        flag is set to 1, the message will be marked as read.

        Example::

           messageupdateflag msgid=4 flag=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.messageupdateflag(msgid=4, flag=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"msgid"] = msgid
        cparams[u"flag"] = flag
        return self._return_proxy(u"messageupdateflag", cparams, uparams, options)

    def permfind(self, **_3to2kwargs):
        permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        u"""
        Usage::

            permfind permid={permID}

        Displays detailed information about all assignments of the permission specified
        with permid. The output is similar to permoverview which includes the type and
        the ID of  the client, channel or group associated with the permission.

        Example::

           permfind permid=4353
           t=0 id1=1 id2=0 p=4353|t=0 id1=2 id2=0 p=4353
           error id=0 msg=ok

        Example::

            >>> ts3cmd.permfind(permid=4353)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"permid"] = permid
        return self._return_proxy(u"permfind", cparams, uparams, options)

    def permget(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        u"""
        Usage::

            permget permid={permID}
            permget permsid={permName}

        Displays the current value of the permission specified with permid or permsid
        for your own connection. This can be useful when you need to check your own
        privileges.

        Example::

           permget permid=21174
           permsid=i_client_move_power permid=21174 permvalue=100
           error id=0 msg=ok

           permget permsid=i_client_move_power
           permsid=i_client_move_power permid=21174 permvalue=100
           error id=0 msg=ok

        Example::

            >>> ts3cmd.permget(permid=21174)
            ...
            >>> ts3cmd.permget(permsid="i_client_move_power")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"permid"] = permid
        cparams[u"permsid"] = permsid
        return self._return_proxy(u"permget", cparams, uparams, options)

    def permidgetbyname(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        u"""
        Usage::

            permidgetbyname permsid={permName}|permsid={permName}|...

        Displays the database ID of one or more permissions specified by permsid.

        Example::

           permidgetbyname permsid=b_serverinstance_help_view
           permsid=b_serverinstance_help_view permid=4353
           error id=0 msg=ok

        Example::

            >>> ts3cmd.permidgetbyname(permsid="b_serverinstance_help_view")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        uparams.append(OrderedDict())
        uparams[0][u"permsid"] = permsid
        return self._return_proxy(u"permidgetbyname", cparams, uparams, options)

    def permissionlist(self):
        u"""
        Usage::

            permissionlist

        Displays a list of permissions available on the server instance including ID,
        name and description.

        Example::

           permissionlist
           permid=21413 permname=b_client_channel_textmessage_send permdesc=Send\ste...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.permissionlist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"permissionlist", cparams, uparams, options)

    def permoverview(self, **_3to2kwargs):
        permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        u"""
        Usage::

            permoverview cid={channelID} cldbid={clientDBID} permid={permID}

        Displays all permissions assigned to a client for the channel specified with
        cid. If permid is set to 0, all permissions will be displayed. The output
        follows the following format:

         t={permType} id1={id1} id2={id2} p={permID} v={permValue} n={permNegated}
         s={permSkip}|t={permType} id1={id1} id2={id2} p={permID} v={permValue}
         n={permNegated} s={permSkip}|...

        The possible values for t, id1 and id2 are:

         0: Server Group;    => id1={serverGroupID}, id2=0
         1: Global Client;   => id1={clientDBID},    id2=0
         2: Channel;         => id1={channelID},     id2=0
         3: Channel Group;   => id1={channelID},     id2={channelGroupID}
         4: Channel Client;  => id1={channelID},     id2={clientDBID}

        Example::

           permoverview cldbid=57 cid=74 permid=0
           t=0 id1=5 id2=0 p=37 v=1 n=0 s=0|t=0 id1=5 id2=0 p=38 v=1 n=0 s=0|...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.permoverview(cldbid=57, cid=74, permid=0)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cid"] = cid
        cparams[u"cldbid"] = cldbid
        cparams[u"permid"] = permid
        return self._return_proxy(u"permoverview", cparams, uparams, options)

    def permreset(self):
        u"""
        Usage::

            permreset

        Restores the default permission settings on the selected virtual server and
        creates a new initial administrator token. Please note that in case of an
        error during the permreset call - e.g. when the database has been modified or
        corrupted - the virtual server will be deleted from the database.

        Example::

           permreset
           token=MqQbPLLm6jLC+x8j31jUL7GkME1UY0GaDYK+XG5e
           error id=0 msg=ok

        Example::

            >>> ts3cmd.permreset()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"permreset", cparams, uparams, options)

    def privilegekeyadd(self, **_3to2kwargs):
        if 'tokencustomset' in _3to2kwargs: tokencustomset = _3to2kwargs['tokencustomset']; del _3to2kwargs['tokencustomset']
        else: tokencustomset = None
        if 'tokendescription' in _3to2kwargs: tokendescription = _3to2kwargs['tokendescription']; del _3to2kwargs['tokendescription']
        else: tokendescription = None
        tokenid2 = _3to2kwargs['tokenid2']; del _3to2kwargs['tokenid2']
        tokenid1 = _3to2kwargs['tokenid1']; del _3to2kwargs['tokenid1']
        tokentype = _3to2kwargs['tokentype']; del _3to2kwargs['tokentype']
        u"""
        Usage::

            privilegekeyadd tokentype={1|0} tokenid1={groupID}
                            tokenid2={channelID} [tokendescription={description}]
                            [tokencustomset={customFieldSet}]

        Create a new token. If tokentype is set to 0, the ID specified with tokenid1
        will be a server group ID. Otherwise, tokenid1 is used as a channel group ID
        and you need to provide a valid channel ID using tokenid2.

        The tokencustomset parameter allows you to specify a set of custom client
        properties. This feature can be used when generating tokens to combine a
        website account database with a TeamSpeak user. The syntax of the value
        needs to be escaped using the ServerQuery escape patterns and has to follow
        the general syntax of:

        ident=ident1 value=value1|ident=ident2 value=value2|ident=ident3 value=value3

        Example::

           privilegekeyadd tokentype=0 tokenid1=6 tokenid2=0 tokendescription=Test
            tokencustomset=ident=forum_user\svalue=dante\pident=forum_id\svalue=123
           token=1ayoQOxG8r5Re78zgChvLYBWWaFWCoty0Uh+pUFk
           error id=0 msg=ok

        Example::

            >>> ts3cmd.privilegekeyadd(
            ...     tokentype=0, tokenid1=6, tokenid2=0,
            ...     tokendescription="Test",
            ...     tokencustomset="ident=forum_user\svalue=dante\pident=forum_id\svalue=123"
            ...     )
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"tokentype"] = tokentype
        cparams[u"tokenid1"] = tokenid1
        cparams[u"tokenid2"] = tokenid2
        cparams[u"tokendescription"] = tokendescription
        cparams[u"tokencustomset"] = tokencustomset
        return self._return_proxy(u"privilegekeyadd", cparams, uparams, options)

    def privilegekeydelete(self, **_3to2kwargs):
        token = _3to2kwargs['token']; del _3to2kwargs['token']
        u"""
        Usage::

            privilegekeydelete token={tokenKey}

        Deletes an existing token matching the token key specified with token.

        Example::

           privilegekeydelete token=eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW
           error id=0 msg=ok

        Example::

            >>> ts3cmd.privilegekeydelete(
            ...     token="eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"token"] = token
        return self._return_proxy(u"privilegekeydelete", cparams, uparams, options)

    def privilegekeylist(self):
        u"""
        Usage::

            privilegekeylist

        Displays a list of tokens available including their type and group IDs. Tokens
        can be used to gain access to specified server or channel groups.

        A token is similar to a client with administrator privileges that adds you to
        a certain permission group, but without the necessity of a such a client with
        administrator privileges to actually exist. It is a long (random looking)
        string that can be used as a ticket into a specific server group.

        Example::

           privilegekeylist
           token=88CVUg\/zkujt+y+WfHdko79UcM4R6uyCL6nEfy3B token_type=0 token_id1=9...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.privilegekeylist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"privilegekeylist", cparams, uparams, options)

    def privilegekeyuse(self, **_3to2kwargs):
        token = _3to2kwargs['token']; del _3to2kwargs['token']
        u"""
        Usage::

            privilegekeyuse token={tokenKey}

        Use a token key gain access to a server or channel group. Please note that the
        server will automatically delete the token after it has
        been used.

        Example::

           privilegekeyuse token=eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW
           error id=0 msg=ok

        Example::

            >>> ts3cmd.privilegekeyuse(
            ...     token="eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"token"] = token
        return self._return_proxy(u"privilegekeyuse", cparams, uparams, options)

    def quit(self):
        u"""
        Usage::

            quit

        Closes the ServerQuery connection to the TeamSpeak 3 Server instance.

        Example::

           quit
           error id=0 msg=ok

        Example::

            >>> ts3cmd.quit()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"quit", cparams, uparams, options)

    def sendtextmessage(self, **_3to2kwargs):
        msg = _3to2kwargs['msg']; del _3to2kwargs['msg']
        target = _3to2kwargs['target']; del _3to2kwargs['target']
        targetmode = _3to2kwargs['targetmode']; del _3to2kwargs['targetmode']
        u"""
        Usage::

            sendtextmessage targetmode={1-3}
                            target={serverID|channelID|clientID} msg={text}

        Sends a text message a specified target. The type of the target is determined
        by targetmode while target specifies the ID of the recipient, whether it be a
        virtual server, a channel or a client.

        Example::

           sendtextmessage targetmode=2 target=1 msg=Hello\sWorld!
           error id=0 msg=ok

        Example::

            >>> ts3cmd.sendtextmessage(
            ...     targetmode=2, target=1, msg="Hello World!")
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"targetmode"] = targetmode
        cparams[u"target"] = target
        cparams[u"msg"] = msg
        return self._return_proxy(u"sendtextmessage", cparams, uparams, options)

    def servercreate(self, **virtualserver_properties):
        u"""
        Usage::

            servercreate [virtualserver_properties...]

        Creates a new virtual server using the given properties and displays its ID and
        initial administrator token. If virtualserver_port is not specified, the server
        will test for the first unused UDP port.

        Example::

           servercreate virtualserver_name=TeamSpeak\s]\p[\sServer
            virtualserver_port=9988 virtualserver_maxclients=32
           sid=7 token=HhPbcMAMdAHGUip1yOma2Tl3sN0DN7B3Y0JVzYv6 virtualserver_port=9988
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servercreate(
            ...     virtualserver_name="TeamSpeak ]|[ Server",
            ...     virtualserver_port=9988, virtualserver_maxclients=32)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams.update(virtualserver_properties)
        return self._return_proxy(u"servercreate", cparams, uparams, options)

    def serverdelete(self, **_3to2kwargs):
        sid = _3to2kwargs['sid']; del _3to2kwargs['sid']
        u"""
        Usage::

            serverdelete sid={serverID}

        Deletes the virtual server specified with sid. Please note that only virtual
        servers in stopped state can be deleted.

        Example::

           serverdelete sid=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serverdelete(sid=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sid"] = sid
        return self._return_proxy(u"serverdelete", cparams, uparams, options)

    def serveredit(self, **virtualserver_properties):
        u"""
        Usage::

            serveredit [virtualserver_properties...]

        Changes the selected virtual servers configuration using given properties.

        Example::

           serveredit virtualserver_name=TeamSpeak\sServer virtualserver_maxclients=32
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serveredit(
            ...     virtualserver_name="TeamSpeak Server",
            ...     virtualserver_maxclients=32)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams.update(virtualserver_properties)
        return self._return_proxy(u"serveredit", cparams, uparams, options)

    def servergroupadd(self, **_3to2kwargs):
        if 'type_' in _3to2kwargs: type_ = _3to2kwargs['type_']; del _3to2kwargs['type_']
        else: type_ = None
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        u"""
        Usage::

            servergroupadd name={groupName} [type={groupDbType}]

        Creates a new server group using the name specified with name and displays
        its ID. The optional type parameter can be used to create ServerQuery groups
        and template groups.

        Example::

           servergroupadd name=Server\sAdmin
           sgid=13
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupadd(name="Server Admin")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"name"] = name
        cparams[u"type"] = type_
        return self._return_proxy(u"servergroupadd", cparams, uparams, options)

    def servergroupaddclient(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergroupaddclient sgid={groupID} cldbid={clientDBID}

        Adds a client to the server group specified with sgid. Please note that a
        client cannot be added to default groups or template groups.

        Example::

           servergroupaddclient sgid=16 cldbid=3
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupaddclient(sgid=16, cldbid=3)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgid"] = sgid
        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"servergroupaddclient", cparams, uparams, options)

    def servergroupaddperm(self, **_3to2kwargs):
        if 'permvalue' in _3to2kwargs: permvalue = _3to2kwargs['permvalue']; del _3to2kwargs['permvalue']
        else: permvalue = None
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        permskip = _3to2kwargs['permskip']; del _3to2kwargs['permskip']
        permnegated = _3to2kwargs['permnegated']; del _3to2kwargs['permnegated']
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergroupaddperm sgid={groupID} permid={permID}
                               permvalue={permValue} permnegated={1|0}
                               permskip={1|0}|...
            servergroupaddperm sgid={groupID} permsid={permName}
                               permvalue={permValue} permnegated={1|0}
                               permskip={1|0}|...

        Adds a set of specified permissions to the server group specified with sgid.
        Multiple permissions can be added by providing the four parameters of each
        permission. A permission can be specified by permid or permsid.

        Example::

           servergroupaddperm sgid=13 permid=8470 permvalue=1 permnegated=0
            permskip=0|permid=8475 permvalue=0 permnegated=1 permskip=0
           error id=0 msg=ok

           servergroupaddperm sgid=13 permsid=i_icon_id permvalue=123
            permnegated=0 permskip=0|permsid=b_virtualserver_stop permvalue=0
            permnegated=1 permskip=0
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupaddperm(
            ...     sgid=13, permid=8470, permvalue=1, permnegated=0,
            ...     permskip=0)
            ...
            >>> ts3cmd.servergroupaddperm(
            ...     sgid=13, permsid="i_icon_id", permvalue=123, permnegated=0,
            ...     permskip=0)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        uparams.append(OrderedDict())
        uparams[0][u"sgid"] = sgid
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        uparams[0][u"permvalue"] = permvalue
        uparams[0][u"permnegated"] = permnegated
        uparams[0][u"permskip"] = permskip
        return self._return_proxy(u"servergroupaddperm", cparams, uparams, options)

    def servergroupautoaddperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        permskip = _3to2kwargs['permskip']; del _3to2kwargs['permskip']
        permnegated = _3to2kwargs['permnegated']; del _3to2kwargs['permnegated']
        permvalue = _3to2kwargs['permvalue']; del _3to2kwargs['permvalue']
        sgtype = _3to2kwargs['sgtype']; del _3to2kwargs['sgtype']
        u"""
        Usage::

            servergroupautoaddperm sgtype={type} permid={permID}
                                   permvalue={permValue} permnegated={1|0}
                                   permskip={1|0}|...
            servergroupautoaddperm sgtype={type} permsid={permName}
                                   permvalue={permValue} permnegated={1|0}
                                   permskip={1|0}|...

        Adds a set of specified permissions to ALL regular server groups on all
        virtual servers. The target groups will be identified by the value of their
        i_group_auto_update_type permission specified with sgtype. Multiple permissions
        can be added at once. A permission can be specified by permid or permsid.

        The known values for sgtype are:

         10: Channel Guest
         15: Server Guest
         20: Query Guest
         25: Channel Voice
         30: Server Normal
         35: Channel Operator
         40: Channel Admin
         45: Server Admin
         50: Query Admin

        Example::

           servergroupautoaddperm sgtype=45 permid=8470 permvalue=1 permnegated=0
            permskip=0|permid=8475 permvalue=0 permnegated=1 permskip=0
           error id=0 msg=ok

           servergroupautoaddperm sgtype=45 permsid=i_icon_id permvalue=123
            permnegated=0 permskip=0|permsid=b_virtualserver_stop permvalue=0
            permnegated=1 permskip=0
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupautoaddperm(
            ...     sgtype=45, permid=8470, permvalue=1, permnegated=0,
            ...     permskip=0)
            ...
            >>> ts3cmd.servergroupautoaddperm(
            ...     sgtype=45, permsid="i_icon_id", permvalue=123,
            ...     permnegated=0, permskip=0)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        uparams.append(OrderedDict())
        uparams[0][u"sgtype"] = sgtype
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        uparams[0][u"permvalue"] = permvalue
        uparams[0][u"permnegated"] = permnegated
        uparams[0][u"permskip"] = permskip
        return self._return_proxy(u"servergroupautoaddperm", cparams, uparams, options)

    def servergroupautodelperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        sgtype = _3to2kwargs['sgtype']; del _3to2kwargs['sgtype']
        u"""
        Usage::

            servergroupautodelperm sgtype={type} permid={permID}|permid={permID}|...
            servergroupautodelperm sgtype={type} permsid={permName}|...

        Removes a set of specified permissions from ALL regular server groups on all
        virtual servers. The target groups will be identified by the value of their
        i_group_auto_update_type permission specified with sgtype. Multiple permissions
        can be removed at once. A permission can be specified by permid or permsid.

        The known values for sgtype are:

         10: Channel Guest
         15: Server Guest
         20: Query Guest
         25: Channel Voice
         30: Server Normal
         35: Channel Operator
         40: Channel Admin
         45: Server Admin
         50: Query Admin

        Examples::

           servergroupautodelperm sgtype=45 permid=8470|permid=8475
           error id=0 msg=ok

           servergroupautodelperm sgtype=45 permsid=b_virtualserver_modify_maxclients
           error id=0 msg=ok

        Examples::

            >>> ts3cmd.servergroupautodelperm(sgtype=45, permid=8470)
            ...
            >>> ts3cmd.servergroupautodelperm(
            ...     sgtype=45, permsid="b_virtualserver_modify_maxclients")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgtype"] = sgtype

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        return self._return_proxy(u"servergroupautodelperm", cparams, uparams, options)

    def servergroupbyclientid(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            servergroupsbyclientid cldbid={clientDBID}

        Displays all server groups the client specified with cldbid is currently
        residing in.

        Example::

           servergroupsbyclientid cldbid=18
           name=Server\sAdmin sgid=6 cldbid=18
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupbyclientid(cldbid=18)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"servergroupbyclientid", cparams, uparams, options)

    def servergroupclientlist(self, **_3to2kwargs):
        if 'names' in _3to2kwargs: names = _3to2kwargs['names']; del _3to2kwargs['names']
        else: names = False
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergroupclientlist sgid={groupID} [-names]

        Displays the IDs of all clients currently residing in the server group
        specified with sgid. If you're using the -names option, the output will
        also contain the last known nickname and the unique identifier of the
        clients.

        Example::

           servergroupclientlist sgid=16
           cldbid=7|cldbid=8|cldbid=9|cldbid=11|cldbid=13|cldbid=16|cldbid=18|...
           error id=0 msg=ok

           servergroupclientlist sgid=8 -names
           cldbid=4 client_nickname=ScP client_unique_identifier=FPMPSC6MXqXq7...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupclientlist(sgid=16)
            ...
            >>> ts3cmd.servergroupclientlist(sgid=8, names=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgid"] = sgid

        if names:
            options.append(u"names")
        return self._return_proxy(u"servergroupclientlist", cparams, uparams, options)

    def servergroupcopy(self, **_3to2kwargs):
        type_ = _3to2kwargs['type_']; del _3to2kwargs['type_']
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        tsgid = _3to2kwargs['tsgid']; del _3to2kwargs['tsgid']
        ssgid = _3to2kwargs['ssgid']; del _3to2kwargs['ssgid']
        u"""
        Usage::

            servergroupcopy ssgid={sourceGroupID} tsgid={targetGroupID}
                            name={groupName} type={groupDbType}

        Creates a copy of the server group specified with ssgid. If tsgid is set to 0,
        the server will create a new group. To overwrite an existing group, simply set
        tsgid to the ID of a designated target group. If a target group is set, the
        name parameter will be ignored.

        The type parameter can be used to create ServerQuery and template groups.

        Example::

           servergroupcopy ssgid=6 tsgid=0 name=My\sGroup\s(Copy) type=1
           sgid=21
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupcopy(
            ...     ssgid=6, tsgid=0, name="My Group (Copy)", type_=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"ssgid"] = ssgid
        cparams[u"tsgid"] = tsgid
        cparams[u"name"] = name
        cparams[u"type"] = type_
        return self._return_proxy(u"servergroupcopy", cparams, uparams, options)

    def servergroupdel(self, **_3to2kwargs):
        if 'force' in _3to2kwargs: force = _3to2kwargs['force']; del _3to2kwargs['force']
        else: force = False
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergroupdel sgid={groupID} force={1|0}

        Deletes the server group specified with sgid. If force is set to 1, the server
        group will be deleted even if there are clients within.

        Example::

           servergroupdel sgid=13
           error id=0 msg=ok

           servergroupdel sgid=14 force=1
           error id=0 msg=ok

        Examples::

            >>> ts3cmd.servergroupdel(sgid=13)
            ...
            >>> ts3cmd.servergroupdel(sgid=14, force=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgid"] = sgid
        cparams[u"force"] = force
        return self._return_proxy(u"servergroupdel", cparams, uparams, options)

    def servergroupdelclient(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergroupdelclient sgid={groupID} cldbid={clientDBID}

        Removes a client from the server group specified with sgid.

        Example::

           servergroupdelclient sgid=16 cldbid=3
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupdelclient(sgid=16, cldbid=3)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgid"] = sgid
        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"servergroupdelclient", cparams, uparams, options)

    def servergroupdelperm(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = None
        if 'permid' in _3to2kwargs: permid = _3to2kwargs['permid']; del _3to2kwargs['permid']
        else: permid = None
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergroupdelperm sgid={groupID} permid={permID}|permid={permID}
            servergroupdelperm sgid={groupID} permsid={permName}

        Removes a set of specified permissions from the server group specified with
        sgid. Multiple permissions can be removed at once. A permission can be
        specified by permid or permsid.

        Examples::

           servergroupdelperm sgid=16 permid=8470|permid=8475
           error id=0 msg=ok

           servergroupdelperm sgid=16 permsid=i_channel_join_power
           error id=0 msg=ok

        Examples::

            >>> ts3cmd.servergroupdelperm(sgid=16, permid=8470)
            ...
            >>> ts3cmd.servergroupdelperm(sgid=16, permid=8475)
            ...
            >>> ts3cmd.servergroupdelperm(
            ...     sgid=16, permsid="i_channel_join_power")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgid"] = sgid

        uparams.append(OrderedDict())
        uparams[0][u"permid"] = permid
        uparams[0][u"permsid"] = permsid
        return self._return_proxy(u"servergroupdelperm", cparams, uparams, options)

    def servergrouplist(self):
        u"""
        Usage::

            servergrouplist

        Displays a list of server groups available. Depending on your permissions, the
        output may also contain global ServerQuery groups and template groups.

        Example::

           servergrouplist
           sgid=9 name=Server\sAdmin type=1 iconid=300 savedb=1|sgid=10 name=Normal t...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergrouplist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"servergrouplist", cparams, uparams, options)

    def servergrouppermlist(self, **_3to2kwargs):
        if 'permsid' in _3to2kwargs: permsid = _3to2kwargs['permsid']; del _3to2kwargs['permsid']
        else: permsid = False
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergrouppermlist sgid={groupID} [-permsid]

        Displays a list of permissions assigned to the server group specified with sgid.
        The optional -permsid parameter can be used to get the permission names instead
        of their internal ID.

        Example:
           servergrouppermlist sgid=13
           permid=8470 permvalue=1 permnegated=0 permskip=0|permid=8475 permvalue=1|...
           error id=0 msg=ok

           servergrouppermlist sgid=14 -permsid
           permsid=b_virtualserver_info_view permvalue=1 permnegated=0 permskip=0|...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergrouppermlist(sgid=13)
            ...
            >>> ts3cmd.servergrouppermlist(sgid=14, permsid=True)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgid"] = sgid

        if permsid:
            options.append(u"permsid")
        return self._return_proxy(u"servergrouppermlist", cparams, uparams, options)

    def servergrouprename(self, **_3to2kwargs):
        name = _3to2kwargs['name']; del _3to2kwargs['name']
        sgid = _3to2kwargs['sgid']; del _3to2kwargs['sgid']
        u"""
        Usage::

            servergrouprename sgid={groupID} name={groupName}

        Changes the name of the server group specified with sgid.

        Example::

           servergrouprename sgid=13 name=New\sName
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergrouprename(sgid=13, name="New Name")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sgid"] = sgid
        cparams[u"name"] = name
        return self._return_proxy(u"servergrouprename", cparams, uparams, options)

    def servergroupsbyclientid(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        u"""
        Usage::

            servergroupsbyclientid cldbid={clientDBID}

        Displays all server groups the client specified with cldbid is currently
        residing in.

        Example::

           servergroupsbyclientid cldbid=18
           name=Server\sAdmin sgid=6 cldbid=18
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servergroupsbyclientid(cldbid=18)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"servergroupsbyclientid", cparams, uparams, options)

    def serveridgetbyport(self, **_3to2kwargs):
        virtualserver_port = _3to2kwargs['virtualserver_port']; del _3to2kwargs['virtualserver_port']
        u"""
        Usage::

            serveridgetbyport virtualserver_port={serverPort}

        Displays the database ID of the virtual server running on the UDP port
        specified by virtualserver_port.

        Example::

           serveridgetbyport virtualserver_port=9987
           server_id=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serveridgetbyport(virtualserver_port=9987)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"virtualserver_port"] = virtualserver_port
        return self._return_proxy(u"serveridgetbyport", cparams, uparams, options)

    def serverinfo(self):
        u"""
        Usage::

            serverinfo

        Displays detailed configuration information about the selected virtual server
        including unique ID, number of clients online, configuration, etc.

        Example::

           serverinfo
           virtualserver_port=9987 virtualserver_name=TeamSpeak\s]I[\sServer virtua...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serverinfo()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"serverinfo", cparams, uparams, options)

    def serverlist(self, **_3to2kwargs):
        if 'onlyoffline' in _3to2kwargs: onlyoffline = _3to2kwargs['onlyoffline']; del _3to2kwargs['onlyoffline']
        else: onlyoffline = False
        if 'short' in _3to2kwargs: short = _3to2kwargs['short']; del _3to2kwargs['short']
        else: short = False
        if 'all_' in _3to2kwargs: all_ = _3to2kwargs['all_']; del _3to2kwargs['all_']
        else: all_ = False
        if 'uid' in _3to2kwargs: uid = _3to2kwargs['uid']; del _3to2kwargs['uid']
        else: uid = False
        u"""
        Usage::

            serverlist [-uid] [-all] [-short] [-onlyoffline]

        Displays a list of virtual servers including their ID, status, number of
        clients online, etc. If you're using the -all option, the server will list all
        virtual servers stored in the database. This can be useful when multiple server
        instances with different machine IDs are using the same database. The machine
        ID is used to identify the server instance a virtual server is associated with.

        The status of a virtual server can be either online, offline, booting up,
        shutting down and virtual online. While most of them are self-explanatory,
        virtual online is a bit more complicated. Whenever you select a virtual server
        which is currently stopped, it will be started in virtual mode which means you
        are able to change its configuration, create channels or change permissions,
        but no regular TeamSpeak 3 Client can connect. As soon as the last ServerQuery
        client deselects the virtual server, its status will be changed back to
        offline.

        Example::

           serverlist
           virtualserver_id=1 virtualserver_port=9987 virtualserver_status=online
           virtualserver_clientsonline=6...
           error id=0 msg=ok

        Examples::

            >>> ts3cmd.serverlist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        if uid:
            options.append(u"uid")
        if all_:
            options.append(u"all")
        if short:
            options.append(u"short")
        if onlyoffline:
            options.append(u"onlyoffline")
        return self._return_proxy(u"serverlist", cparams, uparams, options)

    def servernotifyregister(self, **_3to2kwargs):
        if 'id_' in _3to2kwargs: id_ = _3to2kwargs['id_']; del _3to2kwargs['id_']
        else: id_ = None
        event = _3to2kwargs['event']; del _3to2kwargs['event']
        u"""
        Usage::

            servernotifyregister [id={channelID}]
                                 event={server|channel|textserver|textchannel|textprivate}

        Registers for a specified category of events on a virtual server to receive
        notification messages. Depending on the notifications you've registered for,
        the server will send you a message on every event in the view of your
        ServerQuery client (e.g. clients joining your channel, incoming text messages,
        server configuration changes, etc). The event source is declared by the event
        parameter while id can be used to limit the notifications to a specific channel.

        Example::

           servernotifyregister event=server
           error id=0 msg=ok

           servernotifyregister event=channel id=123
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servernotifyregister(event="server")
            ...
            >>> ts3cmd.servernotifyregister(event="channel", id_=123)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"id"] = id_
        cparams[u"event"] = event
        return self._return_proxy(u"servernotifyregister", cparams, uparams, options)

    def servernotifyunregister(self):
        u"""
        Usage::

            servernotifyunregister

        Unregisters all events previously registered with servernotifyregister so you
        will no longer receive notification messages.

        Example::

           servernotifyunregister
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servernotifyunregister()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"servernotifyunregister", cparams, uparams, options)

    def serverprocessstop(self):
        u"""
        Usage::

            serverprocessstop

        Stops the entire TeamSpeak 3 Server instance by shutting down the process.

        Example::

           serverprocessstop
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serverprocessstop()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"serverprocessstop", cparams, uparams, options)

    def serverrequestconnectioninfo(self):
        u"""
        Usage::

            serverrequestconnectioninfo

        Displays detailed connection information about the selected virtual server
        including uptime, traffic information, etc.

        Example::

           serverrequestconnectioninfo
           connection_filetransfer_bandwidth_sent=0 connection_packets_sent_total=0...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serverrequestconnectioninfo()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"serverrequestconnectioninfo", cparams, uparams, options)

    def serversnapshotcreate(self):
        u"""
        Usage::

            serversnapshotcreate

        Displays a snapshot of the selected virtual server containing all settings,
        groups and known client identities. The data from a server snapshot can be
        used to restore a virtual servers configuration.

        Example::

           serversnapshotcreate
           hash=bnTd2E1kNITHjJYRCFjgbKKO5P8=|virtualserver_name=TeamSpeak\sServer...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serversnapshotcreate()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"serversnapshotcreate", cparams, uparams, options)

    def serversnapshotdeploy(self, **_3to2kwargs):
        virtualserver_snapshot = _3to2kwargs['virtualserver_snapshot']; del _3to2kwargs['virtualserver_snapshot']
        u"""
        Usage::

            serversnapshotdeploy {virtualserver_snapshot}

        Restores the selected virtual servers configuration using the data from a
        previously created server snapshot. Please note that the TeamSpeak 3 Server
        does NOT check for necessary permissions while deploying a snapshot so the
        command could be abused to gain additional privileges.

        Example::

           serversnapshotdeploy hash=bnTd2E1kNITHjJYRCFjgbKKO5P8=|virtualserver_...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serversnapshotdeploy(
            ...     "hash=bnTd2E1kNITHjJYRCFjgbKKO5P8=|virtualserver_...")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u""] = virtualserver_snapshot
        return self._return_proxy(u"serversnapshotdeploy", cparams, uparams, options)

    def serverstart(self, **_3to2kwargs):
        sid = _3to2kwargs['sid']; del _3to2kwargs['sid']
        u"""
        Usage::

            serverstart sid={serverID}

        Starts the virtual server specified with sid. Depending on your permissions,
        you're able to start either your own virtual server only or any virtual server
        in the server instance.

        Example::

           serverstart sid=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serverstart(sid=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sid"] = sid
        return self._return_proxy(u"serverstart", cparams, uparams, options)

    def serverstop(self, **_3to2kwargs):
        sid = _3to2kwargs['sid']; del _3to2kwargs['sid']
        u"""
        Usage::

            serverstop sid={serverID}

        Stops the virtual server specified with sid. Depending on your permissions,
        you're able to stop either your own virtual server only or all virtual servers
        in the server instance.

        Example::

           serverstop sid=1
           error id=0 msg=ok

        Example::

            >>> ts3cmd.serverstop(sid=1)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sid"] = sid
        return self._return_proxy(u"serverstop", cparams, uparams, options)

    def servertemppasswordadd(self, **_3to2kwargs):
        tcpw = _3to2kwargs['tcpw']; del _3to2kwargs['tcpw']
        tcid = _3to2kwargs['tcid']; del _3to2kwargs['tcid']
        duration = _3to2kwargs['duration']; del _3to2kwargs['duration']
        desc = _3to2kwargs['desc']; del _3to2kwargs['desc']
        pw = _3to2kwargs['pw']; del _3to2kwargs['pw']
        u"""
        Usage::

            servertemppasswordadd pw={password} desc={description}
                                  duration={seconds} tcid={channelID}
                                  tcpw={channelPW}

        Sets a new temporary server password specified with pw. The temporary password
        will be valid for the number of seconds specified with duration. The client
        connecting with this password will automatically join the channel specified
        with tcid. If tcid is set to 0, the client will join the default channel.

        Example::

           servertemppasswordadd pw=secret desc=none duration=3600 tcid=117535 tcpw=123
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servertemppasswordadd(
            ...     pw="secret", desc="none", duration=3600, tcid=117535,
            ...     tcpw="123")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"pw"] = pw
        cparams[u"desc"] = desc
        cparams[u"duration"] = duration
        cparams[u"tcid"] = tcid
        cparams[u"tcpw"] = tcpw
        return self._return_proxy(u"servertemppasswordadd", cparams, uparams, options)

    def servertemppassworddel(self, **_3to2kwargs):
        pw = _3to2kwargs['pw']; del _3to2kwargs['pw']
        u"""
        Usage::

            servertemppassworddel pw={password}

        Deletes the temporary server password specified with pw.

        Example::

           servertemppassworddel pw=secret
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servertemppassworddel(pw="secret")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"pw"] = pw
        return self._return_proxy(u"servertemppassworddel", cparams, uparams, options)

    def servertemppasswordlist(self):
        u"""
        Usage::

            servertemppasswordlist

        Returns a list of active temporary server passwords. The output contains the
        clear-text password, the nickname and unique identifier of the creating client.

        Example::

           servertemppasswordlist
           nickname=serveradmin uid=serveradmin desc=none pw_clear=secret
           start=1331496494 end=1331500094 tcid=117535|nickname=serveradmin...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.servertemppasswordlist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"servertemppasswordlist", cparams, uparams, options)

    def setclientchannelgroup(self, **_3to2kwargs):
        cldbid = _3to2kwargs['cldbid']; del _3to2kwargs['cldbid']
        cid = _3to2kwargs['cid']; del _3to2kwargs['cid']
        cgid = _3to2kwargs['cgid']; del _3to2kwargs['cgid']
        u"""
        Usage::

            setclientchannelgroup cgid={groupID} cid={channelID}
                                  cldbid={clientDBID}

        Sets the channel group of a client to the ID specified with cgid.

        Example::

           setclientchannelgroup cgid=13 cid=15 cldbid=20
           error id=0 msg=ok

        Example::

            >>> ts3cmd.setclientchannelgroup(cgid=13, cid=15, cldbid=20)
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"cgid"] = cgid
        cparams[u"cid"] = cid
        cparams[u"cldbid"] = cldbid
        return self._return_proxy(u"setclientchannelgroup", cparams, uparams, options)

    def tokenadd(self, **_3to2kwargs):
        if 'tokencustomset' in _3to2kwargs: tokencustomset = _3to2kwargs['tokencustomset']; del _3to2kwargs['tokencustomset']
        else: tokencustomset = None
        if 'tokendescription' in _3to2kwargs: tokendescription = _3to2kwargs['tokendescription']; del _3to2kwargs['tokendescription']
        else: tokendescription = None
        tokenid2 = _3to2kwargs['tokenid2']; del _3to2kwargs['tokenid2']
        tokenid1 = _3to2kwargs['tokenid1']; del _3to2kwargs['tokenid1']
        tokentype = _3to2kwargs['tokentype']; del _3to2kwargs['tokentype']
        u"""
        Usage::

            tokenadd tokentype={1|0} tokenid1={groupID} tokenid2={channelID}
                     [tokendescription={description}]
                     [tokencustomset={customFieldSet}]

        Create a new token. If tokentype is set to 0, the ID specified with tokenid1
        will be a server group ID. Otherwise, tokenid1 is used as a channel group ID
        and you need to provide a valid channel ID using tokenid2.

        The tokencustomset parameter allows you to specify a set of custom client
        properties. This feature can be used when generating tokens to combine a
        website account database with a TeamSpeak user. The syntax of the value
        needs to be escaped using the ServerQuery escape patterns and has to follow
        the general syntax of:

        ident=ident1 value=value1|ident=ident2 value=value2|ident=ident3 value=value3

        Example::

           tokenadd tokentype=0 tokenid1=6 tokenid2=0 tokendescription=Test
            tokencustomset=ident=forum_user\svalue=ScP\pident=forum_id\svalue=123
           token=eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW
           error id=0 msg=ok

        Example::

            >>> ts3cmd.tokenadd(
            ...     tokentype=0, tokenid1=6, tokenid2=0,
            ...     tokendescription="Test",
            ...     tokencustomset="ident=forum_user\svalue=ScP\pident=forum_id\svalue=123"
            ...     )
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"tokentype"] = tokentype
        cparams[u"tokenid1"] = tokenid1
        cparams[u"tokenid2"] = tokenid2
        cparams[u"tokendescription"] = tokendescription
        cparams[u"tokencustomset"] = tokencustomset
        return self._return_proxy(u"tokenadd", cparams, uparams, options)

    def tokendelete(self, **_3to2kwargs):
        token = _3to2kwargs['token']; del _3to2kwargs['token']
        u"""
        Usage::

            tokendelete token={tokenKey}

        Deletes an existing token matching the token key specified with token.

        Example::

           tokendelete token=eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW
           error id=0 msg=ok

        Example::

            >>> ts3cmd.tokendelete(
            ...     token="eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"token"] = token
        return self._return_proxy(u"tokendelete", cparams, uparams, options)

    def tokenlist(self):
        u"""
        Usage::

            tokenlist

        Displays a list of tokens available including their type and group IDs. Tokens
        can be used to gain access to specified server or channel groups.

        A token is similar to a client with administrator privileges that adds you to
        a certain permission group, but without the necessity of a such a client with
        administrator privileges to actually exist. It is a long (random looking)
        string that can be used as a ticket into a specific server group.

        Example::

           tokenlist
           token=88CVUg\/zkujt+y+WfHdko79UcM4R6uyCL6nEfy3B token_type=0 token_id1=9...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.tokenlist()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"tokenlist", cparams, uparams, options)

    def tokenuse(self, **_3to2kwargs):
        token = _3to2kwargs['token']; del _3to2kwargs['token']
        u"""
        Usage::

            tokenuse token={tokenKey}

        Use a token key gain access to a server or channel group. Please note that the
        server will automatically delete the token after it has
        been used.

        Example::

           tokenuse token=eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW
           error id=0 msg=ok

        Example::

            >>> ts3cmd.tokenuse(
            ...     token="eKnFZQ9EK7G7MhtuQB6+N2B1PNZZ6OZL3ycDp2OW")
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"token"] = token
        return self._return_proxy(u"tokenuse", cparams, uparams, options)

    def use(self, **_3to2kwargs):
        if 'virtual' in _3to2kwargs: virtual = _3to2kwargs['virtual']; del _3to2kwargs['virtual']
        else: virtual = False
        if 'port' in _3to2kwargs: port = _3to2kwargs['port']; del _3to2kwargs['port']
        else: port = None
        if 'sid' in _3to2kwargs: sid = _3to2kwargs['sid']; del _3to2kwargs['sid']
        else: sid = None
        u"""
        Usage::

            use [sid={serverID}] [port={serverPort}] [-virtual]
            use {serverID}

        Selects the virtual server specified with sid or port to allow further
        interaction. The ServerQuery client will appear on the virtual server
        and acts like a real TeamSpeak 3 Client, except it's unable to send or
        receive voice data.

        If your database contains multiple virtual servers using the same UDP port,
        use will select a random virtual server using the specified port.

        Examples::

           use sid=1
           error id=0 msg=ok

           use port=9987
           error id=0 msg=ok

           use 1
           error id=0 msg=ok
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()

        cparams[u"sid"] = sid
        cparams[u"port"] = port

        if virtual:
            options.append(u"virtual")
        return self._return_proxy(u"use", cparams, uparams, options)

    def version(self):
        u"""
        Usage::

            version

        Displays the servers version information including platform and build number.

        Example::

           version
           version=3.0.0-beta16 build=9929 platform=Linux
           error id=0 msg=ok

        Example::

            >>> ts3cmd.version()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"version", cparams, uparams, options)

    def whoami(self):
        u"""
        Usage::

            whoami

        Displays information about your current ServerQuery connection including the ID
        of the selected virtual server, your loginname, etc.

        Example::

           whoami
           virtualserver_status=online virtualserver_id=1 client_channel_id=2 ...
           error id=0 msg=ok

        Example::

            >>> ts3cmd.whoami()
            ...
        """
        cparams = OrderedDict()
        uparams = list()
        options = list()
        return self._return_proxy(u"whoami", cparams, uparams, options)
