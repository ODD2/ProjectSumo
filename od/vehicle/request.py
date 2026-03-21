"""
od/vehicle/request.py - Vehicle uplink resource request types.
"""
from od.vehicle import VehicleRecorder
from od.network.appdata import AppDataHeader


class UploadRequest:
    """Request submitted by a vehicle asking a BS for uplink resource blocks.

    Attributes:
        sender:      The VehicleRecorder that issued the request.
        total_bits:  Total number of bits pending for upload in this social group.
        starv_time:  Creation timestamp of the oldest queued AppData; used by
                     the BS to prioritise vehicles that have been waiting longest.
    """
    def __init__(self, sender: VehicleRecorder, total_bits: int, starv_time: float):
        self.sender = sender
        self.total_bits = total_bits
        self.starv_time = starv_time


class ResendRequest:
    """Request for retransmission of a missing fragment (currently unused).

    Attributes:
        sender: The VehicleRecorder requesting the retransmit.
        header: AppDataHeader identifying the incomplete data unit.
        offset: Byte offset from which retransmission should begin.
        bits:   Number of bits to retransmit.
    """
    def __init__(self, sender: VehicleRecorder, header: AppDataHeader, offset: int, bits: int):
        self.sender = sender
        self.header = header
        self.offset = offset
        self.bits = bits
