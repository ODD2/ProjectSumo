import os
from enum import IntEnum, Enum


class BaseStationType(IntEnum):
    UMI = 0
    UMA = 1


class SociatyGroup(IntEnum):
    GENERAL = 0
    CRITICAL = 1


class NetObjLayer(IntEnum):
    BS_POI = 2
    BS_RAD_UMI = BS_POI - 1
    BS_RAD_UMA = BS_POI - 2
    CON_LINE = BS_POI + 1


BS_UMI_RADIUS_COLOR = (178, 178, 76, 128)
BS_UMA_RADIUS_COLOR = (178, 76, 76, 128)
BS_UMA_RADIUS = 100
BS_UMI_RADIUS = 20

# Base Station Settings
BS_SETTINGS = {
    "bs1": {
        "color": (0, 0, 0, 255),
        "x": 440,
        "y": 250,
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMA,
    },
    "bs2": {
        "color": (0, 0, 0, 255),
        "x": 220,
        "y": 200,
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
    "bs3": {
        "color": (0, 0, 0, 255),
        "x": 363,
        "y": 204,
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
}


BS_BANDWIDTH_TOTAL = 10000  # Khz
BS_PER_RB_BANDWIDTH = 360  # Khz
BS_RESOURCE_BLOCK_TOTAL = BS_BANDWIDTH_TOTAL*0.9 / BS_PER_RB_BANDWIDTH
