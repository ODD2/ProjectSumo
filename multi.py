from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.env.config import ROOT_DIR
from od.view import DisplayStatistics
from multiprocessing import Process, Semaphore
from datetime import datetime
from time import sleep
from os import path
import single

RUN_MISS_ONLY = True


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
            "{} -> {}".format(
                self.process.pid,
                self.weight_conf.interest_config
            )
        )

    def getPid(self):
        return self.process.pid

    def CheckResult(self):
        return path.isfile(ROOT_DIR + self.weight_conf.interest_config.folder())

    def __repr__(self):
        return str(self.weight_conf.interest_config)

    def __str__(self):
        return str(self.weight_conf.interest_config)


def Worker(s: Semaphore, target, args):
    try:
        target(*args)
    except Exception as e:
        print("Worker Exception:{}".format(e))
    s.release()


def ParallelSimulationManager(weight_intconfs, limit):
    s = Semaphore(0)
    weight_process_list = []
    with open("scheme_fail_report.txt", "w") as scheme_fail_report:
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
                            # weight_intconfs.append(wp.weight_conf)
                            time_text = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                            scheme_fail_report.write("[{}]{}\n".format(time_text, wp))
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
    beg_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    weight_intconfs = []
    for qos_re_class in [True, False]:
        for res_alloc_type in [ResourceAllocatorType.NOMA_OPT]:
            for rsu in [False, True]:
                for traffic_scale in [i/10 for i in range(7, 13, 1)]:
                    for seed in range(10):
                        config = InterestConfig(
                            qos_re_class,
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
    print("Start at: " + beg_time)
    print("End at: " + end_time)
