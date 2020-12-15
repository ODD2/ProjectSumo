import pickle
from od.social import SocialGroup
statistic = None
with open("stats/res_alloc_type(NOMA_OPT) req_rsu(True) appdata_poisson(5).object", "rb") as file:
    statistic = pickle.load(file)

maxi = float("-inf")
mini = float("inf")
for header, record in statistic.sg_header[SocialGroup.GENERAL].items():
    for i in range(3):
        if(record.time_bs_tx_end[i] * record.time_bs_tx_beg[i] > 0):
            time = record.time_bs_tx_end[i] - record.time_bs_tx_beg[i]
            if time > maxi:
                maxi = time
            if time < mini:
                mini = time
            if time > 4:
                pass

minii = float("inf")
minii_header = None
for header, record in statistic.sg_header[SocialGroup.CRITICAL].items():
    for recv_time in record.time_veh_recv.values():
        trip_time = recv_time - header.at
        if(trip_time < minii):
            minii = trip_time
            minii_header = header


a = 0
