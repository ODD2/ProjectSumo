from enum import IntEnum


# Link type
class LinkType(IntEnum):
    UPLINK = 0
    DOWNLINK = 1


# Base station type
class BaseStationType(IntEnum):
    UMI = 0
    UMA = 1


# Resource Allocation Method
class ResourceAllocatorType(IntEnum):
    OMA = 0,
    NOMA_OPT = 1,
    NOMA_APR = 2,


class NetworkCastType:
    Broadcast = 0,
    Multicast = 1,
    Unicast = 2,
