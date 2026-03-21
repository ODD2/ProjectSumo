"""
od/env/station.py - Static base station deployment map.

BS_PRESET defines the physical properties of every base station in the NTUST
campus scenario.  Each entry maps a unique name to a dict with:
  - pos:    (x, y) coordinates in the SUMO network coordinate system (metres).
  - color:  RGBA tuple for the POI icon.
  - img:    Absolute path to the icon image shown in the SUMO GUI.
  - width / height: Displayed icon size in SUMO units.
  - type:   BaseStationType (UMA or UMI).

The BS_SETTING dict used at runtime is derived from BS_PRESET in od/vars.py,
filtered by whether UMI cells are enabled for the current scenario.
"""
from od.network.types import BaseStationType
import os
import sys

# Base Station Presets
BS_PRESET = {
    "UMA-1": {
        "color": (0, 0, 0, 255),
        "pos": (160, 100),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMA,
    },
    "UMA-2": {
        "color": (0, 0, 0, 255),
        "pos": (450, 330),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMA,
    },
    "UMI-1": {
        "color": (0, 0, 0, 255),
        "pos": (127, 217),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
    "UMI-2": {
        "color": (0, 0, 0, 255),
        "pos": (52, 145),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
    "UMI-3": {
        "color": (0, 0, 0, 255),
        "pos": (315, 395),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
    "UMI-4": {
        "color": (0, 0, 0, 255),
        "pos": (270, 50),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
    "UMI-5": {
        "color": (0, 0, 0, 255),
        "pos": (525, 95),
        "img": os.getcwd() + "/wifi.png",
        "width": 5,
        "height": 3.9,
        "type": BaseStationType.UMI,
    },
}
