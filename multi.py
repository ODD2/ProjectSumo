from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.config import ROOT_DIR
from od.view import DisplayStatistics
from multiprocessing import Process, Semaphore
from threading import Thread
from datetime import datetime
from time import sleep
from os import path
import single
import numpy as np


class WeightInterestConfig:
    def __init__(self,  interest_config):
        self.interest_config = interest_config
        self.weight = (3 ** interest_config.traffic_scale)
        self.weight *= 1.2 if interest_config.req_rsu else 1
        self.weight *= 1.5 if interest_config.res_alloc_type == ResourceAllocatorType.NOMA_OPT else 1


class WeightProcess:
    def __init__(self, weight_conf, process: Process):
        self.weight_conf = weight_conf
        self.process = process

    def Start(self):
        self.process.start()
        print(
            "{} -> {} seed({})".format(
                self.process.pid,
                str(self.weight_conf.interest_config),
                self.weight_conf.interest_config.rng_seed
            )
        )

    def getPid(self):
        return self.process.pid

    def CheckResult(self):
        interest = self.weight_conf.interest_config
        return path.isfile(ROOT_DIR + "{}/{}/report.pickle".format(interest.rng_seed, str(interest)))


def Worker(s: Semaphore, target, args):
    target(*args)
    s.release()


def ParallelSimulationManager(weight_intconfs, limit):
    s = Semaphore(0)
    weight_process_list = []

    while(True):
        remain_weight_intconfs = []
        # arrange weighted interest configs to let heavier ones to have higher precedence.
        weight_intconfs.sort(key=lambda x: x.weight, reverse=True)
        # arrange resource to interest configs accroding to its weight
        for weight_intconf in weight_intconfs:
            if(weight_intconf.weight < limit):
                weight_process = WeightProcess(
                    weight_intconf,
                    Process(
                        target=Worker,
                        args=(
                            s,
                            single.main,
                            (weight_intconf.interest_config,)
                        )
                    )
                )
                if(not RUN_MISS_ONLY or not weight_process.CheckResult()):
                    weight_process.Start()
                    weight_process_list.append(weight_process)
                    limit -= weight_intconf.weight
                    sleep(2)
            else:
                remain_weight_intconfs.append(weight_intconf)
        # if there're no remaining interest configs, begin to wait all process to end.
        if(len(remain_weight_intconfs) == 0):
            break

        # remove allocated configs.
        weight_intconfs = remain_weight_intconfs

        # wait untill enough resource for the most required config.
        while(limit < weight_intconfs[0].weight):
            # wait for working process to end
            s.acquire()
            # check which process(es) ended
            remain_weight_process_list = []
            for wp in weight_process_list:
                if(not wp.process.is_alive()):
                    # if process is not alive, meaning it has ended, do result check.
                    if(not wp.CheckResult()):
                        weight_intconfs.append(wp.weight_conf)
                    # release resource limit
                    limit += wp.weight_conf.weight
                    # join process to prevent existance of zombie process
                    wp.process.join()
                else:
                    remain_weight_process_list.append(wp)
            weight_process_list = remain_weight_process_list

    for wp in weight_process_list:
        wp.process.join()


if __name__ == "__main__":
    start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    weight_intconfs = []
    for res_alloc_type in [ResourceAllocatorType.NOMA_OPT]:
        for rsu in [False, True]:
            for traffic_scale in [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]:
                for seed in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
                    config = InterestConfig(
                        res_alloc_type,
                        rsu,
                        traffic_scale,
                        seed
                    )
                    weight_intconfs.append(
                        WeightInterestConfig(
                            config
                        )
                    )
    ParallelSimulationManager(weight_intconfs, 100)
    end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("Start at: " + start_time)
    print("End at: " + end_time)
