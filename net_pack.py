
from globs import SociatyGroup


class NetworkTransmitRequest:
    def __init__(self, name: str, owner, size: int, cqi: float, sinr: float, social_group: SociatyGroup):
        self.name = name
        self.owner = owner
        self.bits = size
        self.cqi = cqi
        self.sinr = sinr
        self.social_group = social_group


class NetworkTransmitResponse:
    def __init__(self, status: bool, responder, name: str,  size: int,  social_group: SociatyGroup):
        self.status = status
        self.responder = responder
        self.name = name
        self.bits = size
        self.social_group = social_group
