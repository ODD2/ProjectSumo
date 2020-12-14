import matplotlib.pyplot as plt
import pickle
from od.social import SocialGroup
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

a = [False, True]
b = [False, True]
c = [1, 10, 25, 50]

stats = [[[None for _c in c] for _b in b] for _a in a]
for _a, oma in enumerate(a):
    for _b, rsu in enumerate(b):
        for _c, poisson in enumerate(c):
            with open("stats/oma_only({}) rsu({}) appdata_poisson({}).dict".format(oma, rsu, poisson), "rb") as file:
                stats[_a][_b][_c] = pickle.load(file)

serial = 1
for config in graph_configs:
    topic = config["name"]
    subjects = config["subject"]
    for subject in subjects:
        plt.figure(serial, figsize=(9, 3))
        plt.xlabel("Appdata poisson mean")
        plt.ylabel("time(s)")
        plt.title("{}({})".format(topic, subject))
        for _a in range(len(a)):
            for _b in range(len(b)):
                for sg in SocialGroup:
                    y = []
                    x = c
                    for _c in range(len(c)):
                        y.append(stats[_a][_b][_c][topic][sg][subject])
                    plt.plot(x, y)
                    plt.text(
                        c[-1],
                        y[-1],
                        "{}/{}/{}".format(
                            str(sg).lower(),
                            "oma" if a[_a] else "noma",
                            "rsu" if b[_b] else ""
                        )
                    )
        serial += 1
plt.show()
