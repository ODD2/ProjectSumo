from globs import SocialGroup
from globs import SUMO_SIM_INFO, NET_SECONDS_PER_STEP, NET_SECONDS_PER_TS
from sim_log import STATISTIC
import net_model as nm


class AppdataStatistic:
    def __init__(self):
        self.time_veh_recv = {}
        self.time_bs_txq_enter = [0 for _ in nm.BASE_STATION_CONTROLLER]
        self.time_bs_txq_exit = [0 for _ in nm.BASE_STATION_CONTROLLER]
        self.time_bs_tx_beg = [0 for _ in nm.BASE_STATION_CONTROLLER]
        self.time_bs_tx_end = [0 for _ in nm.BASE_STATION_CONTROLLER]


class StatisticRecorder:
    def __init__(self):
        self.sg_header = [{} for _ in SocialGroup]

    def GetAppdataRecord(self, sg, header):
        self.CreateIfAbsent(sg, header)
        return self.sg_header[sg][header]

    def CreateIfAbsent(self, sg, header):
        if(header not in self.sg_header[sg]):
            self.sg_header[sg][header] = AppdataStatistic()

    def VehicleReceivedIntactAppdata(self, sg, header, vehicle):
        record = self.GetAppdataRecord(sg, header)
        record.time_veh_recv[header] = SUMO_SIM_INFO.getTime()

    def BaseStationAppdataEnterTXQ(self, sg, bs, header):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_txq_enter[bs] = SUMO_SIM_INFO.getTime()

    def BaseStationAppdataExitTXQ(self, sg, bs, header):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_txq_exit[bs] = SUMO_SIM_INFO.getTime()

    def BaseStationAppdataStartTX(self, sg, bs, header, start_ts):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_tx_beg[bs] = (
            SUMO_SIM_INFO.getTime() + start_ts * NET_SECONDS_PER_TS
        )

    def BaseStationAppdataEndTX(self, sg, bs, header, end_ts):
        record = self.GetAppdataRecord(sg, header)
        record.time_bs_tx_end[bs] = (
            SUMO_SIM_INFO.getTime() + end_ts * NET_SECONDS_PER_TS
        )

    def VehicleReceivedIntactAppdataReport(self):
        STATISTIC.Log("=====VehicleReceivedIntactAppdataReport=====")
        sim_max_trip_time = 0
        sim_min_trip_time = 0
        sim_total_trip_time = 0
        sim_total_trip_count = 0
        for sg in SocialGroup:
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
                    record_total_trip_time / max(record_total_trip_count, 1)
                )
                STATISTIC.Log(
                    '{}-{}:{{sum:{}s, num:{}, avg:{}s, max:{}s, min:{}s}}'.format(
                        str(sg),
                        header.id,
                        record_total_trip_time,
                        record_total_trip_count,
                        record_avg_trip_time,
                        record_max_trip_time,
                        record_min_trip_time,
                    )
                )
                sim_total_trip_time += record_total_trip_time
                sim_total_trip_count += record_total_trip_count
                sim_min_trip_time = sim_min_trip_time if sim_min_trip_time < record_min_trip_time else record_min_trip_time
                sim_max_trip_time = sim_max_trip_time if sim_max_trip_time > record_max_trip_time else record_max_trip_time

            sim_avg_trip_time = (
                sim_total_trip_time / max(sim_total_trip_count, 1)
            )
            print("====={}=====".format(sg))
            print("Average Trip Time: {}s".format(sim_avg_trip_time))
            print("Maximum Trip Time: {}s".format(sim_max_trip_time))
            print("Minimum Trip Time: {}s".format(sim_min_trip_time))

    def BaseStationAppdataTXQReport(self):
        STATISTIC.Log("=====BaseStationAppdataTXQReport=====")
        # time waited of appdata in transmit queue
        sim_max_txq_wait_time = float('-inf')
        sim_min_txq_wait_time = float('inf')
        sim_total_txq_wait_time = 0
        sim_total_txq_count = 0
        sim_avg_txq_wait_time = 0
        for sg in SocialGroup:
            for header, record in self.sg_header[sg].items():
                # the time for this appdata to wait in the transmit queues
                record_max_txq_wait_time = float('-inf')
                record_min_txq_wait_time = float('inf')
                record_total_txq_wait_time = 0
                record_total_txq_count = 0
                # evaluate record
                for bs in nm.BASE_STATION_CONTROLLER:
                    serial = bs.serial
                    if(record.time_bs_txq_enter[serial] * record.time_bs_txq_exit[serial] > 0):
                        txq_wait_time = (
                            record.time_bs_txq_exit[serial] -
                            record.time_bs_txq_enter[serial]
                        )
                        if txq_wait_time > 1:
                            a = 0
                        if(txq_wait_time == 0):
                            continue
                        record_total_txq_count += 1
                        record_total_txq_wait_time += txq_wait_time
                        record_max_txq_wait_time = record_max_txq_wait_time if record_max_txq_wait_time > txq_wait_time else txq_wait_time
                        record_min_txq_wait_time = record_min_txq_wait_time if record_min_txq_wait_time < txq_wait_time else txq_wait_time
                # record summery
                record_avg_txq_wait_time = (
                    record_total_txq_wait_time/max(record_total_txq_count, 1)
                )
                STATISTIC.Log(
                    '{}-{}:{{ sum:{}s, num:{}, avg:{}s, max:{}s, min:{}s}}'.format(
                        str(sg),
                        header.id,
                        record_total_txq_wait_time,
                        record_total_txq_count,
                        record_avg_txq_wait_time,
                        record_max_txq_wait_time,
                        record_min_txq_wait_time,
                    )
                )
                # accumulate record
                sim_total_txq_wait_time += record_total_txq_wait_time
                sim_total_txq_count += record_total_txq_count
                sim_max_txq_wait_time = sim_max_txq_wait_time if sim_max_txq_wait_time > record_max_txq_wait_time else record_max_txq_wait_time
                sim_min_txq_wait_time = sim_min_txq_wait_time if sim_min_txq_wait_time < record_min_txq_wait_time else record_min_txq_wait_time
            # simulation summery
            sim_avg_txq_wait_time = (
                sim_total_txq_wait_time / max(sim_total_txq_count, 1)
            )
            print("====={}=====".format(sg))
            print("Average TXQ Time:{}s".format(sim_avg_txq_wait_time))
            print("Maximum TXQ Time:{}s".format(sim_max_txq_wait_time))
            print("Minimum TXQ Time:{}s".format(sim_min_txq_wait_time))

    def BaseStationAppdataTXReport(self):
        STATISTIC.Log("=====BaseStationAppdataTXReport=====")
        sim_max_tx_time = float('-inf')
        sim_min_tx_time = float('inf')
        sim_total_tx_time = 0
        sim_total_tx_count = 0
        sim_avg_tx_time = 0
        for sg in SocialGroup:
            for header, record in self.sg_header[sg].items():
                # the time for this appdata delivered by all base stations.
                record_max_tx_time = float('-inf')
                record_min_tx_time = float('inf')
                record_total_tx_time = 0
                record_total_tx_count = 0
                # evaluate record
                for bs in nm.BASE_STATION_CONTROLLER:
                    serial = bs.serial
                    if(record.time_bs_tx_beg[serial] * record.time_bs_tx_end[serial] > 0):
                        tx_time = (
                            record.time_bs_tx_end[serial] -
                            record.time_bs_tx_beg[serial]
                        )
                        record_total_tx_count += 1
                        record_total_tx_time += tx_time
                        record_max_tx_time = record_max_tx_time if record_max_tx_time > tx_time else tx_time
                        record_min_tx_time = record_min_tx_time if record_min_tx_time < tx_time else tx_time
                # record summery
                record_avg_tx_time = (
                    record_total_tx_time/max(record_total_tx_count, 1)
                )
                STATISTIC.Log(
                    '{}-{}:{{ sum:{}s, num:{}, avg:{}s, max:{}s, min:{}s}}'.format(
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
                sim_total_tx_time += record_total_tx_time
                sim_total_tx_count += record_total_tx_count
                sim_max_tx_time = sim_max_tx_time if sim_max_tx_time > record_max_tx_time else record_max_tx_time
                sim_min_tx_time = sim_min_tx_time if sim_min_tx_time < record_min_tx_time else record_min_tx_time
            # simulation summery
            sim_avg_tx_time = sim_total_tx_time/max(sim_total_tx_count, 1)
            print("====={}=====".format(sg))
            print("Average TX Time:{}s".format(sim_avg_tx_time))
            print("Maximum TX Time:{}s".format(sim_max_tx_time))
            print("Minimum TX Time:{}s".format(sim_min_tx_time))


STATISTIC_RECORDER = StatisticRecorder()
