"""
od/misc/types.py - Debug message type flag definitions.
"""
from enum import IntFlag


class DebugMsgType(IntFlag):
    """Bitmask flags that categorise debug log messages by subsystem.

    Combine flags with | to enable multiple categories simultaneously.
    Set DEBUG_MSG_FLAGS in od/env/config.py to control which categories
    are written to the debug log.

    Attributes:
        NONE:             No debug output.
        NET_APPDATA_INFO: Application-data lifecycle events (spawn, intact).
        NET_PKG_INFO:     Network package create/deliver/receive events.
        NET_ALLOC_INFO:   Resource allocation reports per network step.
        NET_SINR_INFO:    SINR/CQI computation details.
        SUMO_VEH_INFO:    Vehicle join/leave events in the SUMO simulation.
        MATLAB_INFO:      Raw stdout captured from MATLAB engine calls.
    """
    NONE = 0
    NET_APPDATA_INFO = 1 << 0
    NET_PKG_INFO = 1 << 1
    NET_ALLOC_INFO = 1 << 2
    NET_SINR_INFO = 1 << 3
    SUMO_VEH_INFO = 1 << 4
    MATLAB_INFO = 1 << 5
