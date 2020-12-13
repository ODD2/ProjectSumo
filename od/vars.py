# Custom
from od.network.controller import NetworkCoreController
from od.network.model import NetStatusCache
from od.network.types import BaseStationType
from od.misc.siminfo import SumoSimInfo
from od.misc.logger import Logger, Printer
from od.misc.statistic import StatisticRecorder
from od.config import BS_PRESET
from od.misc.interest import InterestConfig
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


def InitializeSimulationVariables(interest_config: InterestConfig):
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
    NET_CORE_CONTROLLER = NetworkCoreController()
    NET_STATUS_CACHE = NetStatusCache()
    NET_STATION_CONTROLLER = []
    # Logger
    DEBUG = Logger(
        "Debug ({}).txt".format(
            datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        )
    )
    ERROR = Printer(
        "Error ({}).txt".format(
            datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        )
    )
    STATISTIC = Logger(
        "Statistic ({}).txt".format(
            datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        )
    )
    # Sumo Simulation Info
    SUMO_SIM_INFO = SumoSimInfo()
    # Statistsic
    STATISTIC_RECORDER = StatisticRecorder()
    # Thread
    TRACI_LOCK = Lock()
    # Base Station Setting
    BS_SETTING = {}
    for name, setting in BS_PRESET.items():
        if (setting["type"] == BaseStationType.UMA or
            (interest_config.rsu and setting["type"] == BaseStationType.UMI)):
            BS_SETTING[name] = setting
    # Downlink Resource Allocation
    NET_RES_OMA_ONLY = interest_config.oma_only
    # Application Data
    APP_DATA_POISSON = interest_config.appdata_poisson
