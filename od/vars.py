# Custom
import od.network.controller as onc
import od.network.model as onm
import od.network.types as ont
import od.misc.siminfo as oms
import od.misc.logger as oml
import od.misc.statistic as omss
import od.env.config as oec
import od.env.station as oes
import od.misc.interest as omi
import od.event.quake as oeq
# STD
from od.social.group import QoSLevel, SocialGroup
from numpy import random
from datetime import datetime
from threading import Lock


# System Parameter
INTEREST_CONFIG = None


# Network
NET_CORE_CONTROLLER = None
NET_STATUS_CACHE = None
NET_STATION_CONTROLLER = None
# - downlink resource allocation method.
NET_RES_ALLOC_TYPE = None
# - qos social group reclass selector.
NET_QoS_RE_CLS = None
# - applcation social group random request modifier.(scale by emergency events)
NET_QoS_RND_REQ_MOD = None


# Logger
DEBUG = None
ERROR = None
STATISTIC = None
RESULT = None


# Sumo Simulation
SUMO_SIM_INFO = None
SUMO_SIM_EVENTS = None


# Statistic
STATISTIC_RECORDER = None

# Thread
TRACI_LOCK = None

# Base Station
BS_SETTING = None


def InitializeSimulationVariables(interest_config: omi.InterestConfig):
    global NET_CORE_CONTROLLER, NET_STATUS_CACHE, NET_STATION_CONTROLLER
    global DEBUG, ERROR, STATISTIC, RESULT
    global INTEREST_CONFIG
    global SUMO_SIM_INFO, SUMO_SIM_EVENTS
    global STATISTIC_RECORDER
    global TRACI_LOCK
    global BS_SETTING
    global NET_RES_ALLOC_TYPE, NET_QoS_RE_CLS, NET_QoS_RND_REQ_MOD

    # Simulation Parameters
    INTEREST_CONFIG = interest_config

    # Directories
    datadir = oec.ROOT_DIR + interest_config.folder()

    # Consistant random seed for consistant random number generator
    random.seed(interest_config.rng_seed)

    # Network
    NET_CORE_CONTROLLER = onc.NetworkCoreController()
    NET_STATUS_CACHE = onm.NetStatusCache()
    NET_STATION_CONTROLLER = []
    # - Qos Re-Classification Switch
    NET_QoS_RE_CLS = interest_config.qos_re_class
    # - Downlink Resource Allocation
    NET_RES_ALLOC_TYPE = interest_config.res_alloc_type
    # modifier
    NET_QoS_RND_REQ_MOD = [1 for _ in QoSLevel]

    # Logger
    time_text = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    DEBUG = oml.Debugger(
        datadir,
        "Debug ({}).txt".format(time_text)
    )
    ERROR = oml.Logger(
        datadir,
        "Error ({}).txt".format(time_text)
    )
    STATISTIC = oml.Logger(
        datadir,
        "Statistic ({}).xml".format(time_text)
    )
    RESULT = oml.Logger(
        datadir,
        "Result ({}).txt".format(time_text)
    )

    # Sumo Simulation Info
    SUMO_SIM_INFO = oms.SumoSimInfo()
    SUMO_SIM_EVENTS = list(map(lambda x: oeq.EarthQuake(x), oec.EVENT_CONFIGS))

    # Statistsic
    STATISTIC_RECORDER = omss.StatisticRecorder(datadir, interest_config)

    # Thread
    TRACI_LOCK = Lock()

    # Base Station Setting
    BS_SETTING = {}
    for name, setting in oes.BS_PRESET.items():
        if (setting["type"] == ont.BaseStationType.UMA or
                (interest_config.req_rsu and
                 setting["type"] == ont.BaseStationType.UMI)):
            BS_SETTING[name] = setting


def TerminateSimulationVariables():
    global DEBUG, ERROR, STATISTIC, RESULT
    DEBUG.Encapsulate()
    ERROR.Encapsulate()
    STATISTIC.Encapsulate()
    RESULT.Encapsulate()
