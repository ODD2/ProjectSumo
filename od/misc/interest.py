from od.network.types import ResourceAllocatorType


class InterestConfig:
    def __init__(self, qos_re_class: bool, res_alloc_type: ResourceAllocatorType, req_rsu: bool, traffic_scale: float, rng_seed=132342421):
        self.res_alloc_type = res_alloc_type
        self.req_rsu = req_rsu
        self.traffic_scale = traffic_scale
        self.rng_seed = rng_seed
        self.qos_re_class = qos_re_class

    def path_repr(self):
        return [
            "yQoS" if self.qos_re_class else "nQoS",
            "yRSU" if self.req_rsu else "nRSU",
            self.res_alloc_type.name,
            "D{}".format(self.traffic_scale),
            "S{}".format(self.rng_seed)
        ]

    def __str__(self):
        return "-".join(self.path_repr())

    def folder(self):
        return "/".join(self.path_repr()) + "/"

    def folder_legacy(self):
        return "/".join([
            "yQoS" if self.qos_re_class else "nQoS",
            str(self.rng_seed),
            "res_alloc_type({}) req_rsu({}) traffic_scale({})".format(
                self.res_alloc_type.name,
                self.req_rsu,
                self.traffic_scale
            )
        ]) + "/"
