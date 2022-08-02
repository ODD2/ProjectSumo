from fileinput import filename
import os
import sys
from matplotlib.lines import Line2D
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
        "figure.figsize": [6, 4],
        "lines.linewidth": 3,
        "lines.markersize": 15
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
CB_COLOR_CYCLE = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
# CB_COLOR_CYCLE = ['r', 'b']
LINE_MARKER_STYLES = [
    {
        "marker": marker_style,
        "linestyle": (i_m, line_style),
        # "markerfacecolor": 'w',
        "markeredgewidth": 1.5,
        "fillstyle": "none",
        "alpha": 0.8,
    }
    # for line_style in ['--', '-.', ':']
    # for marker_style in ['o', 'v', '^', '$*$', '$o$', "$x$", "$+$"]
    # for line_style in [(0, (1, 6)), (2, (1, 6)), (4, (1, 6))]
    for line_style in [(1, 5), (3, 5, 1, 5), (5, 5), (3, 1, 1, 1)]
    for i_m, marker_style in enumerate(['o', 'v', '^', "s", "*", ])
]
random.seed(1)
# random.shuffle(LINE_MARKER_STYLES)
random.shuffle(CB_COLOR_CYCLE)


# ================ Line Style ===================
line_no = -1
line_style_repo = {}


def GetLineMarkerStyle(name):
    if(name not in line_style_repo):
        line_style_repo[name] = GetNewLineMarkerStyle()
    return line_style_repo[name]


def GetNewLineMarkerStyle():
    global line_no
    line_no += 1
    return {
        **LINE_MARKER_STYLES[line_no % len(LINE_MARKER_STYLES)],
        "color": CB_COLOR_CYCLE[line_no % len(CB_COLOR_CYCLE)]
    }


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
        return "Optim"
    elif(alloc_type == ResourceAllocatorType.NOMA_APR):
        return "Approx"


def ScenarioDynamicSGName(dyn_sg_behav):
    if(dyn_sg_behav == DynamicSocialGroupBehaviour.MAX_N_GROUPS):
        return "$\Delta_{Groups}$"
    elif(dyn_sg_behav == DynamicSocialGroupBehaviour.MAX_N_MEMBER):
        return "$\Delta_{Member}$"
    else:
        return "Unknown"


def ScenarioPrefix(req_rsu, qos_re_class):
    if not req_rsu:
        return "MC"
    elif not qos_re_class:
        return "SA"
    return "QR"


def GetScenarioBaseStationNames(req_rsu):
    return YRSU_SCENARIO_BS_ID if req_rsu else NRSU_SCENARIO_BS_ID


def ScenarioSINRState(sinr_stat):
    return "P" if sinr_stat else "NP"


def ScenarioNetFlowType(qos_re_class):
    return [NetFlowType.CRITICAL, NetFlowType.GENERAL]
    # if(qos_re_class):
    #     return NetFlowType
    # else:
    #     return [NetFlowType.CRITICAL, NetFlowType.GENERAL]


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
    def __init__(self, title, xlabel, ylabel, yscale_opts={"value": "linear"}, save_as=None, ncols=3):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.lines = []
        self.yscale_opts = yscale_opts
        self.ncols = ncols
        self.y_lim = None
        self.save_as = save_as if save_as else title

    def addLine(self, line: Line):
        self.lines.append(line)

    def SetYScale(self, y_lim):
        self.y_lim = y_lim


def ShowGraphs(graphs, save, category="general", legend_size=4):
    line_set = set()
    for _g, (title, graph) in enumerate(graphs.items()):
        plt.figure(_g, figsize=(11, 8))
        plt.title(graph.title)
        plt.xlabel(graph.xlabel)
        plt.ylabel(graph.ylabel)
        plt.yscale(**(graph.yscale_opts))
        plt.gca().xaxis.set_major_locator(MaxNLocator(5, min_n_ticks=3))
        if(graph.y_lim != None):
            plt.gca().set_ylim(graph.y_lim)
        for _l, line in enumerate(graph.lines):
            plt.plot(
                line.x,
                line.y,
                **GetLineMarkerStyle(line.label),
                label=line.label
            )
        # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=graph.ncols)
        if save:
            plt.savefig('{}/{}.pdf'.format(dirpath, graph.save_as), bbox_inches="tight")
    plt.figure("Legends")
    lines = [
        Line2D(
            [], [], **line_style_repo[label], label=label
        )
        for label in sorted(line_style_repo.keys())
    ]
    plt.gcf().legend(
        handles=lines,
        loc="center",
        ncol=legend_size
    )
    plt.gcf().savefig('{}/{}_legends.pdf'.format(dirpath, category), bbox_inches="tight")
