from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.view import DisplayStatistics
from multiprocessing import Process
from threading import Thread
from datetime import datetime
import single

start_time = None
end_time = None
if __name__ == "__main__":
    start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # for res_alloc_type in [ResourceAllocatorType.OMA]:
    #     for rsu in [False]:
    #         for poisson in [1]:
    #             process = []
    #             for seed in [13232421]:
    # for res_alloc_type in ResourceAllocatorType:
    #    for rsu in [False, True]:
    #        for poisson in [3,4,5]:
    #            for seed in [13232421, 102948123, 4419883, 5157253]:
    for res_alloc_type in [ResourceAllocatorType.NOMA_OPT]:
        for rsu in [False, True]:
            process = []
            for poisson in [1, 2, 3, 4, 5]:
                for seed in [13232421, 102948123, 4419883, 5157253]:
                    process.append(
                        Process(
                            target=single.main,
                            args=(
                                InterestConfig(
                                    res_alloc_type,
                                    rsu,
                                    poisson,
                                    seed
                                ),
                            )
                        )
                    )
                    process[-1].start()
            for p in process:
                p.join()
    end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("Start at: " + start_time)
    print("End at: " + end_time)
