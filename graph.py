import matplotlib.pyplot as plt
import pickle
import os
from od.social import SocialGroup
from od.network.types import ResourceAllocatorType
from od.misc.interest import InterestConfig
from numpy import random

graph_configs = [
    {
        "name": "veh_recv_intact_appdata_trip",
        "subject": ["avg", "max", "min"]
    },
    {
        "name": "bs_appdata_txq_wait",
        "subject": ["avg", "max", "min"]
    },
    {
        "name": "bs_appdata_tx",
        "subject": ["avg", "max", "min"]
    }
]

a = [t for t in ResourceAllocatorType]
b = [False, True]
c = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
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
    topic = config["name"]
    subjects = config["subject"]
    for subject in subjects:
        title = "{}({})".format(topic, subject)
        plt.figure(serial, figsize=(9, 5))
        plt.xlabel("data poisson mean")
        plt.ylabel("time(s)")
        plt.title(title)
        for _a in range(len(a)):
            for _b in range(len(b)):
                for sg in SocialGroup:
                    y = []
                    x = c
                    for _c in range(len(c)):
                        value = stats[_a][_b][_c][topic][sg][subject]
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
        serial += 1
plt.show()
