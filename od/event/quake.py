from od.social import SocialGroup
from od.event import SumoSimEvents
import od.vars as GV


class EarthQuake(SumoSimEvents):
    def __init__(self, ofs_ss, dur_ss):
        super().__init__(ofs_ss, dur_ss)
        # the modifier of ciritical social group net requests.
        self.sg_crit_net_req_mod = 5

    def Begin(self):
        GV.NET_SG_RND_REQ_MOD[SocialGroup.CRASH] *= self.sg_crit_net_req_mod

    def End(self):
        GV.NET_SG_RND_REQ_MOD[SocialGroup.CRASH] /= self.sg_crit_net_req_mod
