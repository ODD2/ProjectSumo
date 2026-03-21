"""
od/layer.py - SUMO visualisation layer indices for network objects.

Layer ordering determines draw priority in the SUMO GUI (higher value = on top).
"""
from enum import IntEnum


class NetObjLayer(IntEnum):
    """z-layer indices for network-related SUMO GUI objects.

    Attributes:
        BS_RAD_UMA: Coverage radius polygon for UMA macro cells (drawn below UMI).
        BS_RAD_UMI: Coverage radius polygon for UMI small cells.
        BS_POI:     Base station icon (POI), rendered above radius polygons.
        CON_LINE:   Vehicle-to-BS connection line, drawn on top of everything.
    """
    BS_POI = 2
    BS_RAD_UMA = BS_POI - 2
    BS_RAD_UMI = BS_POI - 1
    CON_LINE = BS_POI + 1
