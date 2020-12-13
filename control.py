from od.misc.interest import InterestConfig
from od.view import DisplayStatistics
import osm


if __name__ == "__main__":
    statistics = []
    for rsu in [False, True]:
        for poisson in [1, 10, 25]:
            statistics.append(osm.main(InterestConfig(False, rsu, poisson)))
    DisplayStatistics(statistics)
