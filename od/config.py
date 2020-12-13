from od.network.types import BaseStationType
from od.social import SocialGroup
import os
import sys

# Sumo Simulation Settings
# . simulation scaler
SUMO_SIM_TIME_SCALER = 100
# . seconds per sumo simulation step
SUMO_SECONDS_PER_STEP = SUMO_SIM_TIME_SCALER*0.001
# . total sumo simulation steps
SUMO_TOTAL_STEPS = (1 / SUMO_SECONDS_PER_STEP) * 100

# Network Settings
# . total QoS network channels. qos channel starts from 0.
NET_QOS_CHNLS = (max(SocialGroup, key=lambda x: x.qos).qos) + 1
# . resource block symbols
NET_RB_SLOT_SYMBOLS = 14
# . seconds per network simulation step
NET_SECONDS_PER_STEP = SUMO_SIM_TIME_SCALER * 0.001
# . network simulation steps per sumo simulation step
NET_STEPS_PER_SUMO_STEP = int(SUMO_SECONDS_PER_STEP / NET_SECONDS_PER_STEP)
# . seconds per network timeslot
NET_SECONDS_PER_TS = SUMO_SIM_TIME_SCALER * 0.0005
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
# . base station's radius (m)
BS_RADIUS = {
    BaseStationType.UMA: 500,
    BaseStationType.UMI: 50,
}
# . uma base station's cyclic prefix(us)
BS_UMA_CP = 4.69
# . umi base station's cyclic prefix(us)
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


# Base Station Presets
BS_PRESET = {
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
