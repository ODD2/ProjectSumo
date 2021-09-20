from od.social import SocialGroup
from od.env.config import NET_QoS_SG_MAX_MEMBER


# Dummy Broadcast object class
class BroadcastObject():
    name = 'broadcast'


# Dummy Multicast object class
class MulticastObject():
    name = 'multicast'


# Dummy Unicast object class
class UnicastObject():
    name = 'unicast'


# Dummy Casting object Selector
def CastObject(social_group: SocialGroup):
    if(NET_QoS_SG_MAX_MEMBER[social_group.qos] == 0):
        return BroadcastObject
    elif(NET_QoS_SG_MAX_MEMBER[social_group.qos] == 2):
        return UnicastObject
    else:
        return MulticastObject
