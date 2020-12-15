# Custom
from od.social import SocialGroup
from od.config import SUMO_SECONDS_PER_STEP, NET_SECONDS_PER_STEP, NET_SECONDS_PER_TS
from od.misc.interest import InterestConfig
import od.vars as GV
# STD
import math
import pickle
import os


class AppdataStatistic:
    def __init__(self):
        self.time_veh_recv = {}
        self.time_bs_txq_enter = [0 for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_txq_exit = [0 for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_tx_beg = [0 for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_tx_end = [0 for _ in GV.NET_STATION_CONTROLLER]


class StatisticRecorder:
    def __init__(self, interest_config: InterestConfig):
        self.interest_config = interest_config
        self.sg_header = [{} for _ in SocialGroup]

    def GetAppdataRecord(self, sg, header):
        self.CreateIfAbsent(sg, header)
        return self.sg_header[sg][header]

    def CreateIfAbsent(self, sg, header):
        if(header not in self.sg_header[sg]):
            self.sg_header[sg][header] = AppdataStatistic()

    def VehicleReceivedIntactAppdata(self, sg, header, vehicle):
        record = self.GetAppdataRecord(sg, header)
        record.time_veh_recv[vehicle] = GV.SUMO_SIM_INFO.getTime()

    def BaseStationAppdataEnterTXQ(self, sg, bs, header):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_txq_enter[bs] = (
            # if  the appdata entered the txq at current time slot
            # then the appdata should account the waiting time in txq
            # start from the beginning of the next subframe(net step)
            GV.SUMO_SIM_INFO.getTimeNS() + NET_SECONDS_PER_STEP
        )

    def BaseStationAppdataExitTXQ(self, sg, bs, header):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_txq_exit[bs] = (
            GV.SUMO_SIM_INFO.getTimeNS()
        )

    def BaseStationAppdataStartTX(self, sg, bs, header, start_ts):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_tx_beg[bs] = (
            GV.SUMO_SIM_INFO.getTime() + start_ts * NET_SECONDS_PER_TS
        )

    def BaseStationAppdataEndTX(self, sg, bs, header, end_ts):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_tx_end[bs] = (
            GV.SUMO_SIM_INFO.getTime() + end_ts * NET_SECONDS_PER_TS
        )

    def VehicleReceivedIntactAppdataReport(self):
        sg_stats = {}
        GV.STATISTIC.Log("=====VehicleReceivedIntactAppdataReport=====")
        for sg in SocialGroup:
            sg_total_trip_time = 0
            sg_total_trip_count = 0
            sg_max_trip_time = float('-inf')
            sg_min_trip_time = float('inf')
            sg_avg_trip_time = 0
            for header, record in self.sg_header[sg].items():
                record_total_trip_time = 0
                record_total_trip_count = 0
                record_max_trip_time = float('-inf')
                record_min_trip_time = float('inf')
                for recv_time in record.time_veh_recv.values():
                    trip_time = recv_time - header.at
                    record_total_trip_time += trip_time
                    record_total_trip_count += 1
                    record_max_trip_time = record_max_trip_time if record_max_trip_time > trip_time else trip_time
                    record_min_trip_time = record_min_trip_time if record_min_trip_time < trip_time else trip_time
                record_avg_trip_time = (
                    0 if record_total_trip_count == 0
                    else record_total_trip_time / record_total_trip_count
                )
                GV.STATISTIC.Log(
                    '[{}][{}]:{{ sum:{:.2f}s, num:{:.2f}, avg:{:.2f}s, max:{:.2f}s, min:{:.2f}s}}'.format(
                        str(sg),
                        header.id,
                        record_total_trip_time,
                        record_total_trip_count,
                        record_avg_trip_time,
                        record_max_trip_time,
                        record_min_trip_time,
                    )
                )
                sg_total_trip_time += record_total_trip_time
                sg_total_trip_count += record_total_trip_count
                sg_min_trip_time = sg_min_trip_time if sg_min_trip_time < record_min_trip_time else record_min_trip_time
                sg_max_trip_time = sg_max_trip_time if sg_max_trip_time > record_max_trip_time else record_max_trip_time

            sg_avg_trip_time = (
                0 if sg_total_trip_count == 0
                else sg_total_trip_time / sg_total_trip_count
            )
            print("====={}=====".format(sg))
            print("Average Trip Time: {}s".format(sg_avg_trip_time))
            print("Maximum Trip Time: {}s".format(sg_max_trip_time))
            print("Minimum Trip Time: {}s".format(sg_min_trip_time))
            sg_stats[sg] = {
                "avg": sg_avg_trip_time,
                "max": sg_max_trip_time,
                "min": sg_min_trip_time,
            }
        return sg_stats

    def BaseStationAppdataTXQReport(self):
        sg_stats = {}
        GV.STATISTIC.Log("=====BaseStationAppdataTXQReport=====")
        # time waited of appdata in transmit queue
        for sg in SocialGroup:
            sg_max_txq_wait_time = float('-inf')
            sg_min_txq_wait_time = float('inf')
            sg_total_txq_wait_time = 0
            sg_total_txq_wait_count = 0
            sg_avg_txq_wait_time = 0
            for header, record in self.sg_header[sg].items():
                # the time for this appdata to wait in the transmit queues
                record_max_txq_wait_time = float('-inf')
                record_min_txq_wait_time = float('inf')
                record_total_txq_wait_time = 0
                record_total_txq_wait_count = 0
                # evaluate record
                for bs in GV.NET_STATION_CONTROLLER:
                    serial = bs.serial
                    time_enter = record.time_bs_txq_enter[serial]
                    time_exit = record.time_bs_txq_exit[serial]
                    if(time_enter * time_exit > 0):
                        # only estimate appdata that have waited in a tx queue
                        if(math.isclose(time_enter, time_exit)):
                            continue
                        txq_wait_time = time_exit - time_enter
                        record_total_txq_wait_count += 1
                        record_total_txq_wait_time += txq_wait_time
                        record_max_txq_wait_time = record_max_txq_wait_time if record_max_txq_wait_time > txq_wait_time else txq_wait_time
                        record_min_txq_wait_time = record_min_txq_wait_time if record_min_txq_wait_time < txq_wait_time else txq_wait_time
                # record summery
                record_avg_txq_wait_time = (
                    0 if record_total_txq_wait_count == 0
                    else record_total_txq_wait_time/record_total_txq_wait_count
                )
                GV.STATISTIC.Log(
                    '[{}][{}]:{{ sum:{:.2f}s, num:{:.2f}, avg:{:.2f}s, max:{:.2f}s, min:{:.2f}s}}'.format(
                        str(sg),
                        header.id,
                        record_total_txq_wait_time,
                        record_total_txq_wait_count,
                        record_avg_txq_wait_time,
                        record_max_txq_wait_time,
                        record_min_txq_wait_time,
                    )
                )
                # accumulate record
                sg_total_txq_wait_time += record_total_txq_wait_time
                sg_total_txq_wait_count += record_total_txq_wait_count
                sg_max_txq_wait_time = sg_max_txq_wait_time if sg_max_txq_wait_time > record_max_txq_wait_time else record_max_txq_wait_time
                sg_min_txq_wait_time = sg_min_txq_wait_time if sg_min_txq_wait_time < record_min_txq_wait_time else record_min_txq_wait_time
            # simulation summery
            sg_avg_txq_wait_time = (
                0 if sg_total_txq_wait_count == 0
                else sg_total_txq_wait_time / sg_total_txq_wait_count
            )
            print("====={}=====".format(sg))
            print("Average TXQ Time:{}s".format(sg_avg_txq_wait_time))
            print("Maximum TXQ Time:{}s".format(sg_max_txq_wait_time))
            print("Minimum TXQ Time:{}s".format(sg_min_txq_wait_time))
            sg_stats[sg] = {
                "avg": sg_avg_txq_wait_time,
                "max": sg_max_txq_wait_time,
                "min": sg_min_txq_wait_time,
            }
        return sg_stats

    def BaseStationAppdataTXReport(self):
        sg_stats = {}
        GV.STATISTIC.Log("=====BaseStationAppdataTXReport=====")
        for sg in SocialGroup:
            sg_max_tx_time = float('-inf')
            sg_min_tx_time = float('inf')
            sg_total_tx_time = 0
            sg_total_tx_count = 0
            sg_avg_tx_time = 0
            for header, record in self.sg_header[sg].items():
                # the time for this appdata delivered by all base stations.
                record_max_tx_time = float('-inf')
                record_min_tx_time = float('inf')
                record_total_tx_time = 0
                record_total_tx_count = 0
                # evaluate record
                for bs in GV.NET_STATION_CONTROLLER:
                    serial = bs.serial
                    time_begin = record.time_bs_tx_beg[serial]
                    time_end = record.time_bs_tx_end[serial]
                    if(time_begin * time_end > 0):
                        tx_time = time_end - time_begin
                        record_total_tx_count += 1
                        record_total_tx_time += tx_time
                        record_max_tx_time = record_max_tx_time if record_max_tx_time > tx_time else tx_time
                        record_min_tx_time = record_min_tx_time if record_min_tx_time < tx_time else tx_time
                # record summery
                record_avg_tx_time = (
                    0 if record_total_tx_count == 0
                    else record_total_tx_time / record_total_tx_count
                )
                GV.STATISTIC.Log(
                    '[{}][{}]:{{ sum:{:.2f}s, num:{:.2f}, avg:{:.2f}s, max:{:.2f}s, min:{:.2f}s}}'.format(
                        str(sg),
                        header.id,
                        record_total_tx_time,
                        record_total_tx_count,
                        record_avg_tx_time,
                        record_max_tx_time,
                        record_min_tx_time,
                    )
                )
                # accumulate record
                sg_total_tx_time += record_total_tx_time
                sg_total_tx_count += record_total_tx_count
                sg_max_tx_time = sg_max_tx_time if sg_max_tx_time > record_max_tx_time else record_max_tx_time
                sg_min_tx_time = sg_min_tx_time if sg_min_tx_time < record_min_tx_time else record_min_tx_time
            # simulation summery
            sg_avg_tx_time = (
                0 if sg_total_tx_count == 0
                else sg_total_tx_time / sg_total_tx_count
            )
            print("====={}=====".format(sg))
            print("Average TX Time:{}s".format(sg_avg_tx_time))
            print("Maximum TX Time:{}s".format(sg_max_tx_time))
            print("Minimum TX Time:{}s".format(sg_min_tx_time))
            sg_stats[sg] = {
                "avg": sg_avg_tx_time,
                "max": sg_max_tx_time,
                "min": sg_min_tx_time,
            }
        return sg_stats

    def Report(self, save=True):
        statistic_object = {
            "interest_config": self.interest_config,
            "veh_recv_intact_appdata_trip": self.VehicleReceivedIntactAppdataReport(),
            "bs_appdata_txq_wait": self.BaseStationAppdataTXQReport(),
            "bs_appdata_tx": self.BaseStationAppdataTXReport()
        }
        # save the statistic to file for further estimation
        if save:
            dirpath = "stats/"
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
            filename = '{}.dict'.format(str(self.interest_config))
            with open(dirpath + filename, 'wb') as interest_statistic_file:
                pickle.dump(statistic_object, interest_statistic_file)
        # return statistic object
        return statistic_object
