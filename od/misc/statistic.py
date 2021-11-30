# Custom
from od.social.group import QoSLevel, SocialGroup
from od.env.config import (SUMO_SECONDS_PER_STEP, NET_SECONDS_PER_STEP,
                           NET_SECONDS_PER_TS, SUMO_TOTAL_SECONDS, SUMO_SIM_SECONDS,
                           SUMO_SKIP_SECONDS, SUMO_NET_WARMUP_SECONDS, EVENT_CONFIGS, NET_TIMEOUT_SECONDS)
from od.network.types import BaseStationType
from od.misc.interest import InterestConfig
from od.misc.exception import ODExecption
from od.network.appdata import AppDataHeader
import od.vars as GV
# STD
from enum import IntEnum
import math
import pickle
import os


class NetFlowType(IntEnum):
    CRITICAL = 0
    GENERAL = 1
    C2G = 2
    NC2G = 3


class AppdataStatistic:
    def __init__(self, header: AppDataHeader):
        self.bits = header.total_bits
        self.at = header.at
        self.is_src_ot = False
        self.time_veh_trip = {}
        self.time_bs_txq = [[] for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_tx = [[] for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_serv = [-1 for _ in GV.NET_STATION_CONTROLLER]
        self.time_bs_drop = [-1 for _ in GV.NET_STATION_CONTROLLER]
        self.is_bs_ot = [False for _ in GV.NET_STATION_CONTROLLER]


class StatisticRecorder:
    def __init__(self, dirpath, interest_config: InterestConfig):
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        self.sys_veh_num = 0
        self.dirpath = dirpath
        self.interest_config = interest_config
        self.raw_sg_header = {}
        self.sg_header = {}
        self.social_group = []
        self.interval = (
            SUMO_SKIP_SECONDS + SUMO_NET_WARMUP_SECONDS + min(map(lambda x: x.ofs_sec, EVENT_CONFIGS)),
            SUMO_SKIP_SECONDS + SUMO_NET_WARMUP_SECONDS + max(map(lambda x: x.ofs_sec + x.dur_sec, EVENT_CONFIGS))
        )
        self.nft_traffic = {}

    # the total amount of time for the recorder in seconds.
    def RecordDuration(self):
        return self.interval[1] - self.interval[0]

    # record the amount of vehicles in the system throughout the whole simulation
    def VehiclesJoin(self, veh_num):
        self.sys_veh_num += veh_num

    def GetAppdataRecord(self, sg, header):
        self.CreateIfAbsent(sg, header)
        return self.raw_sg_header[sg][header.id]

    def CreateIfAbsent(self, sg, header):
        if(sg not in self.raw_sg_header):
            self.raw_sg_header[sg] = {}
        if(header.id not in self.raw_sg_header[sg]):
            self.raw_sg_header[sg][header.id] = AppdataStatistic(header)

    # call by vehicle while createing new data.
    def VehicleCreateAppdata(self, sg, header):
        record = self.GetAppdataRecord(sg, header)

    # call by vehicle while receive data from other vehicles
    def VehicleReceivedIntactAppdata(self, sg, vehicle, header):
        current_time = GV.SUMO_SIM_INFO.getTime()
        record = self.GetAppdataRecord(sg, header)
        record.time_veh_trip[vehicle.name] = (
            current_time - header.at
        )

    # call by vehicle while application data has gone over time
    # def VehicleOverTimeAppdata(self, sg, headers):
    #     current_time = GV.SUMO_SIM_INFO.getTime()
    #     for header in headers:
    #         record = self.GetAppdataRecord(sg, header)
    #         record.is_src_ot = current_time

    # call by vehicle while application data has gone over time
    def BaseStationOverTimeAppdata(self, sg, bs, headers):
        pass

    # call by BaseStation while a appdata returns to TX queue
    def BaseStationAppdataEnterTXQ(self, sg, bs, headers):
        current_time = GV.SUMO_SIM_INFO.getTime()
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_txq[bs].append(
                [current_time, 0]
            )

    # call by BaseStation while a appdata exits TX queue
    def BaseStationAppdataExitTXQ(self, sg, bs, headers):
        current_time = GV.SUMO_SIM_INFO.getTime()
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_txq[bs][-1][1] = current_time

    # call by BaseStation while a appdata start TX
    def BaseStationAppdataStartTX(self, sg, bs, headers):
        current_time = GV.SUMO_SIM_INFO.getTime()
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_tx[bs].append(
                [current_time, 0]
            )

    # call by BaseStation while a appdata end TX
    def BaseStationAppdataEndTX(self, sg, bs, headers):
        current_time = GV.SUMO_SIM_INFO.getTime()
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_tx[bs][-1][1] = current_time

    # call by BaseStation while dropping a appdata
    def BaseStationAppdataDrop(self, sg, bs, headers):
        current_time = GV.SUMO_SIM_INFO.getTime()
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_drop[bs] = current_time

    # call by BaseStation when appdata totally served
    def BaseStationAppdataServe(self, sg, bs, headers):
        current_time = GV.SUMO_SIM_INFO.getTime()
        for header in headers:
            record = self.GetAppdataRecord(sg, header)
            record.time_bs_serv[bs] = current_time

    # extract specific network traffic from self.sg_headers
    def ExtractNetworkTraffic(self, nft, fresh=False):
        if(fresh or not nft in self.nft_traffic):
            traffic = {}

            if(nft == NetFlowType.CRITICAL):
                int_records = {}
                for sg in [
                    sg for sg in self.sg_header.keys()
                    if sg.qos == QoSLevel.CRITICAL
                ]:
                    for header, value in self.sg_header[sg].items():
                        if(header in int_records):
                            raise Exception("Appdata Duplicate in different Critical SocialGroups")
                        int_records[header] = value
                traffic = int_records
            elif(nft == NetFlowType.GENERAL):
                int_records = {}
                for sg in [
                    sg for sg in self.sg_header.keys()
                    if sg.qos == QoSLevel.GENERAL
                ]:
                    for header, value in self.sg_header[sg].items():
                        if(header in int_records):
                            raise Exception("Appdata Duplicate in different General SocialGroups")
                        int_records[header] = value
                traffic = int_records
            elif(nft == NetFlowType.C2G):
                crt_records = self.ExtractNetworkTraffic(NetFlowType.CRITICAL)
                gen_records = self.ExtractNetworkTraffic(NetFlowType.GENERAL)
                c2g_records = gen_records.copy()

                for header in gen_records.keys():
                    if(header not in crt_records):
                        c2g_records.pop(header)
                traffic = c2g_records
            elif(nft == NetFlowType.NC2G):
                gen_records = self.ExtractNetworkTraffic(NetFlowType.GENERAL)
                crt_records = self.ExtractNetworkTraffic(NetFlowType.CRITICAL)
                nc2g_records = gen_records.copy()

                for header in gen_records.keys():
                    if(header in crt_records):
                        nc2g_records.pop(header)
                traffic = nc2g_records

            self.nft_traffic[nft] = traffic

        return self.nft_traffic[nft]

    # create report for network traffics.
    def CreateReport(self):
        # summary of different estimate features
        sum_e2e_time = [None for x in NetFlowType]
        sum_wait_time = [None for x in NetFlowType]
        sum_tx_time = [None for x in NetFlowType]
        sum_bst_thrput = [[None for x in BaseStationType] for x in NetFlowType]
        sum_timeout_ratio = [None for x in NetFlowType]
        sum_veh_avg_arv_rate = [None for _ in NetFlowType]
        sum_veh_avg_arv_size = [None for _ in NetFlowType]
        sum_veh_avg_dep_rate = [None for _ in NetFlowType]
        sum_bs_avg_arv_rate = [None for _ in NetFlowType]
        sum_bs_avg_arv_size = [None for _ in NetFlowType]
        sum_bs_avg_dep_rate = [None for _ in NetFlowType]
        # summarize
        for nft in NetFlowType:
            GV.STATISTIC.Doc("<{}>".format(nft.name.upper()))
            app_stats = self.ExtractNetworkTraffic(nft)
            sum_e2e_time[nft] = self.VehicleReceivedIntactAppdataReport(app_stats)
            sum_wait_time[nft] = self.BaseStationAppdataTXQReport(app_stats)
            sum_tx_time[nft] = self.BaseStationAppdataTXReport(app_stats)
            sum_timeout_ratio[nft] = self.AppdataTimeoutRatioReport(app_stats)
            sum_veh_avg_arv_rate[nft] = self.VehicleAppdataArrivalRateReport(app_stats)
            sum_veh_avg_arv_size[nft] = self.VehicleAppdataArrivalSizeReport(app_stats)
            sum_veh_avg_dep_rate[nft] = self.VehicleAppdataDepartRateReport(app_stats)
            sum_bs_avg_arv_rate[nft] = self.BaseStationAppdataArrivalRateReport(app_stats)
            sum_bs_avg_arv_size[nft] = self.BaseStationAppdataArrivalSizeReport(app_stats)
            sum_bs_avg_dep_rate[nft] = self.BaseStationAppdataDepartRateReport(app_stats)
            for bst in BaseStationType:
                sum_bst_thrput[nft][bst] = self.BaseStationTypeThroughPutReport(app_stats, bst)
            GV.STATISTIC.Doc("</{}>".format(nft.name.upper()))

        # base station type throughput
        rep_bst_thrput = {
            bst.name: {
                nft.name: sum_bst_thrput[nft][bst]["bits"] for nft in NetFlowType
            }
            for bst in BaseStationType
        }
        rep_bst_thrput_rate = {
            bst.name: {
                nft.name: 0 for nft in NetFlowType
            }
            for bst in BaseStationType
        }
        for bst in BaseStationType:
            rep_bst_thrput[bst.name]["total"] = 0
            # add critical/general network flows
            for nft in [NetFlowType.CRITICAL, NetFlowType.GENERAL]:
                rep_bst_thrput[bst.name]["total"] += sum_bst_thrput[nft][bst]["bits"]
            # create report
            for nft in NetFlowType:
                rep_bst_thrput_rate[bst.name][nft.name] = (
                    sum_bst_thrput[nft][bst]["bits"] / max(1, rep_bst_thrput[bst.name]["total"])
                )

        # system throughput
        rep_sys_thrput = {
            nft.name: 0
            for nft in NetFlowType
        }
        rep_sys_thrput_rate = {
            nft.name: 0
            for nft in NetFlowType
        }
        rep_sys_thrput["total"] = 0
        for bst in BaseStationType:
            for nft in NetFlowType:
                bits = sum_bst_thrput[nft][bst]["bits"]
                rep_sys_thrput[nft.name] += bits
                if nft == NetFlowType.CRITICAL or nft == NetFlowType.GENERAL:
                    rep_sys_thrput["total"] += bits
        for nft in NetFlowType:
            rep_sys_thrput_rate[nft.name] = (
                rep_sys_thrput[nft.name] / max(1, rep_sys_thrput["total"])
            )

        # base station type social group usage
        rep_bst_sg_rate = {
            x.name: {
                y.name: None
                for y in NetFlowType
            }
            for x in BaseStationType
        }
        for bst in BaseStationType:
            total_count = 0
            # add critical/general network flows
            for nft in [NetFlowType.CRITICAL, NetFlowType.GENERAL]:
                total_count += sum_bst_thrput[nft][bst]["count"]

            # prevent deviding 0
            total_count = max(total_count, 1)

            # create report
            for nft in NetFlowType:
                rep_bst_sg_rate[bst.name][nft.name] = sum_bst_thrput[nft][bst]["count"] / total_count

        # end to end time
        rep_e2e_time = {
            x.name: sum_e2e_time[x]
            for x in NetFlowType
        }
        # wait time
        rep_wait_time = {
            x.name: sum_wait_time[x]
            for x in NetFlowType
        }
        # transmit time
        rep_tx_time = {
            x.name: sum_tx_time[x]
            for x in NetFlowType
        }
        # timeout ratio
        rep_timeout_ratio = {
            x.name: sum_timeout_ratio[x]
            for x in NetFlowType
        }

        # little's law variables
        # . base station
        rep_veh_arv_rate = {
            x.name: sum_veh_avg_arv_rate[x]
            for x in NetFlowType
        }
        rep_veh_arv_size = {
            x.name: sum_veh_avg_arv_size[x]
            for x in NetFlowType
        }
        rep_veh_dep_rate = {
            x.name: sum_veh_avg_dep_rate[x]
            for x in NetFlowType
        }
        rep_bs_arv_rate = {
            x.name: {
                bs.name: sum_bs_avg_arv_rate[x][bs]
                for bs in GV.NET_STATION_CONTROLLER
            } for x in NetFlowType
        }
        rep_bs_arv_size = {
            x.name: {
                bs.name: sum_bs_avg_arv_size[x][bs]
                for bs in GV.NET_STATION_CONTROLLER
            } for x in NetFlowType
        }
        rep_bs_dep_rate = {
            x.name: {
                bs.name: sum_bs_avg_dep_rate[x][bs]
                for bs in GV.NET_STATION_CONTROLLER
            } for x in NetFlowType
        }
        # create report
        report = {
            "end-to-end": rep_e2e_time,
            "wait-time": rep_wait_time,
            "tx-time": rep_tx_time,
            "bst-thrput": rep_bst_thrput,
            "bst-thrput-rate": rep_bst_thrput_rate,
            "sys-thrput": rep_sys_thrput,
            "sys-thrput-rate": rep_sys_thrput_rate,
            "bst-sg-rate": rep_bst_sg_rate,
            "to-ratio": rep_timeout_ratio,
            "veh-arv-rate": rep_veh_arv_rate,
            "veh-arv-size": rep_veh_arv_size,
            "veh-dep-rate": rep_veh_dep_rate,
            "bs-arv-rate": rep_bs_arv_rate,
            "bs-arv-size": rep_bs_arv_size,
            "bs-dep-rate": rep_bs_dep_rate,
        }

        # print report
        self.PrintReport(report, 0)

        return report

    # print report function
    def PrintReport(self, report, depth):
        for key, value in report.items():
            text = "[{}]".format(str(key).upper())
            if depth > 0:
                text = "{:>{}s}".format("", 4 * depth) + text

            if type(value) is not dict:
                text += ":{:.4f}".format(value)
                GV.RESULT.Doc(text)
            else:
                GV.RESULT.Doc(text)
                self.PrintReport(value, depth + 1)
        if depth == 0:
            GV.RESULT.Doc("")

    # Reports
    def VehicleReceivedIntactAppdataReport(self, app_stats):
        GV.STATISTIC.Doc("<End-to-End>")
        # predefine
        total_trip_time = 0
        total_trip_count = 0
        max_trip_time = float('-inf')
        min_trip_time = float('inf')
        avg_trip_time = 0
        # collect data from app stats
        for header_id, record in app_stats.items():
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
                '[{}]:{{ sum:{:.4f}s, num:{:.0f}, avg:{:.4f}s, max:{:.4f}s, min:{:.4f}s}}'.format(
                    header_id,
                    record_total_trip_time,
                    record_total_trip_count,
                    record_avg_trip_time,
                    record_max_trip_time,
                    record_min_trip_time,
                )
            )
            total_trip_time += record_total_trip_time
            total_trip_count += record_total_trip_count
            min_trip_time = min_trip_time if min_trip_time < record_min_trip_time else record_min_trip_time
            max_trip_time = max_trip_time if max_trip_time > record_max_trip_time else record_max_trip_time

        # calculate average
        avg_trip_time = (0 if total_trip_count == 0 else total_trip_time / total_trip_count)
        GV.STATISTIC.Doc("</End-to-End>")
        return {
            "avg": avg_trip_time,
            "max": max_trip_time,
            "min": min_trip_time,
        }

    def BaseStationAppdataTXQReport(self, app_stats):
        GV.STATISTIC.Doc("<TXQ-WAIT>")
        # time waited of appdata in transmit queue
        max_txq_wait_time = float('-inf')
        min_txq_wait_time = float('inf')
        total_txq_wait_time = 0
        total_txq_wait_count = 0
        avg_txq_wait_time = 0
        for header_id, record in app_stats.items():
            # the time for this appdata to wait in the transmit queues
            record_max_txq_wait_time = float('-inf')
            record_min_txq_wait_time = float('inf')
            record_total_txq_wait_time = 0
            record_total_txq_wait_count = 0
            # evaluate record
            for bs in GV.NET_STATION_CONTROLLER:
                serial = bs.serial
                bs_total_txq_wait_time = 0
                # the data was never received by this base station, ignore.
                if(len(record.time_bs_txq[serial]) == 0):
                    continue
                # sum up total base station txq wait time.
                for time_interval in record.time_bs_txq[serial]:
                    time_enter = time_interval[0]
                    time_exit = time_interval[1]
                    # Error detection
                    if(time_enter == 0 or time_exit == 0):
                        GV.ERROR.Log(
                            "Error! TXQ time unexpected. {}".format(record.time_bs_txq[serial])
                        )
                    # accumulate time.
                    if(not math.isclose(time_enter, time_exit) and time_enter * time_exit > 0):
                        bs_total_txq_wait_time += (time_exit - time_enter)

                # ignore if there's no waiting time.
                # if bs_total_txq_wait_time == 0:
                #     continue

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
            # record summary
            record_avg_txq_wait_time = (
                0 if record_total_txq_wait_count == 0
                else record_total_txq_wait_time / record_total_txq_wait_count
            )
            GV.STATISTIC.Doc(
                '[{}]:{{ sum:{:.4f}s, num:{:.0f}, avg:{:.4f}s, max:{:.4f}s, min:{:.4f}s}}'.format(
                    header_id,
                    record_total_txq_wait_time,
                    record_total_txq_wait_count,
                    record_avg_txq_wait_time,
                    record_max_txq_wait_time,
                    record_min_txq_wait_time,
                )
            )
            # add record
            total_txq_wait_time += record_total_txq_wait_time
            total_txq_wait_count += record_total_txq_wait_count
            max_txq_wait_time = max_txq_wait_time if max_txq_wait_time > record_max_txq_wait_time else record_max_txq_wait_time
            min_txq_wait_time = min_txq_wait_time if min_txq_wait_time < record_min_txq_wait_time else record_min_txq_wait_time

        avg_txq_wait_time = (0 if total_txq_wait_count ==
                             0 else total_txq_wait_time / total_txq_wait_count)

        GV.STATISTIC.Doc("</TXQ-WAIT>")
        return {
            "avg": avg_txq_wait_time,
            "max": max_txq_wait_time,
            "min": min_txq_wait_time,
        }

    def BaseStationAppdataTXReport(self, app_stats):
        GV.STATISTIC.Doc("<TX-TIME>")
        max_tx_time = float('-inf')
        min_tx_time = float('inf')
        total_tx_time = 0
        total_tx_count = 0
        avg_tx_time = 0
        for header_id, record in app_stats.items():
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
            # record summary
            record_avg_tx_time = (
                0 if record_total_tx_count == 0
                else record_total_tx_time / record_total_tx_count
            )
            GV.STATISTIC.Doc(
                '[{}]:{{ sum:{:.4f}s, num:{:.0f}, avg:{:.4f}s, max:{:.4f}s, min:{:.4f}s}}'.format(
                    header_id,
                    record_total_tx_time,
                    record_total_tx_count,
                    record_avg_tx_time,
                    record_max_tx_time,
                    record_min_tx_time,
                )
            )
            # accumulate record
            total_tx_time += record_total_tx_time
            total_tx_count += record_total_tx_count
            max_tx_time = max_tx_time if max_tx_time > record_max_tx_time else record_max_tx_time
            min_tx_time = min_tx_time if min_tx_time < record_min_tx_time else record_min_tx_time

        avg_tx_time = (0 if total_tx_count == 0 else total_tx_time / total_tx_count)
        GV.STATISTIC.Doc("</TX-TIME>")
        return {
            "avg": avg_tx_time,
            "max": max_tx_time,
            "min": min_tx_time,
        }

    def AppdataTimeoutRatioReport(self, app_stats):
        ot_data = 0
        for record in app_stats.values():
            if(record.is_src_ot or (True in record.is_bs_ot)):
                ot_data += 1
        return ot_data / max(len(app_stats), 1)

    def BaseStationTypeThroughPutReport(self, app_stats, bs_type):
        # size of data.
        bits = 0
        # number of data.
        count = 0
        # prevent duplicating data.
        bs_ctrlrs = [x for x in GV.NET_STATION_CONTROLLER if x.type == bs_type]

        for header, record in app_stats.items():
            for bs in bs_ctrlrs:
                if(record.time_bs_serv[bs] > 0):
                    bits += record.bits
                    count += 1
                    break

        return {
            "bits": bits,
            "count": count
        }

    def BaseStationSocialGroupResourceUsageReport(self):
        sg_stats = {}
        sg_bs_type_data = [[0 for _ in self.social_group]
                           for _ in BaseStationType]
        for sg in self.social_group:
            for record in self.sg_header[sg].values():
                for bs in GV.NET_STATION_CONTROLLER:
                    if(record.time_bs_serv[bs] > 0):
                        sg_bs_type_data[bs.type][sg] += 1

        for bs_type in BaseStationType:
            bs_type_total_data = max(sum(sg_bs_type_data[bs_type]), 1)
            bs_type_sg_res_rate = [0 for _ in self.social_group]
            GV.RESULT.Doc("====={}=====".format(bs_type.name))
            for sg in self.social_group:
                bs_type_sg_res_rate[sg] = (
                    sg_bs_type_data[bs_type][sg] / bs_type_total_data
                )
                GV.RESULT.Doc(
                    "{} Resource Usage: {:.2f}%".format(
                        sg,
                        bs_type_sg_res_rate[sg] * 100
                    )
                )
            sg_stats[bs_type] = bs_type_sg_res_rate

        return sg_stats

    def BaseStationSocailGroupDataDropRateReport(self):
        sg_stats = {}
        sg_bs_type_recv = [[0 for _ in self.social_group]
                           for _ in BaseStationType]
        sg_bs_type_drop = [[0 for _ in self.social_group]
                           for _ in BaseStationType]
        GV.STATISTIC.Doc("=====BaseStationSocailGroupDataDropRateReport=====")
        for sg in self.social_group:
            for record in self.sg_header[sg].values():
                for bs in GV.NET_STATION_CONTROLLER:
                    if(len(record.time_bs_txq[bs]) > 0):
                        sg_bs_type_recv[bs.type][sg] += 1
                    if(record.time_bs_drop[bs] > 0):
                        sg_bs_type_drop[bs.type][sg] += 1

        for bs_type in BaseStationType:
            GV.RESULT.Doc("====={}=====".format(bs_type.name))
            bs_type_sg_drop_rate = [0 for _ in self.social_group]
            for sg in self.social_group:
                bs_type_sg_drop_rate[sg] = (
                    sg_bs_type_drop[bs_type][sg] /
                    max(sg_bs_type_recv[bs_type][sg], 1)
                )
                GV.RESULT.Doc(
                    "{} Drop Rate: {:.2f}%".format(
                        sg,
                        bs_type_sg_drop_rate[sg] * 100
                    )
                )
            sg_stats[bs_type] = bs_type_sg_drop_rate
        return sg_stats

    def VehicleAppdataArrivalRateReport(self, app_stats):
        time_orgnz_record = {}
        _max = 0
        _min = 0
        _avg = 0
        _num = 0
        if(len(app_stats) > 0):
            for record in app_stats.values():
                time = record.at
                if(time not in time_orgnz_record):
                    time_orgnz_record[time] = 1
                else:
                    time_orgnz_record[time] += 1
            _max = max(time_orgnz_record.values())
            _min = min(time_orgnz_record.values())
            _avg = sum(time_orgnz_record.values()) / (self.RecordDuration() * 1000)
            _num = sum(time_orgnz_record.values())
        # print(time_orgnz_record)
        return {
            "max": _max,
            "avg": _avg,
            "min": _min,
            "num": _num
        }

    def VehicleAppdataArrivalSizeReport(self, app_stats):
        time_orgnz_record = {}
        _max = 0
        _min = 0
        _avg = 0
        _num = 0
        if(len(app_stats) > 0):
            for record in app_stats.values():
                time = record.at
                if(time not in time_orgnz_record):
                    time_orgnz_record[time] = []
                time_orgnz_record[time].append(record.bits)
            per_ms_avg_data_size = [sum(x) / len(x) for x in time_orgnz_record.values()]
            all_data_size = [v for x in time_orgnz_record.values() for v in x]
            _max = max(per_ms_avg_data_size)
            _min = min(per_ms_avg_data_size)
            _avg = sum(all_data_size) / len(all_data_size)
            _num = len(all_data_size)
        return {
            "max": _max,
            "avg": _avg,
            "min": _min,
            "num": _num
        }

    def VehicleAppdataDepartRateReport(self, app_stats):
        time_orgnz_record = {}
        _max = 0
        _min = 0
        _avg = 0
        _num = 0
        if(len(app_stats) > 0):
            for record in app_stats.values():
                time_enter_bs_txq = [
                    time_per_bs_txq[0][0]
                    for time_per_bs_txq in record.time_bs_txq
                    if len(time_per_bs_txq) > 0
                ]
                if(len(time_enter_bs_txq) > 0):
                    time = min(time_enter_bs_txq)
                    if(time not in time_orgnz_record):
                        time_orgnz_record[time] = 1
                    else:
                        time_orgnz_record[time] += 1
            if(len(time_orgnz_record) > 0):
                _max = max(time_orgnz_record.values())
                _min = min(time_orgnz_record.values())
                _avg = sum(time_orgnz_record.values()) / (self.RecordDuration() * 1000)
                _num = sum(time_orgnz_record.values())
        return {
            "max": _max,
            "avg": _avg,
            "min": _min,
            "num": _num
        }

    def BaseStationAppdataArrivalRateReport(self, app_stats):
        bs_report = []
        if(len(app_stats) > 0):
            for bs in GV.NET_STATION_CONTROLLER:
                time_orgnz_record = {}
                _max = 0
                _min = 0
                _avg = 0
                _num = 0
                for record in app_stats.values():
                    if(len(record.time_bs_txq[bs]) > 0):
                        time = record.time_bs_txq[bs][0][0]
                        if(not time in time_orgnz_record):
                            time_orgnz_record[time] = 1
                        else:
                            time_orgnz_record[time] += 1
                if(len(time_orgnz_record) > 0):
                    _max = max(time_orgnz_record.values())
                    _min = min(time_orgnz_record.values())
                    _avg = sum(time_orgnz_record.values()) / self.RecordDuration() / 1000
                    _num = sum(time_orgnz_record.values())
                bs_report.append(
                    {
                        "max": _max,
                        "avg": _avg,
                        "min": _min,
                        "num": _num
                    }
                )
        else:
            bs_report = [
                {
                    "max": 0,
                    "avg": 0,
                    "min": 0,
                    "num": 0
                }
                for _ in GV.NET_STATION_CONTROLLER
            ]
        return bs_report

    def BaseStationAppdataArrivalSizeReport(self, app_stats):
        bs_report = []
        if(len(app_stats) > 0):
            for bs in GV.NET_STATION_CONTROLLER:
                time_orgnz_record = {}
                _max = 0
                _min = 0
                _avg = 0
                _num = 0
                for record in app_stats.values():
                    if(len(record.time_bs_txq[bs]) > 0):
                        time = record.time_bs_txq[bs][0][0]
                        if(not time in time_orgnz_record):
                            time_orgnz_record[time] = []
                        time_orgnz_record[time].append(record.bits)
                if(len(time_orgnz_record) > 0):
                    per_ms_avg_data_size = [sum(x) / len(x) for x in time_orgnz_record.values()]
                    total_data_size = [x for i in time_orgnz_record.values() for x in i]
                    _max = max(per_ms_avg_data_size)
                    _min = min(per_ms_avg_data_size)
                    _avg = sum(total_data_size) / len(total_data_size)
                    _num = len(total_data_size)
                bs_report.append(
                    {
                        "max": _max,
                        "avg": _avg,
                        "min": _min,
                        "num": _num
                    }
                )
        else:
            bs_report = [
                {
                    "max": 0,
                    "avg": 0,
                    "min": 0,
                    "num": 0
                }
                for _ in GV.NET_STATION_CONTROLLER
            ]
        return bs_report

    def BaseStationAppdataDepartRateReport(self, app_stats):
        bs_report = []
        if(len(app_stats) > 0):
            for bs in GV.NET_STATION_CONTROLLER:
                time_orgnz_record = {}
                _max = 0
                _min = 0
                _avg = 0
                _num = 0
                for record in app_stats.values():
                    time = record.time_bs_serv[bs]
                    if(time > 0):
                        if(not time in time_orgnz_record):
                            time_orgnz_record[time] = 1
                        else:
                            time_orgnz_record[time] += 1
                if(len(time_orgnz_record) > 0):
                    _max = max(time_orgnz_record.values())
                    _min = min(time_orgnz_record.values())
                    _avg = sum(time_orgnz_record.values()) / self.RecordDuration() / 1000
                    _num = sum(time_orgnz_record.values())
                bs_report.append(
                    {
                        "max": _max,
                        "avg": _avg,
                        "min": _min,
                        "num": _num
                    }
                )
        else:
            bs_report = [
                {
                    "max": 0,
                    "avg": 0,
                    "min": 0,
                    "num": 0
                }
                for _ in GV.NET_STATION_CONTROLLER
            ]
        return bs_report

    def Preprocess(self):
        # preprocess only raw statistic data, if it has been processed, skip process.
        if(not self.raw_sg_header):
            print("Skipping Preprocess, Since there's no Raw Data.")
            return

        # save the whole social group generated during simulation
        self.social_group = [sg for sg in SocialGroup]

        # create empty dataset for social groups without data during simulation.
        for sg in self.social_group:
            if(sg not in self.raw_sg_header):
                self.raw_sg_header[sg] = {}

        # extract only appdata that're in interest intervals.
        for sg in self.social_group:
            self.sg_header[sg] = {
                header: record
                for header, record in self.raw_sg_header[sg].items()
                if (record.at >= self.interval[0] and
                    record.at < self.interval[1])
            }

        # clean raw appdata since we have our interest intervals.
        self.raw_sg_header = None

        # preprocess txq timing adjustments
        for sg in self.social_group:
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

        # preprocess overtimes
        for sg in self.social_group:
            for record in self.sg_header[sg].values():
                # ignore appdata that're flagged overtime.
                if(record.is_src_ot):
                    continue
                else:
                    # Check data source overtime condition.
                    in_txq_time = list(filter(lambda x: len(x) > 0, record.time_bs_txq))
                    min_enter_txq_time = min(
                        list(map(
                            lambda x: x[0][0],
                            in_txq_time
                        )) + [NET_TIMEOUT_SECONDS + record.at]
                    )
                    if(len(in_txq_time) == 0 or
                       min_enter_txq_time - record.at >= NET_TIMEOUT_SECONDS):
                        record.is_src_ot = True
                    else:
                        # Check base station overtime condition.
                        for bs in GV.NET_STATION_CONTROLLER:
                            if(
                                len(record.time_bs_txq[bs]) > 0 and
                                record.time_bs_txq[bs][-1][1] - record.at >= NET_TIMEOUT_SECONDS
                            ):
                                record.is_bs_ot[bs] = True

        # preprocess wait time adjustment(0.5ms -> 1ms)
        for sg in self.social_group:
            for record in self.sg_header[sg].values():
                for bs in GV.NET_STATION_CONTROLLER:
                    for pair in record.time_bs_txq[bs]:
                        pair[0] = math.ceil(round(pair[0], 4) * 1000) / 1000
                        pair[1] = math.ceil(round(pair[1], 4) * 1000) / 1000

    def Report(self, save=True):
        # preprocess the raw statistics
        self.Preprocess()
        # create report
        statistic_report = self.CreateReport()
        statistic_report["interest"] = self.interest_config
        # save the statistic to file for further estimation
        if save:
            if not os.path.isdir(self.dirpath):
                os.makedirs(self.dirpath)
            report_filename = 'report.pickle'
            object_filename = 'object.pickle'
            with open(self.dirpath + report_filename, 'wb') as interest_statistic_report_file:
                pickle.dump(statistic_report, interest_statistic_report_file)
            with open(self.dirpath + object_filename, 'wb') as interest_statistic_object_file:
                pickle.dump(self, interest_statistic_object_file)
        # return statistic object
        return statistic_report
