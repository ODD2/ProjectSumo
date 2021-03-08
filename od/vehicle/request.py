from od.vehicle import VehicleRecorder
from od.network.appdata import AppDataHeader


# Requests from vehicles for upload resources
class UploadRequest:
    def __init__(self, sender: VehicleRecorder, total_bits: int, starv_time: float):
        self.sender = sender
        self.total_bits = total_bits
        self.starv_time = starv_time


# Requests from vehicles for non-intact appdata
class ResendRequest:
    def __init__(self, sender: VehicleRecorder, header: AppDataHeader, offset: int, bits: int):
        self.sender = sender
        self.header = header
        self.offset = offset
        self.bits = bits
