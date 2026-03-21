"""
od/network/package.py - Network transmission unit.

A NetworkPackage bundles one or more AppData fragments that are transmitted
together in a single radio resource allocation.
"""
from typing import List
from od.social.group import SocialGroup
from od.network.appdata import AppData


class NetworkPackage:
    """A single transmission unit carrying application data fragments.

    Attributes:
        src:          Sender (VehicleRecorder or BaseStationController).
        dest:         Receiver (VehicleRecorder, BaseStationController, or
                      CastObject for broadcast).
        social_group: The SocialGroup this package belongs to.
        bits:         Total payload size in bits.
        appdatas:     List of AppData fragments included in this package.
        offset_ts:    Timeslot index at which transmission starts.
        trans_ts:     Number of timeslots the transmission occupies.
        end_ts:       Timeslot index at which transmission completes
                      (offset_ts + trans_ts).
    """
    def __init__(self,
                 src, dest,
                 social_group: SocialGroup,
                 bits: int,
                 appdatas: List[AppData],
                 trans_ts: int,
                 offset_ts: int):
        self.src = src
        self.dest = dest
        self.social_group = social_group
        self.bits = bits
        self.appdatas = appdatas
        self.offset_ts = offset_ts
        self.trans_ts = trans_ts
        self.end_ts = offset_ts + trans_ts

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
