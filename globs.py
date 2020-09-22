import os
import math
import threading
import matlab
import os
from numpy import random
from enum import IntEnum, Enum


class LinkType(IntEnum):
    UPLOAD = 0
    DOWNLOAD = 1


# Base station type
class BaseStationType(IntEnum):
    UMI = 0
    UMA = 1


# Lower Value Has Higher Priority
class SocialGroup(IntEnum):
    CRITICAL = 0
    GENERAL = 1


# Network object layer
class NetObjLayer(IntEnum):
    BS_POI = 2
    BS_RAD_UMI = BS_POI - 1
    BS_RAD_UMA = BS_POI - 2
    CON_LINE = BS_POI + 1


# Matlab
MATLAB_ENG = matlab.engine.start_matlab()
MATLAB_ENG.addpath(os.getcwd() + "\\matlab\\")
MATLAB_ENG.addpath(os.getcwd() + "\\matlab\\SelectCQI_bySNR\\")
# Traci
TRACI_LOCK = threading.Lock()
# Initialize Random (not sure if it's working)
random.seed(132342421)
# Simulation Settings
SIM_SECONDS_PER_STEP = 0.1
# Network Settings
NET_RB_SLOT_SYMBOLS = 14
NET_SECONDS_PER_STEP = 0.1
NET_RB_BANDWIDTH_TS = {180000: 1,
                       360000: 2}
NET_SG_RND_REQ_SIZE = {
    # SocialGroup.CRITICAL: [300, 1100],
    # SocialGroup.GENERAL: [64, 2048],
    SocialGroup.CRITICAL: [10, 50],
    SocialGroup.GENERAL: [20, 100],
}

# Base Station Settings
BS_UMA_FREQ = 2.0  # Ghz
BS_UMI_FREQ = 3.5  # Ghz
BS_UMA_TRANS_PWR = 23
BS_UMI_TRANS_PWR = 10
BS_UMA_HEIGHT = 25
BS_UMI_HEIGHT = 10
BS_UMA_RB_BANDWIDTH = 360000
BS_UMI_RB_BANDWIDTH_SOCIAL = {SocialGroup.CRITICAL: 180000,
                              SocialGroup.GENERAL: 360000}
BS_UMI_RADIUS_COLOR = (178, 178, 76, 128)
BS_UMA_RADIUS_COLOR = (178, 76, 76, 128)
BS_UMA_RADIUS = 500
BS_UMI_RADIUS = 50
BS_UMA_CP = 4.69
BS_UMI_CP_SOCIAL = {SocialGroup.CRITICAL: 2.34,
                    SocialGroup.GENERAL: 4.69}
BS_ALL_BANDWIDTH = 10000000

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
