from numpy import random
from od.env.config import NET_QoS_SG_MAX_MEMBER
from od.social.group import SocialGroup, QoSLevel
from od.social.group.metaclass import SocialGroupConfig
from od.network.types import BaseStationType


class SocialGroupManagerClass:
    def __init__(self):
        self.vehicle_stack = 0
        self.dyn_gen_sg_serial = 0
        self.dyn_gen_sg_vehs = {}
        for _ in range(3):
            self.CreateGeneralSocialGroup()

    def NewVehicleSocialGroupList(self):
        global SocialGroup
        self.vehicle_stack += 1
        if(not NET_QoS_SG_MAX_MEMBER[QoSLevel.GENERAL] == 0 and
           self.vehicle_stack == NET_QoS_SG_MAX_MEMBER[QoSLevel.GENERAL]):
            self.vehicle_stack = 0
            self.CreateGeneralSocialGroup()
        spare_dyn_gen_sg_list = list(
            filter(
                (
                    lambda x: x.dyn == True and
                    x.qos == QoSLevel.GENERAL and
                    self.dyn_gen_sg_vehs[x] < NET_QoS_SG_MAX_MEMBER[QoSLevel.GENERAL]
                ),
                SocialGroup
            )
        )
        dyn_gen_sg = random.choice(spare_dyn_gen_sg_list)
        self.dyn_gen_sg_vehs[dyn_gen_sg] += 1
        return [SocialGroup.CRASH, dyn_gen_sg]
        # return [SocialGroup.CRASH, SocialGroup.RCWS]

    def CreateGeneralSocialGroup(self):
        global SocialGroup
        sg_name = "DYN_SG_{}".format(self.dyn_gen_sg_serial)
        self.dyn_gen_sg_serial += 1
        SocialGroup.Create(
            sg_name,
            SocialGroupConfig(QoSLevel.GENERAL, [BaseStationType.UMA, BaseStationType.UMI], True)
        )
        self.dyn_gen_sg_vehs[getattr(SocialGroup, sg_name)] = 0


SocialGroupManager = SocialGroupManagerClass()
