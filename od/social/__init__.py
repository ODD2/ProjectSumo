# SocialGroup and QOS priority(Lower value has higher priority, 0 is the lowest value.)
from enum import IntEnum
from od.social.metaclass import SocialGroupMeta, SocialGroupConfig
from od.network.types import BaseStationType
from od.config.station import BS_PRESET


class QoSLevel(IntEnum):
    CRITICAL = 0
    GENERAL = 1


# class SocialGroup(metaclass=SocialGroupMeta):
#     CRASH = SocialGroupConfig(QoSLevel.CRITICAL, [BaseStationType.UMI, BaseStationType.UMA])
#     RCWS = SocialGroupConfig(QoSLevel.GENERAL, [BaseStationType.UMA, BaseStationType.UMI])

SocialGroup = SocialGroupMeta(
    "SocialGroup",
    (),
    {
        "CRASH": SocialGroupConfig(QoSLevel.CRITICAL, [BaseStationType.UMI, BaseStationType.UMA]),
        "RCWS": SocialGroupConfig(QoSLevel.GENERAL, [BaseStationType.UMA, BaseStationType.UMI])
    }
)
