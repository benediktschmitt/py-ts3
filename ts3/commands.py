#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2013-2018 <see AUTHORS.txt>
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
from collections import OrderedDict
from .escape import RawParameter


# Data
# ------------------------------------------------
__all__ = ["TS3Commands"]


# Classes
# ------------------------------------------------
class TS3Commands(object):
    """
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
        """
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

    def banadd(self, *, ip=None, name=None, uid=None, time=None, banreason=None):
        """
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

        cparams["ip"] = ip
        cparams["name"] = name
        cparams["uid"] = uid
        cparams["time"] = time
        cparams["banreason"] = banreason
        return self._return_proxy("banadd", cparams, uparams, options)

    def banclient(self, *, clid, time=None, banreason=None):
        """
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

        cparams["clid"] = clid
        cparams["time"] = time
        cparams["banreason"] = banreason
        return self._return_proxy("banclient", cparams, uparams, options)

    def bandel(self, *, banid):
        """
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

        cparams["banid"] = banid
        return self._return_proxy("bandel", cparams, uparams, options)

    def bandelall(self):
        """
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
        return self._return_proxy("bandelall", cparams, uparams, options)

    def banlist(self):
        """
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
        return self._return_proxy("banlist", cparams, uparams, options)

    def bindinglist(self):
        """
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
        return self._return_proxy("bindinglist", cparams, uparams, options)

    def channeladdperm(self, *, cid, permvalue, permid=None, permsid=None):
        """
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

        cparams["cid"] = cid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        uparams[0]["permvalue"] = permvalue
        return self._return_proxy("channeladdperm", cparams, uparams, options)

    def channelclientaddperm(self, *, cid, cldbid,
                             permvalue, permid=None, permsid=None):
        """
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

        cparams["cid"] = cid
        cparams["cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        uparams[0]["permvalue"] = permvalue
        return self._return_proxy("channelclientaddperm", cparams, uparams, options)

    def channelclientdelperm(self, *, cid, cldbid, permsid=None, permid=None):
        """
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

        cparams["cid"] = cid
        cparams["cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        return self._return_proxy("channelclientdelperm", cparams, uparams, options)

    def channelclientpermlist(self, *, cid, cldbid, permsid=False):
        """
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

        cparams["cid"] = cid
        cparams["cldbid"] = cldbid

        if permsid:
            option.append("permsid")
        return self._return_proxy("channelclientpermlist", cparams, uparams, options)

    def channelcreate(self, *, channel_name, **channel_properties):
        """
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

        cparams["channel_name"] = channel_name
        cparams.update(channel_properties)
        return self._return_proxy("channelcreate", cparams, uparams, options)

    def channeldelete(self, *, cid, force):
        """
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

        cparams["cid"] = cid
        cparams["force"] = force
        return self._return_proxy("channeldelete", cparams, uparams, options)

    def channeldelperm(self, *, cid, permsid=None, permid=None):
        """
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

        cparams["cid"] = cid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        return self._return_proxy("channeldelperm", cparams, uparams, options)

    def channeledit(self, *, cid, **channel_properties):
        """
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

        cparams["cid"] = cid
        cparams.update(channel_properties)
        return self._return_proxy("channeledit", cparams, uparams, options)

    def channelfind(self, *, pattern=None):
        """
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

        cparams["pattern"] = pattern
        return self._return_proxy("channelfind", cparams, uparams, options)

    def channelgroupadd(self, *, name, type_=None):
        """
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

        cparams["name"] = name
        cparams["type"] = type_
        return self._return_proxy("channelgroupadd", cparams, uparams, options)

    def channelgroupaddperm(self, *, cgid,
                            permvalue, permid=None, permsid=None):
        """
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

        cparams["cgid"] = cgid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        uparams[0]["permvalue"] = permvalue
        return self._return_proxy("channelgroupaddperm", cparams, uparams, options)

    def channelgroupclientlist(self, *, cid=None, cldbid=None, cgid=None):
        """
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

        cparams["cid"] = cid
        cparams["cldbid"] = cldbid
        cparams["cgid"] = cgid
        return self._return_proxy("channelgroupclientlist", cparams, uparams, options)

    def channelgroupcopy(self, *, scgid, tcgid, name, type_):
        """
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

        cparams["scgid"] = scgid
        cparams["tcgid"] = tcgid
        cparams["name"] = name
        cparams["type"] = type_
        return self._return_proxy("channelgroupcopy", cparams, uparams, options)

    def channelgroupdel(self, *, cgid, force):
        """
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

        cparams["cgid"] = cgid
        cparams["force"] = force
        return self._return_proxy("channelgroupdel", cparams, uparams, options)

    def channelgroupdelperm(self, *, cgid, permid=None, permsid=None):
        """
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

        cparams["cgid"] = cgid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        return self._return_proxy("channelgroupdelperm", cparams, uparams, options)

    def channelgrouplist(self):
        """
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
        return self._return_proxy("channelgrouplist", cparams, uparams, options)

    def channelgrouppermlist(self, *, cgid, permsid=False):
        """
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

        cparams["cgid"] = cgid

        if permsid:
            options.append("permsid")
        return self._return_proxy("channelgrouppermlist", cparams, uparams, options)

    def channelgrouprename(self, *, cgid, name):
        """
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

        cparams["cgid"] = cgid
        cparams["name"] = name
        return self._return_proxy("channelgrouprename", cparams, uparams, options)

    def channelinfo(self, *, cid):
        """
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

        cparams["cid"] = cid
        return self._return_proxy("channelinfo", cparams, uparams, options)

    def channellist(self, *, topic=False, flags=False, voice=False,
                    limits=False, icon=False, secondsempty=False):
        """
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
            options.append("topic")
        if flags:
            options.append("flags")
        if voice:
            options.append("voice")
        if limits:
            options.append("limits")
        if icon:
            options.append("icon")
        if secondsempty:
            options.append("secondsempty")
        return self._return_proxy("channellist", cparams, uparams, options)

    def channelmove(self, *, cid, cpid, order=None):
        """
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

        cparams["cid"] = cid
        cparams["cpid"] = cpid
        cparams["order"] = order
        return self._return_proxy("channelmove", cparams, uparams, options)

    def channelpermlist(self, *, cid, permsid=False):
        """
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

        cparams["cid"] = cid

        if permsid:
            options.append("permsid")
        return self._return_proxy("channelpermlist", cparams, uparams, options)

    def clientaddperm(self, *, cldbid, permvalue, permskip,
                      permid=None, permsid=None):
        """
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

        cparams["cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        uparams[0]["permvalue"] = permvalue
        uparams[0]["permskip"] = permskip
        return self._return_proxy("clientaddperm", cparams, uparams, options)

    def clientdbdelete(self, *, cldbid):
        """
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

        cparams["cldbid"] = cldbid
        return self._return_proxy("clientdbdelete", cparams, uparams, options)

    def clientdbedit(self, *, cldbid, **client_properties):
        """
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

        cparams["cldbid"] = cldbid
        cparams.update(client_properties)
        return self._return_proxy("clientdbedit", cparams, uparams, options)

    def clientdbfind(self, *, pattern, uid=False):
        """
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

        cparams["pattern"] = pattern

        if uid:
            options.append("uid")
        return self._return_proxy("clientdbfind", cparams, uparams, options)

    def clientdbinfo(self, *, cldbid):
        """
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

        cparams["cldbid"] = cldbid
        return self._return_proxy("clientdbinfo", cparams, uparams, options)

    def clientdblist(self, *, start=None, duration=None, count=False):
        """
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

        cparams["start"] = start
        cparams["duration"] = duration

        if count:
            options.append("count")
        return self._return_proxy("clientdblist", cparams, uparams, options)

    def clientdelperm(self, *, cldbid, permid=None, permsid=None):
        """
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

        cparams["cldbid"] = cldbid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        return self._return_proxy("clientdelperm", cparams, uparams, options)

    def clientedit(self, *, clid, **client_properties):
        """
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

        cparams["clid"] = clid
        cparams.update(client_properties)
        return self._return_proxy("clientedit", cparams, uparams, options)

    def clientfind(self, *, pattern):
        """
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

        cparams["pattern"] = pattern
        return self._return_proxy("clientfind", cparams, uparams, options)

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

    def clientgetdbidfromuid(self, *, cluid):
        """
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

        cparams["cluid"] = cluid
        return self._return_proxy("clientgetdbidfromuid", cparams, uparams, options)

    def clientgetids(self, *, cluid):
        """
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

        cparams["cluid"] = cluid
        return self._return_proxy("clientgetids", cparams, uparams, options)

    def clientgetnamefromdbid(self, *, cldbid):
        """
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

        cparams["cldbid"] = cldbid
        return self._return_proxy("clientgetnamefromdbid", cparams, uparams, options)

    def clientgetnamefromuid(self, *, cluid):
        """
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

        cparams["cluid"] = cluid
        return self._return_proxy("clientgetnamefromuid", cparams, uparams, options)

    def clientgetuidfromclid(self, *, clid):
        """
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

        cparams["clid"] = clid
        return self._return_proxy("clientgetuidfromclid", cparams, uparams, options)

    def clientinfo(self, *, clid):
        """
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

        cparams["clid"] = clid
        return self._return_proxy("clientinfo", cparams, uparams, options)

    def clientkick(self, *, clid, reasonid, reasonmsg=None):
        """
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

        cparams["reasonid"] = reasonid
        cparams["reasonmsg"] = reasonmsg

        uparams.append(OrderedDict())
        uparams[0]["clid"] = clid
        return self._return_proxy("clientkick", cparams, uparams, options)

    def clientlist(self, *, uid=False, away=False, voice=False, times=False,
                   groups=False, info=False, country=False, ip=False):
        """
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
            options.append("uid")
        if away:
            options.append("away")
        if voice:
            options.append("voice")
        if times:
            options.append("times")
        if groups:
            options.append("groups")
        if info:
            options.append("info")
        if country:
            options.append("country")
        if ip:
            options.append("ip")
        return self._return_proxy("clientlist", cparams, uparams, options)

    def clientmove(self, *, clid, cid, cpw=None):
        """
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

        cparams["cid"] = cid
        cparams["cpw"] = cpw

        uparams.append(OrderedDict())
        uparams[0]["clid"] = clid
        return self._return_proxy("clientmove", cparams, uparams, options)

    def clientpermlist(self, *, cldbid, permsid=False):
        """
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

        cparams["cldbid"] = cldbid

        if permsid:
            options.append("permsid")
        return self._return_proxy("clientpermlist", cparams, uparams, options)

    def clientpoke(self, *, msg, clid):
        """
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

        cparams["msg"] = msg
        cparams["clid"] = clid
        return self._return_proxy("clientpoke", cparams, uparams, options)

    def clientsetserverquerylogin(self, *, client_login_name):
        """
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

        cparams["client_login_name"] = client_login_name
        return self._return_proxy("clientsetserverquerylogin", cparams, uparams, options)

    def clientupdate(self, **client_properties):
        """
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
        return self._return_proxy("clientupdate", cparams, uparams, options)

    def complainadd(self, *, tcldbid, message):
        """
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

        cparams["tcldbid"] = tcldbid
        cparams["message"] = message
        return self._return_proxy("complainadd", cparams, uparams, options)

    def complaindel(self, *, tcldbid, fcldbid):
        """
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

        cparams["tcldbid"] = tcldbid
        cparams["fcldbid"] = fcldbid
        return self._return_proxy("complaindel", cparams, uparams, options)

    def complaindelall(self, *, tcldbid):
        """
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

        cparams["tcldbid"] = tcldbid
        return self._return_proxy("complaindelall", cparams, uparams, options)

    def complainlist(self, *, tcldbid=None):
        """
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

        cparams["tcldbid"] = tcldbid
        return self._return_proxy("complainlist", cparams, uparams, options)

    def custominfo(self, *, cldbid):
        """
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

        cparams["cldbid"] = cldbid
        return self._return_proxy("custominfo", cparams, uparams, options)

    def customsearch(self, *, ident, pattern):
        """
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

        cparams["ident"] = ident
        cparams["pattern"] = pattern
        return self._return_proxy("customsearch", cparams, uparams, options)

    def ftcreatedir(self, *, cid, dirname, cpw=None):
        """
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

        cparams["cid"] = cid
        cparams["cpw"] = cpw if cpw is not None else ""
        cparams["dirname"] = dirname
        return self._return_proxy("ftcreatedir", cparams, uparams, options)

    def ftdeletefile(self, *, cid, name, cpw=None):
        """
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

        cparams["cid"] = cid
        cparams["cpw"] = cpw if cpw is not None else str()

        uparams.append(OrderedDict())
        uparams[0]["name"] = name
        return self._return_proxy("ftdeletefile", cparams, uparams, options)

    def ftgetfileinfo(self, *, name, cid, cpw=None):
        """
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
        uparams[0]["cid"] = cid
        uparams[0]["cpw"] = cpw if cpw is not None else str()
        uparams[0]["name"] = name
        return self._return_proxy("ftgetfileinfo", cparams, uparams, options)

    def ftgetfilelist(self, *, path, cid, cpw=None):
        """
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

        cparams["cid"] = cid
        cparams["cpw"] = cpw if cpw is not None else str()
        cparams["path"] = path
        return self._return_proxy("ftgetfilelist", cparams, uparams, options)

    def ftinitdownload(self, *, clientftfid, name, seekpos, cid, cpw=None):
        """
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

        cparams["clientftfid"] = clientftfid
        cparams["name"] = name
        cparams["cid"] = cid
        cparams["cpw"] = cpw if cpw is not None else str()
        cparams["seekpos"] = seekpos
        return self._return_proxy("ftinitdownload", cparams, uparams, options)

    def ftinitupload(self, *, clientftfid, name, cid, size, overwrite, resume,
                     cpw=None):
        """
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

        cparams["clientftfid"] = clientftfid
        cparams["name"] = name
        cparams["cid"] = cid
        cparams["cpw"] = cpw if cpw is not None else str()
        cparams["size"] = size
        cparams["overwrite"] = overwrite
        cparams["resume"] = resume
        return self._return_proxy("ftinitupload", cparams, uparams, options)

    def ftlist(self):
        """
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
        return self._return_proxy("ftlist", cparams, uparams, options)

    def ftrenamefile(self, *, cid, oldname, newname, cpw=None, tcid=None,
                     tcpw=None):
        """
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

        cparams["cid"] = cid
        cparams["cpw"] = cpw if cpw is not None else str()
        cparams["tcid"] = tcid
        cparams["tcpw"] = tcpw
        cparams["oldname"] = oldname
        cparams["newname"] = newname
        return self._return_proxy("ftrenamefile", cparams, uparams, options)

    def ftstop(self, *, serverftfid, delete):
        """
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

        cparams["serverftfid"] = serverftfid
        cparams["delete"] = delete
        return self._return_proxy("ftstop", cparams, uparams, options)

    def gm(self, *, msg):
        """
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

        cparams["msg"] = msg
        return self._return_proxy("gm", cparams, uparams, options)

    def help(self, *, cmd=None):
        """
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

        cparams[""] = cmd
        return self._return_proxy("help", cparams, uparams, options)

    def hostinfo(self):
        """
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
        return self._return_proxy("hostinfo", cparams, uparams, options)

    def instanceedit(self, **instance_properties):
        """
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
        return self._return_proxy("instanceedit", cparams, uparams, options)

    def instanceinfo(self):
        """
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
        return self._return_proxy("instanceinfo", cparams, uparams, options)

    def logadd(self, *, loglevel, logmsg):
        """
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

        cparams["loglevel"] = loglevel
        cparams["logmsg"] = logmsg
        return self._return_proxy("logadd", cparams, uparams, options)

    def login(self, *, client_login_name, client_login_password):
        """
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

        cparams["client_login_name"] = client_login_name
        cparams["client_login_password"] = client_login_password
        return self._return_proxy("login", cparams, uparams, options)

    def logout(self):
        """
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
        return self._return_proxy("logout", cparams, uparams, options)

    def logview(self, *, lines=None, reverse=None, instance=None,
                begin_pos=None):
        """
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

        cparams["lines"] = lines
        cparams["reverse"] = reverse
        cparams["instance"] = instance
        cparams["begin_pos"] = begin_pos
        return self._return_proxy("logview", cparams, uparams, options)

    def messageadd(self, *, cluid, subject, message):
        """
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

        cparams["cluid"] = cluid
        cparams["subject"] = subject
        cparams["message"] = message
        return self._return_proxy("messageadd", cparams, uparams, options)

    def messagedel(self, *, msgid):
        """
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

        cparams["msgid"] = msgid
        return self._return_proxy("messagedel", cparams, uparams, options)

    def messageget(self, *, msgid):
        """
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

        cparams["msgid"] = msgid
        return self._return_proxy("messageget", cparams, uparams, options)

    def messagelist(self):
        """
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
        return self._return_proxy("messagelist", cparams, uparams, options)

    def messageupdateflag(self, *, msgid, flag):
        """
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

        cparams["msgid"] = msgid
        cparams["flag"] = flag
        return self._return_proxy("messageupdateflag", cparams, uparams, options)

    def permfind(self, *, permid):
        """
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

        cparams["permid"] = permid
        return self._return_proxy("permfind", cparams, uparams, options)

    def permget(self, *, permid=None, permsid=None):
        """
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

        cparams["permid"] = permid
        cparams["permsid"] = permsid
        return self._return_proxy("permget", cparams, uparams, options)

    def permidgetbyname(self, *, permsid=None):
        """
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
        uparams[0]["permsid"] = permsid
        return self._return_proxy("permidgetbyname", cparams, uparams, options)

    def permissionlist(self):
        """
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
        return self._return_proxy("permissionlist", cparams, uparams, options)

    def permoverview(self, *, cid, cldbid, permid):
        """
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

        cparams["cid"] = cid
        cparams["cldbid"] = cldbid
        cparams["permid"] = permid
        return self._return_proxy("permoverview", cparams, uparams, options)

    def permreset(self):
        """
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
        return self._return_proxy("permreset", cparams, uparams, options)

    def privilegekeyadd(self, *, tokentype, tokenid1, tokenid2,
                        tokendescription=None, tokencustomset=None):
        """
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

        cparams["tokentype"] = tokentype
        cparams["tokenid1"] = tokenid1
        cparams["tokenid2"] = tokenid2
        cparams["tokendescription"] = tokendescription
        cparams["tokencustomset"] = tokencustomset
        return self._return_proxy("privilegekeyadd", cparams, uparams, options)

    def privilegekeydelete(self, *, token):
        """
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

        cparams["token"] = token
        return self._return_proxy("privilegekeydelete", cparams, uparams, options)

    def privilegekeylist(self):
        """
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
        return self._return_proxy("privilegekeylist", cparams, uparams, options)

    def privilegekeyuse(self, *, token):
        """
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

        cparams["token"] = token
        return self._return_proxy("privilegekeyuse", cparams, uparams, options)

    def quit(self):
        """
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
        return self._return_proxy("quit", cparams, uparams, options)

    def sendtextmessage(self, *, targetmode, target, msg):
        """
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

        cparams["targetmode"] = targetmode
        cparams["target"] = target
        cparams["msg"] = msg
        return self._return_proxy("sendtextmessage", cparams, uparams, options)

    def servercreate(self, **virtualserver_properties):
        """
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
        return self._return_proxy("servercreate", cparams, uparams, options)

    def serverdelete(self, *, sid):
        """
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

        cparams["sid"] = sid
        return self._return_proxy("serverdelete", cparams, uparams, options)

    def serveredit(self, **virtualserver_properties):
        """
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
        return self._return_proxy("serveredit", cparams, uparams, options)

    def servergroupadd(self, *, name, type_=None):
        """
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

        cparams["name"] = name
        cparams["type"] = type_
        return self._return_proxy("servergroupadd", cparams, uparams, options)

    def servergroupaddclient(self, *, sgid, cldbid):
        """
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

        cparams["sgid"] = sgid
        cparams["cldbid"] = cldbid
        return self._return_proxy("servergroupaddclient", cparams, uparams, options)

    def servergroupaddperm(self, *, sgid, permnegated, permskip,
                           permid=None, permsid=None, permvalue=None):
        """
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
        uparams[0]["sgid"] = sgid
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        uparams[0]["permvalue"] = permvalue
        uparams[0]["permnegated"] = permnegated
        uparams[0]["permskip"] = permskip
        return self._return_proxy("servergroupaddperm", cparams, uparams, options)

    def servergroupautoaddperm(self, *, sgtype, permvalue, permnegated,
                               permskip, permid=None, permsid=None):
        """
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
        uparams[0]["sgtype"] = sgtype
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        uparams[0]["permvalue"] = permvalue
        uparams[0]["permnegated"] = permnegated
        uparams[0]["permskip"] = permskip
        return self._return_proxy("servergroupautoaddperm", cparams, uparams, options)

    def servergroupautodelperm(self, *, sgtype, permid=None, permsid=None):
        """
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

        cparams["sgtype"] = sgtype

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        return self._return_proxy("servergroupautodelperm", cparams, uparams, options)

    def servergroupbyclientid(self, *, cldbid):
        """
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

        cparams["cldbid"] = cldbid
        return self._return_proxy("servergroupbyclientid", cparams, uparams, options)

    def servergroupclientlist(self, *, sgid, names=False):
        """
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

        cparams["sgid"] = sgid

        if names:
            options.append("names")
        return self._return_proxy("servergroupclientlist", cparams, uparams, options)

    def servergroupcopy(self, *, ssgid, tsgid, name, type_):
        """
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

        cparams["ssgid"] = ssgid
        cparams["tsgid"] = tsgid
        cparams["name"] = name
        cparams["type"] = type_
        return self._return_proxy("servergroupcopy", cparams, uparams, options)

    def servergroupdel(self, *, sgid, force=False):
        """
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

        cparams["sgid"] = sgid
        cparams["force"] = force
        return self._return_proxy("servergroupdel", cparams, uparams, options)

    def servergroupdelclient(self, *, sgid, cldbid):
        """
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

        cparams["sgid"] = sgid
        cparams["cldbid"] = cldbid
        return self._return_proxy("servergroupdelclient", cparams, uparams, options)

    def servergroupdelperm(self, *, sgid, permid=None, permsid=None):
        """
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

        cparams["sgid"] = sgid

        uparams.append(OrderedDict())
        uparams[0]["permid"] = permid
        uparams[0]["permsid"] = permsid
        return self._return_proxy("servergroupdelperm", cparams, uparams, options)

    def servergrouplist(self):
        """
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
        return self._return_proxy("servergrouplist", cparams, uparams, options)

    def servergrouppermlist(self, *, sgid, permsid=False):
        """
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

        cparams["sgid"] = sgid

        if permsid:
            options.append("permsid")
        return self._return_proxy("servergrouppermlist", cparams, uparams, options)

    def servergrouprename(self, *, sgid, name):
        """
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

        cparams["sgid"] = sgid
        cparams["name"] = name
        return self._return_proxy("servergrouprename", cparams, uparams, options)

    def servergroupsbyclientid(self, *, cldbid):
        """
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

        cparams["cldbid"] = cldbid
        return self._return_proxy("servergroupsbyclientid", cparams, uparams, options)

    def serveridgetbyport(self, *, virtualserver_port):
        """
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

        cparams["virtualserver_port"] = virtualserver_port
        return self._return_proxy("serveridgetbyport", cparams, uparams, options)

    def serverinfo(self):
        """
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
        return self._return_proxy("serverinfo", cparams, uparams, options)

    def serverlist(self, *, uid=False, all_=False, short=False,
                   onlyoffline=False):
        """
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
            options.append("uid")
        if all_:
            options.append("all")
        if short:
            options.append("short")
        if onlyoffline:
            options.append("onlyoffline")
        return self._return_proxy("serverlist", cparams, uparams, options)

    def servernotifyregister(self, *, event, id_=None):
        """
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

        cparams["id"] = id_
        cparams["event"] = event
        return self._return_proxy("servernotifyregister", cparams, uparams, options)

    def servernotifyunregister(self):
        """
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
        return self._return_proxy("servernotifyunregister", cparams, uparams, options)

    def serverprocessstop(self):
        """
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
        return self._return_proxy("serverprocessstop", cparams, uparams, options)

    def serverrequestconnectioninfo(self):
        """
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
        return self._return_proxy("serverrequestconnectioninfo", cparams, uparams, options)

    def serversnapshotcreate(self):
        """
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
        return self._return_proxy("serversnapshotcreate", cparams, uparams, options)

    def serversnapshotdeploy(self, *, virtualserver_snapshot):
        """
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

        cparams[""] = RawParameter(virtualserver_snapshot)
        return self._return_proxy("serversnapshotdeploy", cparams, uparams, options)

    def serverstart(self, *, sid):
        """
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

        cparams["sid"] = sid
        return self._return_proxy("serverstart", cparams, uparams, options)

    def serverstop(self, *, sid):
        """
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

        cparams["sid"] = sid
        return self._return_proxy("serverstop", cparams, uparams, options)

    def servertemppasswordadd(self, *, pw, desc, duration, tcid, tcpw):
        """
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

        cparams["pw"] = pw
        cparams["desc"] = desc
        cparams["duration"] = duration
        cparams["tcid"] = tcid
        cparams["tcpw"] = tcpw
        return self._return_proxy("servertemppasswordadd", cparams, uparams, options)

    def servertemppassworddel(self, *, pw):
        """
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

        cparams["pw"] = pw
        return self._return_proxy("servertemppassworddel", cparams, uparams, options)

    def servertemppasswordlist(self):
        """
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
        return self._return_proxy("servertemppasswordlist", cparams, uparams, options)

    def setclientchannelgroup(self, *, cgid, cid, cldbid):
        """
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

        cparams["cgid"] = cgid
        cparams["cid"] = cid
        cparams["cldbid"] = cldbid
        return self._return_proxy("setclientchannelgroup", cparams, uparams, options)

    def tokenadd(self, *, tokentype, tokenid1, tokenid2, tokendescription=None,
                 tokencustomset=None):
        """
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

        cparams["tokentype"] = tokentype
        cparams["tokenid1"] = tokenid1
        cparams["tokenid2"] = tokenid2
        cparams["tokendescription"] = tokendescription
        cparams["tokencustomset"] = tokencustomset
        return self._return_proxy("tokenadd", cparams, uparams, options)

    def tokendelete(self, *, token):
        """
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

        cparams["token"] = token
        return self._return_proxy("tokendelete", cparams, uparams, options)

    def tokenlist(self):
        """
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
        return self._return_proxy("tokenlist", cparams, uparams, options)

    def tokenuse(self, *, token):
        """
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

        cparams["token"] = token
        return self._return_proxy("tokenuse", cparams, uparams, options)

    def use(self, *, sid=None, port=None, virtual=False):
        """
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

        cparams["sid"] = sid
        cparams["port"] = port

        if virtual:
            options.append("virtual")
        return self._return_proxy("use", cparams, uparams, options)

    def version(self):
        """
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
        return self._return_proxy("version", cparams, uparams, options)

    def whoami(self):
        """
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
        return self._return_proxy("whoami", cparams, uparams, options)
