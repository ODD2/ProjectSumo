from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.view import DisplayStatistics
from multiprocessing import Process
import single


if __name__ == "__main__":
    for seed in [13232421, 102948123, 4419883]:
        # for seed in [13232421]:
        # for res_alloc_type in ResourceAllocatorType:
        for res_alloc_type in [ResourceAllocatorType.NOMA_OPT]:
            for rsu in [False, True]:
                # for rsu in [True]:
                process = []
                for poisson in [3, 4, 5, 6, 7, 8, 9, 10]:
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
