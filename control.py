from od.misc.interest import InterestConfig
from od.view import DisplayStatistics
import osm


if __name__ == "__main__":
    statistics = []
    for oma_only in [False, True]:
        for rsu in [False, True]:
            for poisson in [1, 10, 25, 50]:
                statistics.append(
                    osm.main(InterestConfig(oma_only, rsu, poisson))
                )
    DisplayStatistics(statistics)
