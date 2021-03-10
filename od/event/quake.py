from od.social import SocialGroup
from od.event.base import SumoSimEvent
from od.event.config import SumoSimEventConf
import od.vars as GV


class EarthQuake(SumoSimEvent):
    def __init__(self, config: SumoSimEventConf):
        super().__init__(config)
        # the modifier of ciritical social group net requests.
        self.sg_crit_net_req_mod = 5

    def Begin(self):
        GV.NET_SG_RND_REQ_MOD[SocialGroup.CRASH] *= self.sg_crit_net_req_mod

    def End(self):
        GV.NET_SG_RND_REQ_MOD[SocialGroup.CRASH] /= self.sg_crit_net_req_mod
