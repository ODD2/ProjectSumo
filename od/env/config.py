from . import *
from od.network.types import BaseStationType
from od.social.group import SocialGroup, QoSLevel
from od.misc.types import DebugMsgType
from od.event.config import SumoSimEventConf
import os
import sys
import math

# System Parameters
DEBUG_MSG_FLAGS = (
    # DebugMsgType.NONE
    # DebugMsgType.NET_PKG_INFO |
    # DebugMsgType.NET_APPDATA_INFO |
    DebugMsgType.NET_ALLOC_INFO
    # DebugMsgType.SUMO_VEH_INFO
)
# Sumo Simulation Settings
# . simulation sumo type
SUMO_SIM_GUI = False
# . simulation scaler
SUMO_SIM_TIME_SCALER = 1
# . seconds per sumo simulation step
SUMO_SECONDS_PER_STEP = 0.1
# . total traffic running seconds before network simulation start
SUMO_SKIP_SECONDS = 185
SUMO_SKIP_STEPS = int(round((1 / SUMO_SECONDS_PER_STEP) * SUMO_SKIP_SECONDS))
# . total network warm up seconds for a more realistic network environment.
SUMO_NET_WARMUP_SECONDS = 1
SUMO_NET_WARMUP_STEPS = int(round((SUMO_NET_WARMUP_SECONDS/SUMO_SECONDS_PER_STEP)))


# Network Settings
# . resource block symbols
NET_RB_SLOT_SYMBOLS = 14
# . seconds per network simulation step
NET_SECONDS_PER_STEP = SUMO_SIM_TIME_SCALER * 0.001
# . network simulation steps per sumo simulation step
NET_STEPS_PER_SUMO_STEP = int(round(SUMO_SECONDS_PER_STEP / NET_SECONDS_PER_STEP))
# . seconds per network timeslot
NET_SECONDS_PER_TS = SUMO_SIM_TIME_SCALER * 0.0005
# . network timeslots per network simulation step
NET_TS_PER_NET_STEP = int(round(NET_SECONDS_PER_STEP/NET_SECONDS_PER_TS))
# . network application request timeout limit.
NET_TIMEOUT_SECONDS = 7
# . resource block bandwidth units
NET_RB_BW_UNIT = 180000
# . resource block bandwidth required timeslot(s)
NET_RB_BW_REQ_TS = {2 * NET_RB_BW_UNIT: 1,
                    1 * NET_RB_BW_UNIT: 2}
# . social group random request size(bytes).
NET_QoS_RND_REQ_SIZE = {
    QoSLevel.CRITICAL: [300, 1100],
    QoSLevel.GENERAL: [64, 2048],
}
# . social group random request amount(Packages/second)
#   For general, referencing the recommened birate for streaming at 720p 60fps.(2200Kbps~6000Kbps)
#    - https://support.google.com/youtube/answer/2853702?hl=en#zippy=%2Cp-fps%2Cp
#   the calculation would be: ((2250+6000)*1024/2) / ((64+2048)*8/2)
#
#   For emergency group, the value is preset to an average of 64Kbps.
NET_QoS_RND_REQ_NUM_TIME_SCALE = 1  # seconds
NET_QoS_RND_REQ_NUM = {
    QoSLevel.CRITICAL: int(round((64*1024) / ((300+1100)*8/2))),
    QoSLevel.GENERAL: int(round((500*1024) / ((64+2048)*8/2)))
}
# . maximum number of members that belongs to the same social group of QoS level.
NET_QoS_SG_MAX_MEMBER = {
    QoSLevel.CRITICAL: 0,
    QoSLevel.GENERAL: 20,
}


# Base Station Settings
# . base station's total bandwidth
BS_TOTAL_BAND = {
    BaseStationType.UMA: 10000000,
    BaseStationType.UMI:  5000000
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
BS_UMI_CP_QoS = {
    QoSLevel.CRITICAL: 2.34,
    QoSLevel.GENERAL: 4.69
}
# . uma base station's resource block bandwidth
BS_UMA_RB_BW = 1 * NET_RB_BW_UNIT
# . umi base station's resource block bandwidth
BS_UMI_RB_BW_QoS = {
    QoSLevel.CRITICAL: 2 * NET_RB_BW_UNIT,
    QoSLevel.GENERAL: 1 * NET_RB_BW_UNIT
}


# Vehicle Settings
# . vehicle base station subscribe move distance
VEH_MOVE_BS_CHECK = 1  # meters
# . the vehicle height
VEH_HEIGHT = 1.5  # meters

# Sumo Simulation Event Settings
EVENT_CONFIGS = [
    SumoSimEventConf(0, 2),
]
EVENT_MAX_SECONDS = max(map(lambda x: (x.dur_sec + x.ofs_sec), EVENT_CONFIGS))

# Timing Settings
# . total sumo simulation seconds (network warmup + event + inspect duration.)
SUMO_SIM_SECONDS = (
    SUMO_NET_WARMUP_SECONDS +
    EVENT_MAX_SECONDS +
    NET_TIMEOUT_SECONDS
)
SUMO_SIM_STEPS = int(round((1 / SUMO_SECONDS_PER_STEP) * SUMO_SIM_SECONDS))
# . total sumo seconds
SUMO_TOTAL_SECONDS = SUMO_SKIP_SECONDS + SUMO_SIM_SECONDS
SUMO_TOTAL_STEPS = SUMO_SKIP_STEPS + SUMO_SIM_STEPS


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

# Directory Settings
ROOT_DIR = "data/Tval/"

# Resource Allocation Parameters
ALLOC_TVAL_CONST = 1000
