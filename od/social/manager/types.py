"""
od/social/manager/types.py - Dynamic social group behaviour strategy enum.
"""
from enum import IntEnum


class DynamicSocialGroupBehaviour(IntEnum):
    """Strategy for assigning vehicles to dynamic GENERAL QoS social groups.

    Attributes:
        MAX_N_MEMBER: Limit the number of vehicles per group; create new groups
                      as needed to stay within the limit.
        MAX_N_GROUPS: Fix the total number of groups; distribute vehicles
                      randomly among them.
    """
    MAX_N_MEMBER = 0,
    MAX_N_GROUPS = 1,
