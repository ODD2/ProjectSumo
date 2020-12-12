from enum import IntEnum

# Sumo Graphics Network Object Layer
class NetObjLayer(IntEnum):
    BS_POI = 2
    BS_RAD_UMA = BS_POI - 2
    BS_RAD_UMI = BS_POI - 1
    CON_LINE = BS_POI + 1
