# Custom
from od.social import SocialGroup
from od.env.config import (SUMO_SECONDS_PER_STEP, NET_SECONDS_PER_STEP,
                           NET_SECONDS_PER_TS, SUMO_TOTAL_SECONDS, SUMO_SIM_SECONDS,
                           SUMO_SKIP_SECONDS, SUMO_NET_WARMUP_SECONDS, EVENT_CONFIGS, NET_TIMEOUT_SECONDS)
from od.network.types import BaseStationType
from od.misc.interest import InterestConfig
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
        self.dirpath = dirpath
        self.interest_config = interest_config
        self.sg_header = [{} for _ in SocialGroup]
        self.interval = (
            SUMO_SKIP_SECONDS + SUMO_NET_WARMUP_SECONDS + min(map(lambda x: x.ofs_sec, EVENT_CONFIGS)),
            SUMO_SKIP_SECONDS + SUMO_NET_WARMUP_SECONDS + max(map(lambda x: x.ofs_sec+x.dur_sec, EVENT_CONFIGS))
        )

    def GetAppdataRecord(self, sg, header):
        self.CreateIfAbsent(sg, header)
        return self.sg_header[sg][header.id]

    def CreateIfAbsent(self, sg, header):
        if(header.id not in self.sg_header[sg]):
            self.sg_header[sg][header.id] = AppdataStatistic(header)

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
    def ExtractNetworkTraffic(self, nft):
        if(nft == NetFlowType.CRITICAL):
            return self.sg_header[SocialGroup.CRASH]
        elif(nft == NetFlowType.GENERAL):
            return self.sg_header[SocialGroup.RCWS]
        elif(nft == NetFlowType.C2G):
            umi_bs_ctrlrs = [x for x in GV.NET_STATION_CONTROLLER if x.type == BaseStationType.UMI]
            flows = {}
            for header, record in self.sg_header[SocialGroup.CRASH].items():
                for bs_ctrlr in umi_bs_ctrlrs:
                    if record.time_bs_serv[bs_ctrlr] > 0:
                        if(header in self.sg_header[SocialGroup.RCWS]):
                            flows[header] = self.sg_header[SocialGroup.RCWS][header]
            return flows
        elif(nft == NetFlowType.NC2G):
            umi_bs_ctrlrs = [x for x in GV.NET_STATION_CONTROLLER if x.type == BaseStationType.UMI]
            nc2g_flows = {}
            g_set = set(self.sg_header[SocialGroup.RCWS])
            c2g_set = set()
            for header, record in self.sg_header[SocialGroup.CRASH].items():
                for bs_ctrlr in umi_bs_ctrlrs:
                    if record.time_bs_serv[bs_ctrlr] > 0:
                        if(header in self.sg_header[SocialGroup.RCWS]):
                            c2g_set.add(header)
            for header in (g_set - c2g_set):
                nc2g_flows[header] = self.sg_header[SocialGroup.RCWS][header]
            return nc2g_flows
        return {}

    # create report for network traffics.
    def CreateReport(self):
        # summary of different estimate features
        sum_e2e_time = [None for x in NetFlowType]
        sum_wait_time = [None for x in NetFlowType]
        sum_tx_time = [None for x in NetFlowType]
        sum_bst_thrput = [[None for x in BaseStationType] for x in NetFlowType]
        sum_timeout_ratio = [None for x in NetFlowType]
        # summarize
        for nft in NetFlowType:
            GV.STATISTIC.Doc("<{}>".format(nft.name.upper()))
            app_stats = self.ExtractNetworkTraffic(nft)
            sum_e2e_time[nft] = self.VehicleReceivedIntactAppdataReport(app_stats)
            sum_wait_time[nft] = self.BaseStationAppdataTXQReport(app_stats)
            sum_tx_time[nft] = self.BaseStationAppdataTXReport(app_stats)
            sum_timeout_ratio[nft] = self.AppdataSourceTimeoutRatioReport(app_stats)
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
        }

        # print report
        self.PrintReport(report, 0)

        return report

    # print report function
    def PrintReport(self, report, depth):
        for key, value in report.items():
            text = "[{}]".format(str(key).upper())
            if depth > 0:
                text = "{:>{}s}".format("", 4*depth) + text

            if type(value) is not dict:
                text += ":{:.4f}".format(value)
                GV.RESULT.Doc(text)
            else:
                GV.RESULT.Doc(text)
                self.PrintReport(value, depth+1)
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
                else record_total_txq_wait_time/record_total_txq_wait_count
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

    def AppdataSourceTimeoutRatioReport(self, app_stats):
        total_bits = 0
        ot_bits = 0
        for record in app_stats.values():
            total_bits += record.bits
            if(record.is_src_ot):
                ot_bits += record.bits
        return ot_bits/max(total_bits, 1)

    # def BaseStationAppdataTimeoutRatioReport(self, app_stats):
    #    pass

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
        # extract only appdata that're in interest intervals.
        for sg in SocialGroup:
            self.sg_header[sg] = {
                header: record
                for header, record in self.sg_header[sg].items()
                if (record.at >= self.interval[0] and
                    record.at <= self.interval[1])
            }

        # preprocess txq timing adjustments
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

        # preprocess overtimes
        for sg in SocialGroup:
            for record in self.sg_header[sg].values():
                # ignore appdata that're flagged overtime.
                if(record.is_src_ot):
                    continue
                # Check data source overtime condition.
                elif(max(map(lambda x: len(x), record.time_bs_txq)) == 0):
                    record.is_src_ot = True
                # Check base station overtime condition.
                else:
                    for bs in GV.NET_STATION_CONTROLLER:
                        if(record.time_bs_serv[bs] - record.at >= NET_TIMEOUT_SECONDS):
                            record.is_bs_ot[bs] = True

    def Report(self, save=True):
        # preprocess the raw statistics
        self.Preprocess()
        # create report
        statistic_report = self.CreateReport()
        statistic_report["interest"] = self.interest_config
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
