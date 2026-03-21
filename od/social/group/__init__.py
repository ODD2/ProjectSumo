"""
od/social/group/__init__.py - Social group definitions.

SocialGroup uses the SocialGroupMeta metaclass so that each class attribute
declared as a SocialGroupConfig is automatically converted into a
SocialGroupAttr with a unique gid.  New groups can be added at runtime via
SocialGroup.Create().

Predefined groups:
  CRASH – CRITICAL QoS, vehicle-originated emergency/collision data.
           Prefers UMI for low-latency delivery.
  RCWS  – GENERAL QoS, road condition warning data broadcast by UMAs.
           Reader-only (vehicles only receive; data is injected by the network).
"""
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
