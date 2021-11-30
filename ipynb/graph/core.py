import os
import sys
import matplotlib.pyplot as plt
import pickle
import math
import random
import numpy as np
from numpy import random
# ============== Enter Project Directory ================
# enter project directory
while(not os.getcwd() == "/"):
    if(".gitignore" in os.listdir()):
        break
    else:
        os.chdir("../")
else:
    exit(-1)
sys.path.append(os.getcwd())
# ============== Custom Module Import ===================
from od.env.config import ROOT_DIR
from od.env.station import BS_PRESET
from od.network.types import ResourceAllocatorType, BaseStationType
from od.misc.interest import InterestConfig
from od.misc.statistic import NetFlowType
from od.social.manager.types import DynamicSocialGroupBehaviour
# ============== Create Picture Folder ===================
dirpath = "pics/"
if not os.path.isdir(dirpath):
    os.mkdir(dirpath)
# ============== PLT Configuration ================
plt.rcParams.update(
    {
        "text.usetex": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica"],
        "legend.loc": "upper left",
        "legend.framealpha": 0.3,
        "font.size": 26,
        "figure.autolayout": True,
        "figure.dpi": 100,
        "axes.titlesize": "medium",
        "legend.fontsize": "x-small",
        'figure.figsize': [6, 4],

    }
)
PINF = float("inf")
NINF = float("-inf")


# ============== Basestation ID ================
YRSU_SCENARIO_BS_ID = []
NRSU_SCENARIO_BS_ID = []

for name, bs_config in BS_PRESET.items():
    if (bs_config["type"] == BaseStationType.UMA):
        YRSU_SCENARIO_BS_ID.append(name)
        NRSU_SCENARIO_BS_ID.append(name)
    if (bs_config["type"] == BaseStationType.UMI):
        YRSU_SCENARIO_BS_ID.append(name)

# ============== LINE MARKER ================

LINE_MARKER_STYLES = [
    marker_style + line_style
    for marker_style in ['o', 'v', '^', '<', '>', '*', 'x', 'd']
    for line_style in ['--', '-.', ':']
]
random.seed(1)
random.shuffle(LINE_MARKER_STYLES)


def GetLineMarkerStyle(line_no):
    return LINE_MARKER_STYLES[line_no % len(LINE_MARKER_STYLES)]


# ============== Helper Functions ================
def ExtractAbbreviations(abbrev):
    if(abbrev.lower() == "avg"):
        return "Average"
    elif(abbrev.lower() == "max"):
        return "Maximum"
    elif(abbrev.lower() == "min"):
        return "Minimum"


def BaseStationScenario(with_rsu):
    if(with_rsu):
        return "4G+5G"
    else:
        return "4G"


def ScenarioAllocName(alloc_type):
    if(alloc_type == ResourceAllocatorType.OMA):
        return "OMA"
    elif(alloc_type == ResourceAllocatorType.NOMA_OPT):
        return "NOMA-Optim"
    elif(alloc_type == ResourceAllocatorType.NOMA_APR):
        return "NOMA-Approx"


def ScenarioPrefix(req_rsu, qos_re_class):
    if not req_rsu:
        return "MC"
    elif not qos_re_class:
        return "SA"
    return "QR"


def GetScenarioBaseStationNames(req_rsu):
    return YRSU_SCENARIO_BS_ID if req_rsu else NRSU_SCENARIO_BS_ID


def ScenarioNetFlowType(qos_re_class):
    if(qos_re_class):
        return NetFlowType
    else:
        return [NetFlowType.CRITICAL, NetFlowType.GENERAL]


def ScenarioQoSReClassRange(req_rsu):
    if(req_rsu):
        return [True, False]
    else:
        return [False]


# ============== GRAPH COMPONENTS =============
from matplotlib.ticker import MaxNLocator


class Line:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class Graph:
    def __init__(self, title, xlabel, ylabel, yscale_opts={"value": "linear"}, ncols=3):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.lines = []
        self.yscale_opts = yscale_opts
        self.ncols = ncols

    def addLine(self, line: Line):
        self.lines.append(line)


def ShowGraphs(graphs, save):
    for _g, (title, graph) in enumerate(graphs.items()):
        plt.figure(_g, figsize=(11, 8))
        plt.title(title)
        plt.xlabel(graph.xlabel)
        plt.ylabel(graph.ylabel)
        plt.yscale(**(graph.yscale_opts))
        plt.gca().xaxis.set_major_locator(MaxNLocator(5, min_n_ticks=3))
        for _l, line in enumerate(graph.lines):
            plt.plot(
                line.x,
                line.y,
                GetLineMarkerStyle(_l),
                label=line.label
            )
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=graph.ncols)
        if save:
            plt.savefig('{}/{}.pdf'.format(dirpath, title), bbox_inches="tight")
    plt.show()
