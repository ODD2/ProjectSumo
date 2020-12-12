from enum import IntEnum

# Link type
class LinkType(IntEnum):
    UPLINK = 0
    DOWNLINK = 1

# Base station type
class BaseStationType(IntEnum):
    UMI = 0
    UMA = 1

# Dummy Broadcast object class
class BroadcastObject():
	name = 'broadcast'
