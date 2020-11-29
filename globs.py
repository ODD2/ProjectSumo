import os
import math
import threading
import os
import traci
import sys
import matlab.engine
from sg_meta import SocialGroupMeta
from numpy import random
from enum import IntEnum, Enum


# Link type
class LinkType(IntEnum):
    UPLINK = 0
    DOWNLINK = 1


# Base station type
class BaseStationType(IntEnum):
    UMI = 0
    UMA = 1


# SocialGroup and QOS priority(Lower value has higher priority, 0 is the lowest value.)
class SocialGroup(metaclass=SocialGroupMeta):
    CRITICAL = 0
    GENERAL = 1


# Network object layer
class NetObjLayer(IntEnum):
    BS_POI = 2
    BS_RAD_UMA = BS_POI - 2
    BS_RAD_UMI = BS_POI - 1
    CON_LINE = BS_POI + 1


# Simulation Infos
class SumoSimInfo:
    def __init__(self):
        self.new_veh_ids = []
        self.veh_ids = []
        self.ghost_veh_ids = []
        self.time = 0

    def UpdateSS(self):
        self.time = traci.simulation.getTime()
        # net step
        self.ns = 0
        # time step
        self.ts = 0
        # vehicles currently on the map
        cur_veh_ids = traci.vehicle.getIDList()
        # Find the vehicles that've left the map
        self.ghost_veh_ids = [
            veh_id for veh_id in self.veh_ids if veh_id not in cur_veh_ids
        ]
        # Find the vehicles that've joined the map
        self.new_veh_ids = [
            veh_id for veh_id in cur_veh_ids if veh_id not in self.veh_ids
        ]
        # Update current vehicle ids
        self.veh_ids = cur_veh_ids

    def UpdateNS(self, ns):
        self.ns = ns

    def UpdateTS(self, ts):
        self.ts = ts


# Threading -Traci
TRACI_LOCK = threading.Lock()

# Matlab
MATLAB_ENG = matlab.engine.start_matlab()
MATLAB_ENG.addpath(os.getcwd() + "/matlab/")
MATLAB_ENG.addpath(os.getcwd() + "/matlab/SelectCQI_bySNR/")
MATLAB_ENG.addpath(os.getcwd() + "/matlab/NomaPlannerV1/")

# Random Number Generator
# . initialize the rng
random.seed(132342421)
# Sumo Simulation Settings
# . simulation info
SUMO_SIM_INFO = SumoSimInfo()
# . simulation scaler
SUMO_SIM_TIME_SCALER = 100
# . seconds per sumo simulation step
SUMO_SECONDS_PER_STEP = 0.001*SUMO_SIM_TIME_SCALER
# . total sumo simulation steps
SUMO_TOTAL_STEPS = (1 / SUMO_SECONDS_PER_STEP) * 100

# Network Settings
# . total QoS network channels. qos channel starts from 0.
NET_QOS_CHNLS = (max(SocialGroup, key=lambda x: x.qos).qos) + 1
# . resource block symbols
NET_RB_SLOT_SYMBOLS = 14
# . seconds per network simulation step
NET_SECONDS_PER_STEP = 0.001*SUMO_SIM_TIME_SCALER
# . network simulation steps per sumo simulation step
NET_STEPS_PER_SUMO_STEP = int(SUMO_SECONDS_PER_STEP / NET_SECONDS_PER_STEP)
# . seconds per network timeslot
NET_SECONDS_PER_TS = 0.0005*SUMO_SIM_TIME_SCALER
# . network timeslots per network simulation step
NET_TS_PER_NET_STEP = int(NET_SECONDS_PER_STEP/NET_SECONDS_PER_TS)
# . resource block bandwidth units
NET_RB_BW_UNIT = 180000
# . resource block bandwidth required timeslot(s)
NET_RB_BW_REQ_TS = {2 * NET_RB_BW_UNIT: 1,
                    1 * NET_RB_BW_UNIT: 2}
# . social group random request size
NET_SG_RND_REQ_SIZE = {
    SocialGroup.CRITICAL: [300, 1100],
    SocialGroup.GENERAL: [64, 2048],
    # SocialGroup.CRITICAL: [10, 50],
    # SocialGroup.GENERAL: [20, 100],
}


# Base Station Settings
# . base station's total bandwidth
BS_TOTAL_BANDWIDTH = {
    BaseStationType.UMA: 20000000,
    BaseStationType.UMI: 10000000
    # BaseStationType.UMA: 200000,
    # BaseStationType.UMI: 100000,
}
# . base station's frequency
BS_FREQ = {
    # Ghz
    BaseStationType.UMA: 2,
    BaseStationType.UMI: 3.5,
}
# . base station's maximum power
BS_TRANS_PWR = {
    # dBm
    BaseStationType.UMA: 23,
    BaseStationType.UMI: 10,
}
# . base station's antenna height
BS_HEIGHT = {
    # m
    BaseStationType.UMA: 25,
    BaseStationType.UMI: 10
}
# . base station's radius color
BS_RADIUS_COLOR = {
    BaseStationType.UMA: (255, 0, 0, 64),
    BaseStationType.UMI: (0, 255, 0, 64)
}
# . base station's radius
BS_RADIUS = {
    BaseStationType.UMA: 500,
    BaseStationType.UMI: 50,
}
# . uma base station's cyclic prefix
BS_UMA_CP = 4.69
# . umi base station's cyclic prefix
BS_UMI_CP_SOCIAL = {
    SocialGroup.CRITICAL: 2.34,
    SocialGroup.GENERAL: 4.69
}
# . uma base station's resource block bandwidth
BS_UMA_RB_BW = 1 * NET_RB_BW_UNIT
# . umi base station's resource block bandwidth
BS_UMI_RB_BW_SG = {
    SocialGroup.CRITICAL: 2 * NET_RB_BW_UNIT,
    SocialGroup.GENERAL: 1 * NET_RB_BW_UNIT
}

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

# Frequently used constants
TS_PER_NET_STEP = int(NET_SECONDS_PER_STEP/NET_SECONDS_PER_TS)


# Basic Requirement Check
if SUMO_SECONDS_PER_STEP < NET_SECONDS_PER_STEP:
    print(
        "Error: seconds per simulation step should be larger than the value of seconds per network step."
    )
    sys.exit()
if SUMO_SECONDS_PER_STEP / NET_SECONDS_PER_STEP % 1 != 0:
    print(
        "Error: seconds per simulation step should be totally devided by the value of seconds per network step."
    )
    sys.exit()
if NET_SECONDS_PER_STEP/NET_SECONDS_PER_TS % 1 != 0:
    print(
        "Error: seconds per network simulation step should be totally devided by the value of seconds per network timeslot."
    )
    sys.exit()
