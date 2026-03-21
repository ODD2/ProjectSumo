"""
od/misc/interest.py - Scenario configuration container.

InterestConfig bundles every parameter that distinguishes one simulation run
from another.  It is passed to InitializeSimulationContext() and
InitializeSimulationVariables() at startup and is used by multi.py to
generate the scenario grid.
"""
from od.network.types import ResourceAllocatorType
from od.social.manager import DynamicSocialGroupBehaviour


class InterestConfig:
    """Immutable descriptor for a single simulation scenario.

    Attributes:
        dyn_sg_behav:  Dynamic social group behaviour strategy
                       (MAX_N_MEMBER or MAX_N_GROUPS).
        dyn_sg_conf:   Integer configuration value for the strategy
                       (max members per group, or max number of groups).
        qos_re_class:  Whether UMI-received critical data is reclassified
                       as general QoS before forwarding to the UMA.
        res_alloc_type: Downlink resource allocation algorithm
                        (OMA, NOMA_OPT, or NOMA_APR).
        req_rsu:       Whether UMI (roadside unit) small cells are included.
        traffic_scale: SUMO vehicle departure rate multiplier (e.g. 1.4 = 40 %
                       more vehicles than the base scenario).
        rng_seed:      Seed for numpy random and MATLAB RNG for reproducibility.
    """
    def __init__(
        self,
        dyn_sg_behav: DynamicSocialGroupBehaviour,
        dyn_sg_conf: int,
        qos_re_class: bool,
        res_alloc_type: ResourceAllocatorType,
        req_rsu: bool,
        traffic_scale: float,
        rng_seed=132342421
    ):
        self.dyn_sg_behav = dyn_sg_behav
        self.dyn_sg_conf = dyn_sg_conf
        self.res_alloc_type = res_alloc_type
        self.req_rsu = req_rsu
        self.traffic_scale = traffic_scale
        self.rng_seed = rng_seed
        self.qos_re_class = qos_re_class

    def path_repr(self):
        """Return a list of short strings that uniquely identify this config.

        Each element becomes one directory level when constructing the output
        folder path (see folder()).
        """
        return [
            "{}({})".format(self.dyn_sg_behav.name, self.dyn_sg_conf),
            "yQoS" if self.qos_re_class else "nQoS",
            "yRSU" if self.req_rsu else "nRSU",
            self.res_alloc_type.name,
            "D{}".format(self.traffic_scale),
            "S{}".format(self.rng_seed)
        ]

    def __str__(self):
        return "-".join(self.path_repr())

    def folder(self):
        """Return the relative output directory path for this configuration.

        The path is built from path_repr() joined by "/" and terminated with
        a slash so it can be directly concatenated with a base directory.
        """
        return "/".join(self.path_repr()) + "/"

    def folder_legacy(self, version=0):
        if(version == 0):
            return "/".join([
                "yQoS" if self.qos_re_class else "nQoS",
                str(self.rng_seed),
                "res_alloc_type({}) req_rsu({}) traffic_scale({})".format(
                    self.res_alloc_type.name,
                    self.req_rsu,
                    self.traffic_scale
                )
            ]) + "/"
        if(version == 1):
            return "/".join([
                "yQoS" if self.qos_re_class else "nQoS",
                "yRSU" if self.req_rsu else "nRSU",
                self.res_alloc_type.name,
                "D{}".format(self.traffic_scale),
                "S{}".format(self.rng_seed)
            ]) + "/"
