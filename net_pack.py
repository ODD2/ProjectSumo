from globs import SocialGroup
from net_app import AppData


class NetworkPackage:
    def __init__(self,
                 src, dest,
                 social_group: SocialGroup,
                 bits: int,
                 appdatas: [AppData],
                 trans_ts: int,
                 offset_ts: int):
        self.src = src
        self.dest = dest
        self.social_group = social_group
        self.bits = bits
        self.appdatas = appdatas
        self.trans_ts = trans_ts
        self.offset_ts = offset_ts
