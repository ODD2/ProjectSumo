from od.vehicle import VehicleRecorder
from od.network.application import AppDataHeader


# Requests from vehicles for upload resources
class UploadRequest:
    def __init__(self, sender: VehicleRecorder, total_bits: int):
        self.sender = sender
        self.total_bits = total_bits


# Requests from vehicles for non-intact appdata
class ResendRequest:
    def __init__(self, sender: VehicleRecorder, header: AppDataHeader, offset: int, bits: int):
        self.sender = sender
        self.header = header
        self.offset = offset
        self.bits = bits
