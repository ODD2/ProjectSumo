from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.social.manager import DynamicSocialGroupBehaviour
from od.env.config import ROOT_DIR
from od.view import DisplayStatistics
from datetime import datetime
from time import sleep
from os import path
from psutil import virtual_memory as vm
import multiprocessing as mp
from threading import Thread
import single

RUN_MISS_ONLY = True
SYS_TOTAL_MEM = vm().total / (1024**3)
LIMIT = 50
VALID_MEMORY = LIMIT
WEIGHT_INTCONFS = []


class WeightInterestConfig:
    def __init__(self, interest_config):
        self.interest_config = interest_config
        self.weight = (4 / 1.4 * interest_config.traffic_scale)
        self.weight *= 1.2 if interest_config.req_rsu else 1
        self.weight *= 1 if interest_config.res_alloc_type == ResourceAllocatorType.OMA else 1.5
        self.weight /= SYS_TOTAL_MEM
        self.weight *= 100


class WeightProcess:
    def __init__(self, weight_conf, process: mp.Process):
        self.weight_conf = weight_conf
        self.process = process

    def Start(self):
        self.process.start()
        print(
            "{} -> {}".format(
                self.process.pid,
                self.weight_conf.interest_config
            )
        )

    def getPid(self):
        return self.process.pid

    def CheckResult(self):
        return path.isfile(ROOT_DIR + self.weight_conf.interest_config.folder() + "report.pickle")

    def __repr__(self):
        return str(self.weight_conf.interest_config)

    def __str__(self):
        return str(self.weight_conf.interest_config)


def Worker(s: mp.Semaphore, target, args):
    try:
        target(*args)
    except Exception as e:
        print("Worker Exception:{}".format(e))
    s.release()


def ParallelSimulationManager():
    global VALID_MEMORY, LIMIT, WEIGHT_INTCONFS
    # begin memory monitor for accurate memory estimation
    s = mp.Semaphore(0)
    WEIGHT_INTCONFS.sort(key=lambda x: x.weight, reverse=True)
    weight_process_list = []
    with open("scheme_fail_report.txt", "w") as scheme_fail_report:
        while True:
            # start simulations to drain valid memory space.
            for direction in [0, -1]:
                while(len(WEIGHT_INTCONFS) > 0 and VALID_MEMORY > WEIGHT_INTCONFS[direction].weight):
                    # arrange weighted interest configs to let heavier ones to have higher precedence.
                    weight_process = WeightProcess(
                        WEIGHT_INTCONFS[direction],
                        mp.Process(
                            target=Worker,
                            args=(
                                s,
                                single.main,
                                (WEIGHT_INTCONFS[direction].interest_config,)
                            )
                        )
                    )
                    if(not RUN_MISS_ONLY or not weight_process.CheckResult()):
                        weight_process.Start()
                        weight_process_list.append(weight_process)
                        VALID_MEMORY -= WEIGHT_INTCONFS[direction].weight
                    WEIGHT_INTCONFS = WEIGHT_INTCONFS[1:] if direction == 0 else WEIGHT_INTCONFS[:-1]

            # if there're no remaining interest configs, begin to wait all process to end.
            if(len(WEIGHT_INTCONFS) == 0):
                break
            # wait until at least one simulation ends
            s.acquire()
            # remove terminated simulations
            remain_weight_process_list = []
            for wp in weight_process_list:
                if(not wp.process.is_alive()):
                    # if process is not alive, meaning it has ended, do result check.
                    if(not wp.CheckResult()):
                        # WEIGHT_INTCONFS.append(wp.weight_conf)
                        time_text = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        scheme_fail_report.write("[{}]{}\n".format(time_text, wp))
                        # release resource limit
                    VALID_MEMORY += wp.weight_conf.weight
                    # join process to prevent existance of zombie process
                    wp.process.join()
                else:
                    remain_weight_process_list.append(wp)
            weight_process_list = remain_weight_process_list
        # wait for all the simulation process to join
        for wp in weight_process_list:
            wp.process.join()


def SimulationSettings(fn):
    def wrapper(**args):
        result = []
        seed_range = [i + 1 for i in range(20)]
        traffic_scale_range = [i / 10 for i in range(10, 15, 1)]
        for res_alloc_type in [ResourceAllocatorType.NOMA_OPT, ResourceAllocatorType.NOMA_APR]:
            for rsu in [True, False]:
                for qos_re_class in [True, False] if rsu == True else [False]:
                    for traffic_scale in traffic_scale_range:
                        for seed in seed_range:
                            result.append(
                                fn(
                                    **args,
                                    dyn_sg_behav=DynamicSocialGroupBehaviour.MAX_N_MEMBER,
                                    dyn_sg_conf=20,
                                    qos_re_class=qos_re_class,
                                    res_alloc_type=res_alloc_type,
                                    req_rsu=rsu,
                                    traffic_scale=traffic_scale,
                                    rng_seed=seed
                                )
                            )
        for dyn_sg_behav in DynamicSocialGroupBehaviour:
            for dyn_sg_conf in [(i * 2) + 5 for i in range(5)]:
                for res_alloc_type in [ResourceAllocatorType.NOMA_APR]:
                    for rsu in [True]:
                        for qos_re_class in [True, False] if rsu == True else [False]:
                            for traffic_scale in [1.4]:
                                for seed in seed_range:
                                    result.append(
                                        fn(
                                            **args,
                                            dyn_sg_behav=dyn_sg_behav,
                                            dyn_sg_conf=dyn_sg_conf,
                                            qos_re_class=qos_re_class,
                                            res_alloc_type=res_alloc_type,
                                            req_rsu=rsu,
                                            traffic_scale=traffic_scale,
                                            rng_seed=seed
                                        )
                                    )
        return result
    return wrapper


@ SimulationSettings
def CreateWeightIntConfs(**kargs):
    return WeightInterestConfig(
        InterestConfig(
            **kargs
        )
    )


if __name__ == "__main__":
    mp.set_start_method("forkserver")
    beg_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    WEIGHT_INTCONFS = CreateWeightIntConfs()
    ParallelSimulationManager()
    end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("Start at: " + beg_time)
    print("End at: " + end_time)
