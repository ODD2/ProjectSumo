from globs import SUMO_SIM_INFO
import net_model as nm


class AppdataStatistic:
    def __init__(self):
        self.time_veh_recv = {}
        self.time_bs_txq_enter = [0 for _ in nm.BASE_STATION_CONTROLLER]
        self.time_bs_txq_exit = [0 for _ in nm.BASE_STATION_CONTROLLER]
        self.time_bs_tx_beg = [0 for _ in nm.BASE_STATION_CONTROLLER]
        self.time_bs_tx_end = [0 for _ in nm.BASE_STATION_CONTROLLER]

    def TimeElapseTrip(self, veh):
        return 0

    def AvgTimeElapseTXQ(self):
        return 0

    def TimeElapseTXQ(self, bs):
        return 1

    def AvgTimeElapseTX(self):
        return 0

    def TimeElapseTX(self, bs):
        return 0


class StatisticRecorder:
    def __init__(self):
        self.appdata_record = {}

    def GetAppdataRecord(self, appdata_header):
        self.CreateIfAbsent(appdata_header)
        return self.appdata_record[appdata_header]

    def CreateIfAbsent(self, appdata_header):
        if(appdata_header not in self.appdata_record):
            self.appdata_record[appdata_header] = AppdataStatistic()

    def VehicleReceivedIntactAppdata(self, appdata_header, vehicle):
        record = self.GetAppdataRecord(appdata_header)
        record.time_veh_recv[appdata_header] = SUMO_SIM_INFO.time

    def BaseStationAppdataEnterTXQ(self, bs, appdata_header):
        record = self.GetAppdataRecord(appdata_header)
        record.time_bs_txq_enter[bs] = SUMO_SIM_INFO.time

    def BaseStationAppdataExitTXQ(self, bs, appdata_header):
        record = self.GetAppdataRecord(appdata_header)
        record.time_bs_txq_exit[bs] = SUMO_SIM_INFO.time

    def BaseStationAppdataStartTX(self, bs, appdata_header):
        record = self.GetAppdataRecord(appdata_header)
        record.time_bs_tx_beg[bs] = SUMO_SIM_INFO.time

    def BaseStationAppdataEndTX(self, bs, appdata_header):
        record = self.GetAppdataRecord(appdata_header)
        record.time_bs_tx_end[bs] = SUMO_SIM_INFO.time

    def VehicleReceivedIntactAppdataReport(self):
        sim_max_trip_time = 0
        sim_min_trip_time = 0
        sim_total_trip_time = 0
        sim_total_trip_count = 0
        for header, record in self.appdata_record.items():
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
            # record_avg_trip_time = (
            #     record_total_trip_time / max(record_total_trip_count, 1)
            # )
            # print(
            #     '{}:{{ sum:{}s, num:{}, avg:{}s, max:{}s, min:{}s}}'.format(
            #         header.id,
            #         record_total_trip_time,
            #         record_total_trip_count,
            #         record_avg_trip_time,
            #         record_max_trip_time,
            #         record_min_trip_time,
            #     )
            # )
            sim_total_trip_time += record_total_trip_time
            sim_total_trip_count += record_total_trip_count
            sim_min_trip_time = sim_min_trip_time if sim_min_trip_time < record_min_trip_time else record_min_trip_time
            sim_max_trip_time = sim_max_trip_time if sim_max_trip_time > record_max_trip_time else record_max_trip_time

        sim_avg_trip_time = sim_total_trip_time/max(sim_total_trip_count, 1)
        print("Average Trip Time: {}s".format(sim_avg_trip_time))
        print("Maximum Trip Time: {}s".format(sim_max_trip_time))
        print("Minimum Trip Time: {}s".format(sim_min_trip_time))

    def BaseStationAppdataTXQReport(self):
        # time waited of appdata in transmit queue
        sim_max_txq_time = float('-inf')
        sim_min_txq_time = float('inf')
        sim_total_txq_time = 0
        sim_total_txq_count = 0
        sim_avg_txq_time = 0

        for header, record in self.appdata_record.items():
            # time waited of appdata in transmit queue
            record_max_txq_time = float('-inf')
            record_min_txq_time = float('inf')
            record_total_txq_time = 0
            record_total_txq_count = 0
            for bs in nm.BASE_STATION_CONTROLLER:
                serial = bs.serial
                if(record.time_bs_txq_enter[serial] * record.time_bs_txq_exit[serial] > 0):
                    txq_time = (
                        record.time_bs_txq_exit[serial] -
                        record.time_bs_txq_enter[serial]
                    )
                    record_total_txq_count += 1
                    record_total_txq_time += txq_time
                    record_max_txq_time = record_max_txq_time if record_max_txq_time > txq_time else txq_time
                    record_min_txq_time = record_min_txq_time if record_min_txq_time < txq_time else txq_time
            # record_avg_txq_time = (
            #   record_total_txq_time/max(record_total_txq_count,1)
            # )
            # print(
            #     '{}:{{ sum:{}s, num:{}, avg:{}s, max:{}s, min:{}s}}'.format(
            #         header.id,
            #         record_total_txq_time,
            #         record_total_txq_count,
            #         record_avg_txq_time,
            #         record_max_txq_time,
            #         record_min_txq_time,
            #     )
            # )
            sim_total_txq_time += record_total_txq_time
            sim_total_txq_count += record_total_txq_count
            sim_max_txq_time = sim_max_txq_time if sim_max_txq_time > record_max_txq_time else record_max_txq_time
            sim_min_txq_time = sim_min_txq_time if sim_min_txq_time < record_min_txq_time else record_min_txq_time

        sim_avg_txq_time = (
            sim_total_txq_time / max(sim_total_txq_count, 1)
        )
        print("Average TXQ Time:{}s".format(sim_avg_txq_time))
        print("Maximum TXQ Time:{}s".format(sim_max_txq_time))
        print("Minimum TXQ Time:{}s".format(sim_min_txq_time))

    def BaseStationAppdataTXReport(self):
        # time waited of appdata in transmit queue
        sim_max_tx_time = float('-inf')
        sim_min_tx_time = float('inf')
        sim_total_tx_time = 0
        sim_total_tx_count = 0
        sim_avg_tx_time = 0

        for header, record in self.appdata_record.items():
            # time waited of appdata in transmit queue
            record_max_tx_time = float('-inf')
            record_min_tx_time = float('inf')
            record_total_tx_time = 0
            record_total_tx_count = 0
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
            # record_avg_tx_time = (
            #   record_total_tx_time/max(record_total_tx_count,1)
            # )
            # print(
            #     '{}:{{ sum:{}s, num:{}, avg:{}s, max:{}s, min:{}s}}'.format(
            #         header.id,
            #         record_total_tx_time,
            #         record_total_tx_count,
            #         record_avg_tx_time,
            #         record_max_tx_time,
            #         record_min_tx_time,
            #     )
            # )
            sim_total_tx_time += record_total_tx_time
            sim_total_tx_count += record_total_tx_count
            sim_max_tx_time = sim_max_tx_time if sim_max_tx_time > record_max_tx_time else record_max_tx_time
            sim_min_tx_time = sim_min_tx_time if sim_min_tx_time < record_min_tx_time else record_min_tx_time

        sim_avg_tx_time = sim_total_tx_time/max(sim_total_tx_count, 1)
        print("Average TX Time:{}s".format(sim_avg_tx_time))
        print("Maximum TX Time:{}s".format(sim_max_tx_time))
        print("Minimum TX Time:{}s".format(sim_min_tx_time))


STATISTIC_RECORDER = StatisticRecorder()
