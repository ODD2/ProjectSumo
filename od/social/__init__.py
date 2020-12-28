# SocialGroup and QOS priority(Lower value has higher priority, 0 is the lowest value.)
from .metaclass import SocialGroupMeta, SocialGroupConfig
from od.network.types import BaseStationType


class SocialGroup(metaclass=SocialGroupMeta):
    CRITICAL = SocialGroupConfig(0, [BaseStationType.UMI, BaseStationType.UMA])
    GENERAL = SocialGroupConfig(1, [BaseStationType.UMA, BaseStationType.UMI])
