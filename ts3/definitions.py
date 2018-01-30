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

"""
:mod:`ts3.definitions`
======================

This module contains the definitions described in the TeamSpeak 3 Server Manual,
so that the variables can be used instead of the constans to improve the
readability of the code.
"""


__all__ = [
    "HostMessageMode",
    "HostBannerMode",
    "Codec",
    "CodecEncryptionMode",
    "TextMessageTargetMode",
    "LogLevel",
    "ReasonIdentifier",
    "PermissionGroupDatabaseTypes",
    "PermissionGroupTypes",
    "TokenType"
    ]


class HostMessageMode(object):

    #: don't display anything
    NONE = 0
    #: display message in chatlog
    LOG = 1
    #: display message in modal dialog
    MODAL = 2
    #: display message in modal dialog and close connection
    MODALQUIT = 3

class HostBannerMode(object):

    #: do not adjust
    NOADJUST = 0
    #: adjust but ignore aspect ratio (like TeamSpeak 2)
    IGNOREASPECT = 1
    #: adjust and keep aspect ratio
    KEEPASPECT = 2

class Codec(object):

    #: speex narrowband (mono, 16bit, 8kHz)
    SPEEX_NARROWBAND = 0
    #: speex wideband (mono, 16bit, 16kHz)
    SPEEX_WIDEBAND = 1
    #: speex ultra-wideband (mono, 16bit, 32kHz)
    SPEEX_ULTRAWIDEBAND = 2
    #: celt mono (mono, 16bit, 48kHz)
    CELT_MONO = 3

class CodecEncryptionMode(object):

    #: configure per channel
    INDIVIDUAL = 0
    #: globally disabled
    DISABLED = 1
    #: globally enabled
    ENABLED = 2

class TextMessageTargetMode(object):

    #: target is a client
    CLIENT = 1
    #: target is a channel
    CHANNEL = 2
    #: target is a virtual server
    SERVER = 3

class LogLevel(object):

    #: everything that is really bad
    ERROR = 1
    #: everything that might be bad
    WARNING = 2
    #: output that might help find a problem
    DEBUG = 3
    #: informational output
    INFO = 4

class ReasonIdentifier(object):

    #: kick client from channel
    KICK_CHANNEL = 4
    #: kick client from server
    KICK_SERVER = 5

class PermissionGroupDatabaseTypes(object):

    #: template group (used for new virtual server)
    Template = 0
    #: regular group (used for regular clients)
    Regular = 1
    #: global query group (used for ServerQuery clients)
    Query = 2

class PermissionGroupTypes(object):

    #: server group permission
    ServerGroup = 0
    #: client specific permission
    GlobalClient = 1
    #: channel specific permission
    Channel = 2
    #: channel group permission
    ChannelGroup = 3
    #: channel-client specific permission
    ChannelClient = 4

class TokenType(object):

    #: server group token (id1={groupID} id2=0)
    ServerGroup = 0
    #: channel group token (id1={groupID} id2={channelID})
    ChannelGroup = 1
