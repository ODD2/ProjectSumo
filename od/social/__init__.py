# SocialGroup and QOS priority(Lower value has higher priority, 0 is the lowest value.)
from .metaclass import SocialGroupMeta

class SocialGroup(metaclass=SocialGroupMeta):
    CRITICAL = 0
    GENERAL = 1
