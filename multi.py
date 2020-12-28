from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.view import DisplayStatistics
from multiprocessing import Process
import single


if __name__ == "__main__":
    process = []
    for res_alloc_type in ResourceAllocatorType:
        for rsu in [False, True]:
            for poisson in [1, 5]:
                # for poisson in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
                process.append(
                    Process(
                        target=single.main,
                        args=(
                            InterestConfig(
                                res_alloc_type,
                                rsu,
                                poisson
                            ),
                        )
                    )
                )
                process[-1].start()
    for p in process:
        p.join()
