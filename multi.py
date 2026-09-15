"""
multi.py - Parallel simulation manager.

Generates a grid of InterestConfig scenarios (allocator types, RSU modes,
QoS flags, traffic densities, RNG seeds, and dynamic social-group
behaviour/config) and schedules them as separate OS processes.  A weighted
memory model limits the number of concurrent processes so that total RAM
usage stays within a configurable budget.

Usage:
    python multi.py

Results are written to data/<scenario_path>/report.pickle.
Failed scenarios are recorded in scheme_fail_report.txt.
"""
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
    """Pairs an InterestConfig with a relative memory-cost estimate.

    The weight is proportional to the expected memory footprint of the
    simulation, taking into account traffic density, RSU presence, and
    allocator type.  Heavier configurations are scheduled first so that
    lighter ones can fill the remaining budget at the end.
    """

    def __init__(self, interest_config):
        self.interest_config = interest_config
        self.weight = (4 / 1.4 * interest_config.traffic_scale)
        self.weight *= 1.2 if interest_config.req_rsu else 1
        self.weight *= 1 if interest_config.res_alloc_type == ResourceAllocatorType.OMA else 1.5
        self.weight /= SYS_TOTAL_MEM
        self.weight *= 100


class WeightProcess:
    """Wraps an mp.Process together with its WeightInterestConfig.

    Provides helpers to start the process, look up its PID, and verify
    whether the simulation produced a result file after it exits.
    """

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
    """Process target that runs a simulation and releases the semaphore when done.

    Catches any exception so that a single failed run does not crash the
    whole batch; the missing report file will be logged as a failure.
    """
    try:
        target(*args)
    except Exception as e:
        print("Worker Exception:{}".format(e))
    s.release()


def ParallelSimulationManager():
    """Schedule and execute all weighted simulation configurations in parallel.

    Processes are launched greedily: heaviest configurations first, then the
    lightest, so the memory budget (VALID_MEMORY) is consumed as efficiently
    as possible.  When no slots are left the manager blocks on the semaphore
    until a process finishes, reclaims its memory weight, and resumes
    scheduling.  Configurations whose report.pickle is missing after the
    process exits are written to scheme_fail_report.txt.
    """
    global VALID_MEMORY, LIMIT, WEIGHT_INTCONFS
    # begin memory monitor for accurate memory estimation
    # semaphore a worker releases when its simulation finishes
    s = mp.Semaphore(0)
    WEIGHT_INTCONFS.sort(key=lambda x: x.weight, reverse=True)
    weight_process_list = []
    with open("scheme_fail_report.txt", "w") as scheme_fail_report:
        while True:
            # start simulations to drain valid memory space.
            # direction 0 takes the heaviest remaining config (front of the
            # sorted list), -1 the lightest (back), to fill leftover budget.
            for direction in [0, -1]:
                while (len(WEIGHT_INTCONFS) > 0 and VALID_MEMORY > WEIGHT_INTCONFS[direction].weight):
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
                    if (not RUN_MISS_ONLY or not weight_process.CheckResult()):
                        weight_process.Start()
                        weight_process_list.append(weight_process)
                        VALID_MEMORY -= WEIGHT_INTCONFS[direction].weight
                    WEIGHT_INTCONFS = WEIGHT_INTCONFS[1:] if direction == 0 else WEIGHT_INTCONFS[:-1]

            # if there're no remaining interest configs, begin to wait all process to end.
            if (len(WEIGHT_INTCONFS) == 0):
                break
            # wait until at least one simulation ends
            s.acquire()
            # remove terminated simulations
            remain_weight_process_list = []
            for wp in weight_process_list:
                if (not wp.process.is_alive()):
                    # process ended: log it as failed if no report.pickle was produced.
                    if (not wp.CheckResult()):
                        # WEIGHT_INTCONFS.append(wp.weight_conf)
                        time_text = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        scheme_fail_report.write("[{}]{}\n".format(time_text, wp))
                    # reclaim memory weight regardless of success/failure
                    VALID_MEMORY += wp.weight_conf.weight
                    # join to prevent a zombie process
                    wp.process.join()
                else:
                    remain_weight_process_list.append(wp)
            weight_process_list = remain_weight_process_list
        # wait for all the simulation process to join
        for wp in weight_process_list:
            wp.process.join()


def SimulationSettings(fn):
    """Decorator that expands a factory function over the full scenario grid.

    Runs two grids and concatenates the results: one sweeping allocator type,
    RSU mode, QoS reclassification flag, traffic scale and seed (with social
    group settings fixed); another sweeping social-group behaviour and config
    (with allocator/RSU/traffic fixed).  Calls *fn* once per combination.
    """
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


@SimulationSettings
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
