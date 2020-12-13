from od.misc.interest import InterestConfig
import osm


if __name__ == "__main__":
    for rsu in [False, True]:
        for poisson in [1, 10, 25]:
            osm.main(InterestConfig(False, rsu, poisson))
