# SocialGroup and QOS priority(Lower value has higher priority, 0 is the lowest value.)
from enum import IntEnum
from od.social.group.metaclass import SocialGroupMeta, SocialGroupConfig
from od.social.group.types import *
from od.network.types import BaseStationType
from od.env.station import BS_PRESET


class SocialGroup(metaclass=SocialGroupMeta):
    CRASH = SocialGroupConfig(
        QoSLevel.CRITICAL,
        [
            BaseStationType.UMI,
            BaseStationType.UMA
        ],
        False,
        False,
    )
    RCWS = SocialGroupConfig(
        QoSLevel.GENERAL,
        [
            BaseStationType.UMA,
            BaseStationType.UMI
        ],
        True,
        False,
    )

# SocialGroup = SocialGroupMeta(
#     "SocialGroup",
#     (),
#     {
#         "CRASH": SocialGroupConfig(QoSLevel.CRITICAL, [BaseStationType.UMI, BaseStationType.UMA], False),
#         "RCWS": SocialGroupConfig(QoSLevel.GENERAL, [BaseStationType.UMA, BaseStationType.UMI], False)
#     }
# )
