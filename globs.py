import os
import math
from enum import IntEnum, Enum

#


class BaseStationType(IntEnum):
    UMI = 0
    UMA = 1


# Lower Value Has Higher Priority
class SociatyGroup(IntEnum):
    CRITICAL = 0
    GENERAL = 1


#
class NetObjLayer(IntEnum):
    BS_POI = 2
    BS_RAD_UMI = BS_POI - 1
    BS_RAD_UMA = BS_POI - 2
    CON_LINE = BS_POI + 1


# Network Settings
NET_RB_SLOT_SYMBOLS = 14
NET_RB_BANDWIDTH_TS = {180000: 1,
                       360000: 2}


# Base Station Settings
BS_UMA_FREQ = 2.0  # Ghz
BS_UMI_FREQ = 3.5  # Ghz
BS_UMA_TRANS_PWR = 23
BS_UMI_TRANS_PWR = 10
BS_UMA_HEIGHT = 25
BS_UMI_HEIGHT = 10
BS_UMA_RB_BANDWIDTH = 360000
BS_UMI_RB_BANDWIDTH_SOCIAL = {SociatyGroup.CRITICAL: 180000,
                              SociatyGroup.GENERAL: 360000}
BS_UMI_RADIUS_COLOR = (178, 178, 76, 128)
BS_UMA_RADIUS_COLOR = (178, 76, 76, 128)
BS_UMA_RADIUS = 500
BS_UMI_RADIUS = 50
BS_UMI_CP_SOCIAL = {SociatyGroup.CRITICAL: 2.34,
                    SociatyGroup.GENERAL: 4.69}
BS_ALL_BANDWIDTH = 10000000

# BS_UMA_RADIUS = (10**((BS_UMA_TRANS_PWR-92.45-20*math.log(2, 10))/20))*1000
# BS_UMI_RADIUS = (10**((BS_UMI_TRANS_PWR-92.45-20*math.log(3.5, 10))/20))*1000
# BS_UMA_RADIUS = (10**((BS_UMA_TRANS_PWR-32.4-20*math.log(2000, 10))/30))*1000
# BS_UMI_RADIUS = (10**((BS_UMI_TRANS_PWR-32.4-20*math.log(3500, 10))/31.9))*1000


BS_SETTINGS = {
    "bs1": {
        "color": (0, 0, 0, 255),
        "pos": (285, 245),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMA,
    },
    "bs2": {
        "color": (0, 0, 0, 255),
        "pos": (220, 200),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
    "bs3": {
        "color": (0, 0, 0, 255),
        "pos": (363, 204),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
}
