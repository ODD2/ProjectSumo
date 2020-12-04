from globs import SUMO_SIM_INFO


class AppdataStatistic:
    def __init__(self):
        self.total_trans_time = 0
        self.total_trans_count = 0
        self.min_trans_time = float('inf')
        self.max_trans_time = float('-inf')


class StatisticRecorder:
    def __init__(self):
        self.appdata_statistics = {}

    def VehicleReceivedIntactAppdata(self, appdata_header, vehicle):
        if(appdata_header not in self.appdata_statistics):
            self.appdata_statistics[appdata_header] = AppdataStatistic()

        trans_time = SUMO_SIM_INFO.time - appdata_header.at
        statistic = self.appdata_statistics[appdata_header]
        statistic.total_trans_count += 1
        statistic.total_trans_time += trans_time
        statistic.min_trans_time = trans_time if trans_time < statistic.min_trans_time else statistic.min_trans_time
        statistic.max_trans_time = trans_time if trans_time > statistic.max_trans_time else statistic.max_trans_time

    def VehicleRecevedIntactAppdataReport(self):
        sim_max_trans_time = 0
        sim_min_trans_time = 0
        sim_total_trans_time = 0
        sim_total_trans_count = 0
        for appdata_header, appdata_stat in self.appdata_statistics.items():
            print(
                '{}: ttime({}),tcount({}),avgtime({})'.format(
                    appdata_header,
                    appdata_stat.total_trans_time,
                    appdata_stat.total_trans_count,
                    appdata_stat.total_trans_time/appdata_stat.total_trans_count
                )
            )

            sim_min_trans_time = appdata_stat.min_trans_time if appdata_stat.min_trans_time < sim_min_trans_time else sim_min_trans_time
            sim_max_trans_time = appdata_stat.max_trans_time if appdata_stat.max_trans_time > sim_max_trans_time else sim_max_trans_time
            sim_total_trans_time += appdata_stat.total_trans_time
            sim_total_trans_count += appdata_stat.total_trans_count

        print("Maximum Transition Time: {}".format(sim_max_trans_time))
        print("Minimum Transition Time: {}".format(sim_min_trans_time))
        print(
            "Average Transition Time: {}".format(
                sim_total_trans_time/sim_total_trans_count
            )
        )


STATISTIC_RECORDER = StatisticRecorder()
