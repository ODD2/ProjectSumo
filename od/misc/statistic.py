# Custom
from od.social import SocialGroup
from od.config import (SUMO_SECONDS_PER_STEP, NET_SECONDS_PER_STEP,
                       NET_SECONDS_PER_TS, SUMO_TOTAL_SECONDS, SUMO_SIM_SECONDS)
from od.network.types import BaseStationType
from od.misc.interest import InterestConfig
from od.network.appdata import AppDataHeader
import od.vars as GV
# STD
import math
import pickle
import os


class AppdataStatistic:
    def __init__(self, header: AppDataHeader):
        self.bits = header.total_bits
        self.at = header.at
        self.time_veh_trip = {}
        self.time_bs_txq = [[] for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_tx = [[] for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_serv = [-1 for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_drop = [-1 for _ in GV.NET_STATION_CONTROLLER]


class StatisticRecorder:
    def __init__(self, dirpath, interest_config: InterestConfig):
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        self.dirpath = dirpath
        self.interest_config = interest_config
        self.sg_header = [{} for _ in SocialGroup]

    def GetAppdataRecord(self, sg, header):
        self.CreateIfAbsent(sg, header)
        return self.sg_header[sg][header.id]

    def CreateIfAbsent(self, sg, header):
        if(header.id not in self.sg_header[sg]):
            self.sg_header[sg][header.id] = AppdataStatistic(header)

    def VehicleReceivedIntactAppdata(self, sg, vehicle, header):
        record = self.GetAppdataRecord(sg, header)
        record.time_veh_trip[vehicle.name] = (
            GV.SUMO_SIM_INFO.getTime() - header.at
        )

    # call by BaseStation while a appdata returns to TX queue
    def BaseStationAppdataEnterTXQ(self, sg, bs, headers):
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_txq[bs].append(
                [GV.SUMO_SIM_INFO.getTime(), 0]
            )

    # call by BaseStation while a appdata exits TX queue
    def BaseStationAppdataExitTXQ(self, sg, bs, headers):
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_txq[bs][-1][1] = GV.SUMO_SIM_INFO.getTime()

    # call by BaseStation while a appdata start TX
    def BaseStationAppdataStartTX(self, sg, bs, headers):
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_tx[bs].append(
                [GV.SUMO_SIM_INFO.getTime(), 0]
            )

    # call by BaseStation while a appdata end TX
    def BaseStationAppdataEndTX(self, sg, bs, headers):
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_tx[bs][-1][1] = GV.SUMO_SIM_INFO.getTime()

    # call by BaseStation while dropping a appdata
    def BaseStationAppdataDrop(self, sg, bs, headers):
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_drop[bs] = GV.SUMO_SIM_INFO.getTime()

    # call by BaseStation when appdata totally served
    def BaseStationAppdataServe(self, sg, bs, headers):
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_serv[bs] = GV.SUMO_SIM_INFO.getTime()

    def VehicleReceivedIntactAppdataReport(self):
        sg_stats = {}
        GV.STATISTIC.Doc("=====VehicleReceivedIntactAppdataReport=====")
        for sg in SocialGroup:
            sg_total_trip_time = 0
            sg_total_trip_count = 0
            sg_max_trip_time = float('-inf')
            sg_min_trip_time = float('inf')
            sg_avg_trip_time = 0
            for header_id, record in self.sg_header[sg].items():
                record_total_trip_time = 0
                record_total_trip_count = 0
                record_max_trip_time = float('-inf')
                record_min_trip_time = float('inf')
                for trip_time in record.time_veh_trip.values():
                    record_total_trip_time += trip_time
                    record_total_trip_count += 1
                    record_max_trip_time = record_max_trip_time if record_max_trip_time > trip_time else trip_time
                    record_min_trip_time = record_min_trip_time if record_min_trip_time < trip_time else trip_time
                record_avg_trip_time = (
                    0 if record_total_trip_count == 0
                    else record_total_trip_time / record_total_trip_count
                )
                GV.STATISTIC.Doc(
                    '[{}][{}]:{{ sum:{:.4f}s, num:{:.0f}, avg:{:.4f}s, max:{:.4f}s, min:{:.4f}s}}'.format(
                        str(sg),
                        header_id,
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
            GV.RESULT.Doc("====={}=====".format(sg))
            GV.RESULT.Doc("Average Trip Time: {:.4f}".format(sg_avg_trip_time))
            GV.RESULT.Doc("Maximum Trip Time: {:.4f}".format(sg_max_trip_time))
            GV.RESULT.Doc("Minimum Trip Time: {:.4f}".format(sg_min_trip_time))
            sg_stats[sg] = {
                "avg": sg_avg_trip_time,
                "max": sg_max_trip_time,
                "min": sg_min_trip_time,
            }
        return sg_stats

    def BaseStationAppdataTXQReport(self):
        sg_stats = {}
        GV.STATISTIC.Doc("=====BaseStationAppdataTXQReport=====")
        # time waited of appdata in transmit queue
        for sg in SocialGroup:
            sg_max_txq_wait_time = float('-inf')
            sg_min_txq_wait_time = float('inf')
            sg_total_txq_wait_time = 0
            sg_total_txq_wait_count = 0
            sg_avg_txq_wait_time = 0
            for header_id, record in self.sg_header[sg].items():
                # the time for this appdata to wait in the transmit queues
                record_max_txq_wait_time = float('-inf')
                record_min_txq_wait_time = float('inf')
                record_total_txq_wait_time = 0
                record_total_txq_wait_count = 0
                # evaluate record
                for bs in GV.NET_STATION_CONTROLLER:
                    serial = bs.serial
                    bs_total_txq_wait_time = 0
                    # sum up total base station txq wait time.
                    for time_interval in record.time_bs_txq[serial]:
                        time_enter = time_interval[0]
                        time_exit = time_interval[1]
                        # Error detection
                        if(time_enter == 0 or time_exit == 0):
                            print(
                                "Error! TXQ time unexpected. {}".format(
                                    record.time_bs_txq[serial])
                            )
                        # accumulate time.
                        if(not math.isclose(time_enter, time_exit) and time_enter * time_exit > 0):
                            bs_total_txq_wait_time += (time_exit - time_enter)
                    # ignore if there's no waiting time.
                    if bs_total_txq_wait_time == 0:
                        continue
                    # add txq wait time to record.
                    record_total_txq_wait_count += 1
                    record_total_txq_wait_time += bs_total_txq_wait_time
                    record_max_txq_wait_time = (
                        record_max_txq_wait_time
                        if record_max_txq_wait_time > bs_total_txq_wait_time
                        else bs_total_txq_wait_time
                    )
                    record_min_txq_wait_time = (
                        record_min_txq_wait_time
                        if record_min_txq_wait_time < bs_total_txq_wait_time
                        else bs_total_txq_wait_time
                    )
                # record summery
                record_avg_txq_wait_time = (
                    0 if record_total_txq_wait_count == 0
                    else record_total_txq_wait_time/record_total_txq_wait_count
                )
                GV.STATISTIC.Doc(
                    '[{}][{}]:{{ sum:{:.4f}s, num:{:.0f}, avg:{:.4f}s, max:{:.4f}s, min:{:.4f}s}}'.format(
                        str(sg),
                        header_id,
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
            # simulation summary
            sg_avg_txq_wait_time = (
                0 if sg_total_txq_wait_count == 0
                else sg_total_txq_wait_time / sg_total_txq_wait_count
            )
            GV.RESULT.Doc("====={}=====".format(sg))
            GV.RESULT.Doc("Average TXQ Time:{:.4f}".format(
                sg_avg_txq_wait_time))
            GV.RESULT.Doc("Maximum TXQ Time:{:.4f}".format(
                sg_max_txq_wait_time))
            GV.RESULT.Doc("Minimum TXQ Time:{:.4f}".format(
                sg_min_txq_wait_time))
            sg_stats[sg] = {
                "avg": sg_avg_txq_wait_time,
                "max": sg_max_txq_wait_time,
                "min": sg_min_txq_wait_time,
            }
        return sg_stats

    def BaseStationAppdataTXReport(self):
        sg_stats = {}
        GV.STATISTIC.Doc("=====BaseStationAppdataTXReport=====")
        for sg in SocialGroup:
            sg_max_tx_time = float('-inf')
            sg_min_tx_time = float('inf')
            sg_total_tx_time = 0
            sg_total_tx_count = 0
            sg_avg_tx_time = 0
            for header_id, record in self.sg_header[sg].items():
                # the time for this appdata to deliver by all base stations.
                record_max_tx_time = float('-inf')
                record_min_tx_time = float('inf')
                record_total_tx_time = 0
                record_total_tx_count = 0
                # evaluate record
                for bs in GV.NET_STATION_CONTROLLER:
                    serial = bs.serial
                    bs_total_tx_time = 0
                    # ignore if base station never transmit this appdata.
                    # or if base station did not seccessfully transmit the appdata.
                    if(record.time_bs_drop[serial] > 0 or
                       record.time_bs_serv[serial] < 0):
                        continue
                    # sum up all the base station tx time
                    for time_pair in record.time_bs_tx[serial]:
                        time_begin = time_pair[0]
                        time_end = time_pair[1]
                        if(time_begin * time_end > 0):
                            # ignore trivial values
                            if(math.isclose(time_begin, time_end)):
                                continue
                            bs_total_tx_time += time_end - time_begin
                    # add tx time to record
                    record_total_tx_count += 1
                    record_total_tx_time += bs_total_tx_time
                    record_max_tx_time = (
                        record_max_tx_time
                        if record_max_tx_time > bs_total_tx_time
                        else bs_total_tx_time
                    )
                    record_min_tx_time = (
                        record_min_tx_time
                        if record_min_tx_time < bs_total_tx_time
                        else bs_total_tx_time
                    )
                # record summery
                record_avg_tx_time = (
                    0 if record_total_tx_count == 0
                    else record_total_tx_time / record_total_tx_count
                )
                GV.STATISTIC.Doc(
                    '[{}][{}]:{{ sum:{:.4f}s, num:{:.0f}, avg:{:.4f}s, max:{:.4f}s, min:{:.4f}s}}'.format(
                        str(sg),
                        header_id,
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
            GV.RESULT.Doc("====={}=====".format(sg))
            GV.RESULT.Doc("Average TX Time:{:.4f}".format(sg_avg_tx_time))
            GV.RESULT.Doc("Maximum TX Time:{:.4f}".format(sg_max_tx_time))
            GV.RESULT.Doc("Minimum TX Time:{:.4f}".format(sg_min_tx_time))
            sg_stats[sg] = {
                "avg": sg_avg_tx_time,
                "max": sg_max_tx_time,
                "min": sg_min_tx_time,
            }
        return sg_stats

    def BaseStationThroughPutReport(self):
        # pass
        sg_stats = {}
        bs_bits = [0 for _ in GV.NET_STATION_CONTROLLER]
        for sg in SocialGroup:
            for record in self.sg_header[sg].values():
                for bs in GV.NET_STATION_CONTROLLER:
                    if(record.time_bs_serv[bs] > 0):
                        bs_bits[bs] += record.bits
        for bs_type in BaseStationType:
            bs_type_num = 0
            bs_type_bits = 0
            for bs in [x for x in GV.NET_STATION_CONTROLLER if x.type == bs_type]:
                bs_type_bits += bs_bits[bs]
                bs_type_num += 1
            bs_type_through_put_avg = (
                (bs_type_bits / max(bs_type_num, 1))
            )
            GV.RESULT.Doc("====={}=====".format(bs_type.name))
            GV.RESULT.Doc(
                "Throughput:{:.2f}/s".format(bs_type_through_put_avg)
            )
            sg_stats[bs_type] = bs_type_through_put_avg
        return sg_stats

    def SystemThroughPutReport(self):
        total_bits = 0
        for sg in SocialGroup:
            for record in self.sg_header[sg].values():
                for bs in GV.NET_STATION_CONTROLLER:
                    if(record.time_bs_serv[bs] > 0):
                        total_bits += record.bits
        return total_bits

    def BaseStationSocialGroupResourceUsageReport(self):
        sg_stats = {}
        sg_bs_type_data = [[0 for _ in SocialGroup]
                           for _ in BaseStationType]
        for sg in SocialGroup:
            for record in self.sg_header[sg].values():
                for bs in GV.NET_STATION_CONTROLLER:
                    if(record.time_bs_serv[bs] > 0):
                        sg_bs_type_data[bs.type][sg] += 1

        for bs_type in BaseStationType:
            bs_type_total_data = max(sum(sg_bs_type_data[bs_type]), 1)
            bs_type_sg_res_rate = [0 for _ in SocialGroup]
            GV.RESULT.Doc("====={}=====".format(bs_type.name))
            for sg in SocialGroup:
                bs_type_sg_res_rate[sg] = (
                    sg_bs_type_data[bs_type][sg]/bs_type_total_data
                )
                GV.RESULT.Doc(
                    "{} Resource Usage: {:.2f}%".format(
                        sg,
                        bs_type_sg_res_rate[sg]*100
                    )
                )
            sg_stats[bs_type] = bs_type_sg_res_rate
        return sg_stats

    def BaseStationSocailGroupDataDropRateReport(self):
        sg_stats = {}
        sg_bs_type_recv = [[0 for _ in SocialGroup]
                           for _ in BaseStationType]
        sg_bs_type_drop = [[0 for _ in SocialGroup]
                           for _ in BaseStationType]
        GV.STATISTIC.Doc("=====BaseStationSocailGroupDataDropRateReport=====")
        for sg in SocialGroup:
            for record in self.sg_header[sg].values():
                for bs in GV.NET_STATION_CONTROLLER:
                    if(len(record.time_bs_txq[bs]) > 0):
                        sg_bs_type_recv[bs.type][sg] += 1
                    if(record.time_bs_drop[bs] > 0):
                        sg_bs_type_drop[bs.type][sg] += 1

        for bs_type in BaseStationType:
            GV.RESULT.Doc("====={}=====".format(bs_type.name))
            bs_type_sg_drop_rate = [0 for _ in SocialGroup]
            for sg in SocialGroup:
                bs_type_sg_drop_rate[sg] = (
                    sg_bs_type_drop[bs_type][sg] /
                    max(sg_bs_type_recv[bs_type][sg], 1)
                )
                GV.RESULT.Doc(
                    "{} Drop Rate: {:.2f}%".format(
                        sg,
                        bs_type_sg_drop_rate[sg]*100
                    )
                )
            sg_stats[bs_type] = bs_type_sg_drop_rate
        return sg_stats

    def Preprocess(self):
        for sg in SocialGroup:
            for record in self.sg_header[sg].values():
                for serial in GV.NET_STATION_CONTROLLER:
                    if(len(record.time_bs_txq[serial]) > 0):
                        # check if the latest enqueue time exceeds the total simulation time
                        if(record.time_bs_txq[serial][-1][0] > SUMO_TOTAL_SECONDS):
                            record.time_bs_drop[serial] = SUMO_TOTAL_SECONDS
                            record.time_bs_txq[serial][-1][0] = SUMO_TOTAL_SECONDS

                        # check if the latest dequeue time is unset
                        if(record.time_bs_txq[serial][-1][1] == 0):
                            if(record.time_bs_drop[serial] >= 0):
                                # if it's unset because it had been dropped by base station
                                # the dequeue time will be the time it was dropped
                                record.time_bs_txq[serial][-1][1] = record.time_bs_drop[serial]
                            elif(record.time_bs_serv[serial] >= 0):
                                # if it's unset because it had been completely served
                                # no dequeue time is not required, so is the enqueue time.
                                record.time_bs_txq[serial].pop()
                            else:
                                # if it's unset because the simulation ended (not dropped also not served)
                                # set the dequeue time to the simulation end time.
                                record.time_bs_txq[serial][-1][1] = SUMO_TOTAL_SECONDS

    def Report(self, save=True):
        # preprocess the raw statistics
        self.Preprocess()
        # create report
        statistic_report = {
            "interest_config": self.interest_config,
            "veh_recv_intact_appdata_trip": self.VehicleReceivedIntactAppdataReport(),
            "bs_appdata_txq_wait": self.BaseStationAppdataTXQReport(),
            "bs_appdata_tx": self.BaseStationAppdataTXReport(),
            "bs_through_put": self.BaseStationThroughPutReport(),
            "bs_sg_res_use_rate": self.BaseStationSocialGroupResourceUsageReport(),
            "sys_through_put": self.SystemThroughPutReport(),
            # "bs_sg_data_drop_rate": self.BaseStationSocailGroupDataDropRateReport(),
        }
        # save the statistic to file for further estimation
        if save:
            if not os.path.isdir(self.dirpath):
                os.mkdir(self.dirpath)
            report_filename = 'report.pickle'
            object_filename = 'object.pickle'
            with open(self.dirpath + report_filename, 'wb') as interest_statistic_report_file:
                pickle.dump(statistic_report, interest_statistic_report_file)
            with open(self.dirpath + object_filename, 'wb') as interest_statistic_object_file:
                pickle.dump(self, interest_statistic_object_file)
        # return statistic object
        return statistic_report
