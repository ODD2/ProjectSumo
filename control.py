from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.view import DisplayStatistics
import osm


if __name__ == "__main__":
    statistics = []
    for res_alloc_type in ResourceAllocatorType:
        for rsu in [False, True]:
            for poisson in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
                statistics.append(
                    osm.main(
                        InterestConfig(
                            res_alloc_type,
                            rsu,
                            poisson
                        )
                    )
                )
    # DisplayStatistics(statistics)
