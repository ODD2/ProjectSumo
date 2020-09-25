from globs import SocialGroup


class NetworkPackage:
    def __init__(self, name: str, owner, size: int, social_group: SocialGroup, at: float):
        self.name = name
        self.owner = owner
        self.bits = size
        self.social_group = social_group
        self.at = at


class NetworkTransmitRequest:
    def __init__(self, package: NetworkPackage, cqi: float, sinr: float):
        self.package = package
        self.cqi = cqi
        self.sinr = sinr


class NetworkTransmitResponse:
    def __init__(self, status: bool, sender, package: NetworkPackage, time_slots=0):
        self.status = status
        self.sender = sender
        self.package = package
        self.req_time_slots = time_slots


class PackageProcessing:
    def __init__(self, package: NetworkPackage, opponent, bits: int, tx_ts: int, of_ts: int):
        self.package = package
        self.opponent = opponent
        self.proc_bits = bits
        # transmission time slots
        self.tx_ts = tx_ts
        # offset time slots
        self.of_ts = of_ts
