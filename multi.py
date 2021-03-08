from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.view import DisplayStatistics
from multiprocessing import Process, Semaphore
from threading import Thread
from datetime import datetime
import single
import numpy as np


class WeightInterestConfig:
    def __init__(self, weight, interest_config):
        self.weight = weight
        self.interest_config = interest_config


class WeightProcess:
    def __init__(self, weight, process: Process):
        self.weight = weight
        self.process = process
        self.process.start()


def Worker(s: Semaphore, target, args):
    target(*args)
    s.release()


def ParallelSimulationManager(weight_intconfs, limit):
    s = Semaphore(0)
    min_i = 0
    max_i = len(weight_intconfs) - 1
    weight_intconfs.sort(key=lambda x: x.weight, reverse=True)
    weight_process = []
    while(True):
        remain_weight_intconfs = []

        for weight_intconf in weight_intconfs:
            if(weight_intconf.weight < limit):
                weight_process.append(
                    WeightProcess(
                        weight_intconf.weight,
                        Process(
                            target=Worker,
                            args=(
                                s,
                                single.main,
                                (weight_intconf.interest_config,)
                            )
                        )
                    )
                )
                limit -= weight_intconf.weight
            else:
                remain_weight_intconfs.append(weight_intconf)

        if(len(remain_weight_intconfs) == 0):
            break

        weight_intconfs = remain_weight_intconfs

        while(limit < weight_intconfs[0].weight):
            s.acquire()
            i = 0
            while(i < len(weight_process)):
                if(not weight_process[i].process.is_alive()):
                    limit += weight_process[i].weight
                    weight_process = weight_process[: i] + weight_process[i+1:]
                else:
                    i += 1

    for wp in weight_process:
        wp.process.join()


if __name__ == "__main__":
    start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    weight_intconfs = []
    # for res_alloc_type in ResourceAllocatorType:
    #     for rsu in [False, True]:
    #         for traffic_scale in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    #             for seed in range(1):
    #                 weight = (3**traffic_scale)
    #                 weight *= 1.3 if rsu else 1
    #                 weight *= 1.5 if res_alloc_type == ResourceAllocatorType.NOMA_OPT else 1
    #                 config = InterestConfig(
    #                     res_alloc_type,
    #                     rsu,
    #                     traffic_scale,
    #                     seed
    #                 )
    #                 weight_intconfs.append(
    #                     WeightInterestConfig(
    #                         weight,
    #                         config
    #                     )
    #                 )

    # weight_intconfs.append(
    #     WeightInterestConfig(
    #         0,
    #         InterestConfig(ResourceAllocatorType.OMA, True, 0.5, 123456)
    #     )
    # )
    # weight_intconfs.append(
    #     WeightInterestConfig(
    #         0,
    #         InterestConfig(ResourceAllocatorType.NOMA_OPT, True, 0.5, 123456)
    #     )
    # )
    weight_intconfs.append(
        WeightInterestConfig(
            0,
            InterestConfig(ResourceAllocatorType.NOMA_OPT, True, 0.5, 0)
        )
    )
    weight_intconfs.append(
        WeightInterestConfig(
            0,
            InterestConfig(ResourceAllocatorType.NOMA_OPT, False, 0.9, 0)
        )
    )

    ParallelSimulationManager(weight_intconfs, 80)
    end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("Start at: " + start_time)
    print("End at: " + end_time)
