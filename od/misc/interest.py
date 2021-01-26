from od.network.types import ResourceAllocatorType


class InterestConfig:
    def __init__(self, res_alloc_type: ResourceAllocatorType, req_rsu: bool, traffic_scale: float, rng_seed=132342421):
        self.res_alloc_type = res_alloc_type
        self.req_rsu = req_rsu
        self.traffic_scale = traffic_scale
        self.rng_seed = rng_seed

    def __str__(self):
        return (
            "res_alloc_type({}) req_rsu({}) traffic_scale({})".format(
                self.res_alloc_type.name,
                self.req_rsu,
                self.traffic_scale
            )
        )
