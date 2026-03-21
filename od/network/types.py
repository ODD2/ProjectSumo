"""
od/network/types.py - Network-layer enumeration types.
"""
from enum import IntEnum


class LinkType(IntEnum):
    """Direction of a network transmission."""
    UPLINK = 0
    DOWNLINK = 1


class BaseStationType(IntEnum):
    """5G NR cell deployment type.

    UMI (Urban Micro / small cell) has a 50 m radius and targets low-latency
    critical traffic.  UMA (Urban Macro) has a 500 m radius and handles
    general-purpose V2X traffic.
    """
    UMI = 0
    UMA = 1


class ResourceAllocatorType(IntEnum):
    """Downlink resource allocation algorithm selection.

    OMA:       Orthogonal Multiple Access – each RB is assigned to one group.
    NOMA_OPT:  Non-Orthogonal MA with optimal power allocation via MATLAB solver.
    NOMA_APR:  Non-Orthogonal MA with fast approximation (no MATLAB optimisation).
    """
    OMA = 0,
    NOMA_OPT = 1,
    NOMA_APR = 2,


class NetworkCastType:
    """Transmission addressing modes for network packages."""
    Broadcast = 0,
    Multicast = 1,
    Unicast = 2,
