"""
od/event/quake.py - Earthquake emergency event.

Simulates a sudden surge in CRITICAL V2X traffic (e.g. simultaneous
crash / emergency alerts from many vehicles) by multiplying the CRITICAL QoS
random request rate modifier by sg_crit_net_req_mod for the event duration.
"""
from od.social.group import QoSLevel, SocialGroup
from od.event.base import SumoSimEvent
from od.event.config import SumoSimEventConf
import od.vars as GV


class EarthQuake(SumoSimEvent):
    """Emergency event that scales up CRITICAL QoS traffic during its duration.

    On Begin(): multiplies GV.NET_QoS_RND_REQ_MOD[CRITICAL] by
                sg_crit_net_req_mod (default 5×).
    On End():   restores the original value by dividing by the same factor.
    """
    def __init__(self, config: SumoSimEventConf):
        super().__init__(config)
        # the modifier of ciritical social group net requests.
        self.sg_crit_net_req_mod = 5

    def Begin(self):
        GV.NET_QoS_RND_REQ_MOD[QoSLevel.CRITICAL] *= self.sg_crit_net_req_mod

    def End(self):
        GV.NET_QoS_RND_REQ_MOD[QoSLevel.CRITICAL] /= self.sg_crit_net_req_mod
