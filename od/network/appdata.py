"""
od/network/appdata.py - Application data structures for the network layer.

AppDataHeader is the immutable identity record created when a vehicle spawns
a new piece of application data.  AppData is a mutable fragment that tracks
how many bits of that data have been (or remain to be) transmitted.
"""


class AppDataHeader:
    """Immutable identity and metadata for one application data unit.

    A header is created once when the vehicle application generates data and
    is shared across all AppData fragments derived from it.

    Attributes:
        owner:      VehicleRecorder that originated this data.
        total_bits: Total size of the data in bits.
        serial:     Per-vehicle monotonically increasing counter.
        at:         Creation timestamp in simulation seconds.
        id:         Human-readable unique identifier "<owner_name>-<serial>".
    """
    def __init__(self, owner, total_bits, serial: int, at: float):
        self.owner = owner
        self.total_bits = total_bits
        self.serial = serial
        self.at = at
        self.id = "{}-{}".format(self.owner.name, self.serial)

    def __str__(self):
        return "AppDataHeader({},{}b,{:.4f}s)".format(
            self.id,
            self.total_bits,
            self.at
        )


class AppData:
    """A transmittable fragment of an application data unit.

    Represents the portion of the original data starting at *offset* bits
    with *bits* bits remaining to be sent.  Multiple AppData objects can
    share the same AppDataHeader; together they describe the delivery progress
    of that data unit.

    Attributes:
        header: Reference to the originating AppDataHeader.
        bits:   Number of bits still to be transmitted in this fragment.
        offset: Bit offset of this fragment within the full data unit.
    """
    def __init__(self, header: AppDataHeader, bits: int, offset: int):
        self.header = header
        self.bits = bits
        self.offset = offset

    def __str__(self):
        return "Appdata({}-{},{}o+{}b)".format(
            self.header.owner.name,
            self.header.serial,
            self.offset,
            self.bits
        )
