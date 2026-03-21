"""
od/social/group/types.py - Quality-of-Service level enumeration.
"""
from enum import IntEnum


class QoSLevel(IntEnum):
    """QoS priority levels used to classify social group traffic.

    Lower integer value = higher priority.

    Attributes:
        CRITICAL: Time-sensitive traffic (e.g. crash alerts).
                  Uses wider subcarrier spacing (2 × SCS) on UMI cells and is
                  given scheduling priority over GENERAL traffic.
        GENERAL:  Best-effort traffic (e.g. road condition warnings).
    """
    CRITICAL = 0
    GENERAL = 1
