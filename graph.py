import matplotlib.pyplot as plt
import pickle
import os
from od.social import SocialGroup
from od.network.types import ResourceAllocatorType
from od.misc.interest import InterestConfig
from numpy import random

graph_configs = [
    {
        "catalog": "veh_recv_intact_appdata_trip",
        "topic": "End-to-End Time",
        "x": "Maximum Data Generated Per Second(Unique Distribution) ",
        "y": "Time(Second)",
        "subject": ["Avg", "Max", "Min"]
    },
    {
        "catalog": "bs_appdata_txq_wait",
        "topic": "Wait Time in Downlink Queue",
        "x": "Maximum Data Generated Per Second(Unique Distribution) ",
        "y": "Time(Second)",
        "subject": ["Avg", "Max", "Min"]
    },
    {
        "catalog": "bs_appdata_tx",
        "topic": "Transfer Time",
        "x": "Maximum Data Generated Per Second(Unique Distribution) ",
        "y": "Time(Second)",
        "subject": ["Avg", "Max", "Min"]
    }
]


a = [t for t in ResourceAllocatorType]
b = [False, True]
c = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
interest_config = InterestConfig(None, False, 0)
stats = [[[None for _c in c] for _b in b] for _a in a]
for _a, res_alloc_type in enumerate(a):
    for _b, req_rsu in enumerate(b):
        for _c, appdata_poisson in enumerate(c):
            interest_config.res_alloc_type = res_alloc_type
            interest_config.req_rsu = req_rsu
            interest_config.appdata_poisson = appdata_poisson
            with open("stats/{}.dict".format(str(interest_config)), "rb") as file:
                stats[_a][_b][_c] = pickle.load(file)

# create picture folder
dirpath = "pics/"
if not os.path.isdir(dirpath):
    os.mkdir(dirpath)

# intialize
_pinf = float("inf")
_ninf = float("-inf")
serial = 1
for config in graph_configs:
    catalog = config["catalog"]
    topic = config["topic"]
    subjects = config["subject"]
    for subject in subjects:
        title = "{}({})".format(topic, subject)
        plt.figure(serial, figsize=(9, 5))
        plt.xlabel(config["x"])
        plt.ylabel(config["y"])
        plt.title(title)
        for _a in range(len(a)):
            for _b in range(len(b)):
                for sg in SocialGroup:
                    y = []
                    x = c
                    for _c in range(len(c)):
                        value = stats[_a][_b][_c][catalog][sg][subject.lower()]
                        if value == _pinf or value == _ninf:
                            value = 0
                        y.append(value)
                    plt.plot(
                        x,
                        y,
                        ".-",
                        label="{}/{}/{}".format(
                              str(sg).lower(),
                              a[_a].name.lower(),
                              "rsu" if b[_b] else ""
                        )
                    )

                    #   plt.text(
                    #     c[-1],
                    #     y[-1],
                    #   )
        plt.legend(loc='upper left', bbox_to_anchor=(0, 1))
        plt.savefig('{}/{}.png'.format(dirpath, title))
        plt.savefig('{}/{}.pdf'.format(dirpath, title))
        serial += 1
plt.show()
