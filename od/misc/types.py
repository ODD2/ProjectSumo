from enum import IntFlag

class DebugMsgType(IntFlag):
    NONE = 0
    NET_APPDATA_INFO = 1<<0
    NET_PKG_INFO = 1<<1
    NET_ALLOC_INFO = 1<<2
    SUMO_VEH_INFO = 1<<3
    