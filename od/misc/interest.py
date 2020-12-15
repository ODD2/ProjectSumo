from od.network.types import ResourceAllocatorType


class InterestConfig:
    def __init__(self, res_alloc_type: ResourceAllocatorType, req_rsu: bool, appdata_poisson):
        self.res_alloc_type = res_alloc_type
        self.req_rsu = req_rsu
        self.appdata_poisson = appdata_poisson

    def __str__(self):
        return (
            "res_alloc_type({}) req_rsu({}) appdata_poisson({})".format(
                self.res_alloc_type.name,
                self.req_rsu,
                self.appdata_poisson
            )
        )
