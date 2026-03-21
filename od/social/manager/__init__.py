"""
od/social/manager/__init__.py - Dynamic social group managers.

Two strategies control how new vehicles are assigned to dynamic GENERAL QoS
social groups at simulation start:

  MaxGroupSGM  (MAX_N_GROUPS behaviour)
      Pre-creates exactly dyn_sg_conf dynamic groups.  Each new vehicle is
      randomly assigned to one of them.

  MaxMemberSGM (MAX_N_MEMBER behaviour)
      Creates a new dynamic group every dyn_sg_conf vehicles.  Each new group
      starts with three pre-allocated groups and a new one is added whenever
      the current groups would exceed the per-group member limit.

Both managers also assign every vehicle to the static CRASH and RCWS groups.
CreateSocialGroupManager() is the factory function used by od/vars.py.
"""
from numpy import random
from od.social.group import SocialGroup, QoSLevel
from od.social.group.metaclass import SocialGroupConfig
from od.social.manager.types import DynamicSocialGroupBehaviour
from od.network.types import BaseStationType, NetworkCastType


class SocialGroupManagerClass:
    """Abstract base for social group managers.

    Attributes:
        dyn_sg_conf:        Configuration integer (meaning depends on subclass).
        dyn_gen_sg_serial:  Counter for naming dynamic groups (DYN_SG_0, …).
        dyn_gen_sg_vehs:    Dict mapping dynamic SocialGroupAttr → member count.
    """
    def __init__(self, dyn_sg_conf):
        self.dyn_sg_conf = dyn_sg_conf
        self.dyn_gen_sg_serial = 0
        self.dyn_gen_sg_vehs = {}

    def NewVehicleSocialGroupList(self):
        """Return the list of SocialGroupAttr instances for a newly joined vehicle.

        Subclasses must override this to implement their assignment strategy.
        """
        pass

    def CreateGeneralSocialGroup(self):
        """Allocate a new dynamic GENERAL QoS social group.

        Creates a new SocialGroupConfig, registers it with SocialGroup.Create(),
        and initialises its member counter in dyn_gen_sg_vehs.
        """
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


class MaxGroupSGM(SocialGroupManagerClass):
    """Social group manager: fixed pool of N dynamic groups.

    Creates exactly dyn_sg_conf dynamic GENERAL groups at initialisation.
    Each new vehicle is randomly assigned to one of them.
    """
    def __init__(self, dyn_sg_conf):
        super().__init__(dyn_sg_conf)
        for _ in range(dyn_sg_conf):
            self.CreateGeneralSocialGroup()

    def NewVehicleSocialGroupList(self):
        global SocialGroup
        return [SocialGroup.CRASH, SocialGroup.RCWS, random.choice([sg for sg in SocialGroup if sg.dyn])]


# Number of dynamic groups pre-created at startup before any vehicles join.
MAX_N_MEMBER_PRELOCATE_GROUP_NUM = 3


class MaxMemberSGM(SocialGroupManagerClass):
    """Social group manager: groups grow by one every N vehicles.

    Starts with MAX_N_MEMBER_PRELOCATE_GROUP_NUM groups.  A new dynamic group
    is created every dyn_sg_conf vehicles so that no group exceeds that member
    limit.  New vehicles are randomly assigned to groups that still have
    capacity.
    """
    def __init__(self, dyn_sg_conf):
        super().__init__(dyn_sg_conf)
        self.vehicle_stack = 0
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
    """Factory: return the correct SocialGroupManagerClass subclass.

    Args:
        dyn_sg_behav: DynamicSocialGroupBehaviour enum value.
        dyn_sg_conf:  Integer configuration (max members or max groups).

    Returns:
        A MaxMemberSGM or MaxGroupSGM instance.

    Raises:
        Exception if dyn_sg_behav is not a recognised value.
    """
    if(dyn_sg_behav == DynamicSocialGroupBehaviour.MAX_N_MEMBER):
        return MaxMemberSGM(dyn_sg_conf)
    elif(dyn_sg_behav == DynamicSocialGroupBehaviour.MAX_N_GROUPS):
        return MaxGroupSGM(dyn_sg_conf)
    else:
        raise Exception("Undefined Class for DSGB:{}".format(dyn_sg_behav))
