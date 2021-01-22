class AppDataHeader:
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
