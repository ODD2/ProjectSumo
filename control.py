from od.misc.interest import InterestConfig
from od.network.types import ResourceAllocatorType
from od.view import DisplayStatistics
import osm


if __name__ == "__main__":
    statistics = []
    for res_alloc_type in ResourceAllocatorType:
        for rsu in [False, True]:
            for poisson in [1, 10, 25, 50]:
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
