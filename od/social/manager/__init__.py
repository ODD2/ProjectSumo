from numpy import random
from od.social.group import SocialGroup, QoSLevel
from od.social.group.metaclass import SocialGroupConfig
from od.social.manager.types import DynamicSocialGroupBehaviour
from od.network.types import BaseStationType, NetworkCastType


class SocialGroupManagerClass:
    def __init__(self, dyn_sg_conf):
        self.dyn_sg_conf = dyn_sg_conf
        self.dyn_gen_sg_serial = 0

    def NewVehicleSocialGroupList(self):
        pass

    def CreateGeneralSocialGroup(self):
        global SocialGroup
        sg_name = "DYN_SG_{}".format(self.dyn_gen_sg_serial)
        self.dyn_gen_sg_serial += 1
        SocialGroup.Create(
            sg_name,
            SocialGroupConfig(
                QoSLevel.GENERAL,
                [BaseStationType.UMA, BaseStationType.UMI],
                False,
                True
            )
        )
        self.dyn_gen_sg_vehs[getattr(SocialGroup, sg_name)] = 0


# Dynamic social group manager for Max N Social Groups Scenario.
class MaxGroupSGM(SocialGroupManagerClass):
    def __init__(self, dyn_sg_conf):
        self.super().__init__(dyn_sg_conf)
        for _ in range(MAX_N_MEMBER_PRELOCATE_GROUP_NUM):
            self.CreateGeneralSocialGroup()

    def NewVehicleSocialGroupList(self):
        global SocialGroup
        return [SocialGroup.CRASH, SocialGroup.RCWS, random.choice(SocialGroup)]


# Dynamic social group manager for Max N Members Per Social Group Scenario.
MAX_N_MEMBER_PRELOCATE_GROUP_NUM = 3


class MaxMemberSGM(SocialGroupManagerClass):
    def __init__(self, dyn_sg_conf):
        super().__init__(dyn_sg_conf)
        self.vehicle_stack = 0

        self.dyn_gen_sg_vehs = {}
        for _ in range(MAX_N_MEMBER_PRELOCATE_GROUP_NUM):
            self.CreateGeneralSocialGroup()

    def NewVehicleSocialGroupList(self):
        global SocialGroup
        self.vehicle_stack += 1
        if(not self.dyn_sg_conf == 0 and
           self.vehicle_stack == self.dyn_sg_conf):
            self.vehicle_stack = 0
            self.CreateGeneralSocialGroup()
        spare_dyn_gen_sg_list = list(
            filter(
                (
                    lambda x: x.dyn == True and
                    x.qos == QoSLevel.GENERAL and
                    self.dyn_gen_sg_vehs[x] < self.dyn_sg_conf
                ),
                SocialGroup
            )
        )
        dyn_gen_sg = random.choice(spare_dyn_gen_sg_list)
        self.dyn_gen_sg_vehs[dyn_gen_sg] += 1
        return [SocialGroup.CRASH, SocialGroup.RCWS, dyn_gen_sg]
        # return [SocialGroup.CRASH, SocialGroup.RCWS]


def CreateSocialGroupManager(dyn_sg_behav, dyn_sg_conf):
    if(dyn_sg_behav == DynamicSocialGroupBehaviour.MAX_N_MEMBER):
        return MaxMemberSGM(dyn_sg_conf)
    elif(dyn_sg_behav == DynamicSocialGroupBehaviour.MAX_N_GROUPS):
        return MaxGroupSGM(dyn_sg_conf)
    else:
        raise Exception("Undefined Class for DSGB:{}".format(dyn_sg_behav))
