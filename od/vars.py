# Custom
from od.network.controller import NetworkCoreController
from od.network.model import NetStatusCache
from od.misc.siminfo import SumoSimInfo
from od.misc.logger import Logger, Printer
from od.misc.statistic import StatisticRecorder
# STD
from numpy import random
from datetime import datetime
from threading import Lock


# Network
NET_CORE_CONTROLLER = None
NET_STATUS_CACHE = None
NET_STATION_CONTROLLER = None
# Logger
DEBUG = None
ERROR = None
STATISTIC = None
# Sumo
SUMO_SIM_INFO = None
# Statistic
STATISTIC_RECORDER = None
# Thread
TRACI_LOCK = None


def InitializeSimulationVariables():
    global NET_CORE_CONTROLLER, NET_STATUS_CACHE, NET_STATION_CONTROLLER
    global DEBUG, ERROR, STATISTIC
    global SUMO_SIM_INFO
    global STATISTIC_RECORDER
    global TRACI_LOCK
    #
    NET_CORE_CONTROLLER = NetworkCoreController()
    NET_STATUS_CACHE = NetStatusCache()
    NET_STATION_CONTROLLER = []
    #
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
    #
    SUMO_SIM_INFO = SumoSimInfo()
    #
    STATISTIC_RECORDER = StatisticRecorder()
    #
    TRACI_LOCK = Lock()

    # consistant random seed for consistant random number generator
    random.seed(132342421)
