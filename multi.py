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
VALID_MEMORY = 0
LIMIT = 70
WEIGHT_INTCONFS = []


class WeightInterestConfig:
    def __init__(self, interest_config):
        self.interest_config = interest_config
        self.weight = (10 / 1.4 * interest_config.traffic_scale)
        self.weight *= 1.2 if interest_config.req_rsu else 1
        self.weight *= 1.5 if interest_config.res_alloc_type == ResourceAllocatorType.NOMA_OPT else 1
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


def MemoryMonitor():
    global VALID_MEMORY, LIMIT
    VALID_MEMORY = LIMIT - vm().percent
    sleep(300)


def ParallelSimulationManager():
    global VALID_MEMORY, LIMIT, WEIGHT_INTCONFS
    if((LIMIT - vm().percent) < 0):
        print("Startup Memory Insufficinet")
        return
    # begin memory monitor for accurate memory estimation
    mm = Thread(target=MemoryMonitor)
    mm.start()
    # wait for memory to update
    sleep(1)
    # process manager
    s = mp.Semaphore(0)
    weight_process_list = []
    with open("scheme_fail_report.txt", "w") as scheme_fail_report:
        while(True):
            remain_weight_intconfs = []
            # arrange weighted interest configs to let heavier ones to have higher precedence.
            WEIGHT_INTCONFS.sort(key=lambda x: x.weight, reverse=True)
            # arrange resource to interest configs accroding to its weight
            for weight_intconf in WEIGHT_INTCONFS:
                if(weight_intconf.weight < VALID_MEMORY):
                    weight_process = WeightProcess(
                        weight_intconf,
                        mp.Process(
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
                        VALID_MEMORY -= weight_intconf.weight
                else:
                    remain_weight_intconfs.append(weight_intconf)

            # remove allocated configs.
            WEIGHT_INTCONFS = remain_weight_intconfs

            # if there're no remaining interest configs, begin to wait all process to end.
            if(len(WEIGHT_INTCONFS) == 0):
                break

            # wait untill enough resource for the most required config.
            while(VALID_MEMORY < WEIGHT_INTCONFS[0].weight):
                # check which process(es) ended
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
                MemoryMonitor()
        # wait for all the simulation process to join
        for wp in weight_process_list:
            wp.process.join()
        # wait for the memory monitor thread to join
        mm.join()


def SimulationSettings(fn):
    def wrapper(**args):
        result = []
        # for qos_re_class in [True, False]:
        #     for res_alloc_type in [ResourceAllocatorType.NOMA_OPT, ResourceAllocatorType.NOMA_APR]:
        #         for rsu in [False, True]:
        #             for traffic_scale in [i / 10 for i in range(7, 15, 1)]:
        #                 for seed in [i + 11 for i in range(10)]:
        # for dyn_sg_conf in [(i + 2) * 5 for i in range(5)]:
        #     for res_alloc_type in [ResourceAllocatorType.NOMA_APR]:
        #         for rsu in [True, False]:
        #             for qos_re_class in [True, False] if rsu == True else [False]:
        #                 for traffic_scale in [i / 10 for i in range(10, 15, 1)]:
        #                     for seed in [i + 1 for i in range(9)]:
        for dyn_sg_conf in [(i * 2) + 5 for i in range(5)]:
            for res_alloc_type in [ResourceAllocatorType.NOMA_APR]:
                for rsu in [True]:
                    for qos_re_class in [True, False] if rsu == True else [False]:
                        for traffic_scale in [1.4]:
                            for seed in [i + 1 for i in range(9)]:
                                result.append(
                                    fn(
                                        **args,
                                        dyn_sg_behav=DynamicSocialGroupBehaviour.MAX_N_GROUPS,
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
