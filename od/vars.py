# Custom
import od.network.controller as onc
import od.network.model as onm
import od.network.types as ont
import od.misc.siminfo as oms
import od.misc.logger as oml
import od.misc.statistic as omss
import od.config as oc
import od.misc.interest as omi
# STD
from numpy import random
from datetime import datetime
from threading import Lock


# Network
NET_CORE_CONTROLLER = None
NET_STATUS_CACHE = None
NET_STATION_CONTROLLER = None
# - downlink resource allocation method
NET_RES_OMA_ONLY = None

# Logger
DEBUG = None
ERROR = None
STATISTIC = None

# Sumo Simulation Info
SUMO_SIM_INFO = None

# Statistic
STATISTIC_RECORDER = None

# Thread
TRACI_LOCK = None

# Base Station
BS_SETTING = None

# Application Data
APP_DATA_POISSON = None


def InitializeSimulationVariables(interest_config: omi.InterestConfig):
    global NET_CORE_CONTROLLER, NET_STATUS_CACHE, NET_STATION_CONTROLLER
    global DEBUG, ERROR, STATISTIC
    global SUMO_SIM_INFO
    global STATISTIC_RECORDER
    global TRACI_LOCK
    global BS_SETTING
    global NET_RES_OMA_ONLY
    global APP_DATA_POISSON
    # consistant random seed for consistant random number generator
    random.seed(132342421)
    # Network
    NET_CORE_CONTROLLER = onc.NetworkCoreController()
    NET_STATUS_CACHE = onm.NetStatusCache()
    NET_STATION_CONTROLLER = []
    # Logger
    DEBUG = oml.Logger(
        "Debug ({}).txt".format(
            datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        )
    )
    ERROR = oml.Printer(
        "Error ({}).txt".format(
            datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        )
    )
    STATISTIC = oml.Logger(
        "Statistic ({}).txt".format(
            datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        )
    )
    # Sumo Simulation Info
    SUMO_SIM_INFO = oms.SumoSimInfo()
    # Statistsic
    STATISTIC_RECORDER = omss.StatisticRecorder()
    # Thread
    TRACI_LOCK = Lock()
    # Base Station Setting
    BS_SETTING = {}
    for name, setting in oc.BS_PRESET.items():
        if (setting["type"] == ont.BaseStationType.UMA or
                (interest_config.rsu and setting["type"] == ont.BaseStationType.UMI)):
            BS_SETTING[name] = setting
    # Downlink Resource Allocation
    NET_RES_OMA_ONLY = interest_config.oma_only
    # Application Data
    APP_DATA_POISSON = interest_config.appdata_poisson
