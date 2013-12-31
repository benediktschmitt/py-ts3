#!/usr/bin/python3


"""
Contains the enumerations defined in the TS3 ServerQuery Manual.
"""


# Data
# ------------------------------------------------
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


# Definitions
# ------------------------------------------------
class HostMessageMode(object):

    # Display message in chatlog
    LOG = 1
    # Display message in modal dialog
    MODAL = 2    
    # Display message in modal dialog and close connection.
    MODALQUIT = 3

class HostBannerMode(object):

    # do not adjust
    NOADJUST = 0
    # adjust but ignore aspect ratio (like TeamSpeak 2)
    IGNOREASPECT = 1
    # adjust and keep aspect ratio
    KEEPASPECT = 2

class Codec(object):

    # speex narrowband (mono, 16bit, 8kHz)
    SPEEX_NARROWBAND = 0
    # speex wideband (mono, 16bit, 16kHz)
    SPEEX_WIDEBAND = 1
    # speex ultra-wideband (mono, 16bit, 32kHz)
    SPEEX_ULTRAWIDEBAND = 2
    # celt mono (mono, 16bit, 48kHz)
    CELT_MONO = 3

class CodecEncryptionMode(object):

    # configure per channel
    INDIVIDUAL = 0
    # globally disabled
    DISABLED = 1
    # globally enabled
    ENABLED = 2

class TextMessageTargetMode(object):

    # target is a client
    CLIENT = 1
    # target is a channel
    CHANNEL = 2
    # target is a virtual server
    SERVER = 3

class LogLevel(object):

    # everything that is really bad
    ERROR = 1
    # everything that might be bad
    WARNING = 2
    # output that might help find a problem
    DEBUG = 3
    # informational output
    INFO = 4

class ReasonIdentifier(object):

    # kick client from channel
    KICK_CHANNEL = 4
    # kick client from server
    KICK_SERVER = 5
    
class PermissionGroupDatabaseTypes(object):

    # template group (used for new virtual server)
    Template = 0
    # regular group (used for regular clients)
    Regular = 1
    # global query group (used for ServerQuery clients)
    Query = 2

class PermissionGroupTypes(object):

    # server group permission
    ServerGroup = 0
    # client specific permission
    GlobalClient = 1
    # channel specific permission
    Channel = 2
    # channel group permission
    ChannelGroup = 3
    # channel-client specific permission
    ChannelClient = 4

class TokenType(object):

    # server group token (id1={groupID} id2=0)
    ServerGroup = 0
    # channel group token (id1={groupID} id2={channelID})
    ChannelGroup = 1
