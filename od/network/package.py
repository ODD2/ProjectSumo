from od.social import SocialGroup
from od.network.application import AppData


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

    def __str__(self):
        return "NetworkPackage({}>{},{}-Q{},{}b,{}o+{}t,[{}])".format(
            self.src.name,
            self.dest.name,
            self.social_group.fname.lower(),
            self.social_group.qos,
            self.bits,
            self.offset_ts,
            self.trans_ts,
            ",".join([str(data) for data in self.appdatas])
        )
