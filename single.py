import od.engine as GE
import od.vars as GV
# STD
from threading import Thread
import numpy as np
import os
import gc
import sys
import traci
import cProfile
import re
# Custom
from od.network.controller import BaseStationController
from od.network.types import BaseStationType, ResourceAllocatorType
from od.vehicle import VehicleRecorder
from od.config import (SUMO_SECONDS_PER_STEP, SUMO_SIM_GUI,
                       SUMO_SIM_STEPS, SUMO_SKIP_STEPS,
                       BS_PRESET,
                       NET_STEPS_PER_SUMO_STEP, NET_TS_PER_NET_STEP,
                       BS_RADIUS_COLOR, BS_RADIUS)
from od.misc.types import DebugMsgType
from od.layer import NetObjLayer
from od.misc.interest import InterestConfig


# Base Station Indicator Creator
def CreateBaseStationIndicator(name, setting):
    # Bs Info
    bs_type = setting["type"]
    x = setting["pos"][0]
    y = setting["pos"][1]
    # Create POI
    traci.poi.add("poi_" + name, x, y, setting["color"], "net_bs",
                  NetObjLayer.BS_POI, setting["img"], setting["width"],
                  setting["height"])

    # Create Polygon
    coef = pow(3, 0.5) / 2
    radius_color = BS_RADIUS_COLOR[bs_type]
    radius = BS_RADIUS[bs_type]
    if bs_type == BaseStationType.UMI:
        radius_layer = NetObjLayer.BS_RAD_UMI
    else:
        radius_layer = NetObjLayer.BS_RAD_UMA
    traci.polygon.add("poly_" + name + "_radius",
                      [(x - radius * coef, y + radius / 2),
                       (x - radius * coef, y - radius / 2), (x, y - radius),
                       (x + radius * coef, y - radius / 2),
                       (x + radius * coef, y + radius / 2), (x, y + radius)],
                      radius_color, True, "net_bs_radius", radius_layer)


def UpdateSS(objs):
    # Debug
    for obj in objs:
        obj.UpdateSS()
    return

    # threads = []
    # Update vehicles (Parellelized)
    # for obj in objs:
    #     t = Thread(target=obj.UpdateSS)
    #     t.start()
    #     threads.append(t)
    # Wait until all vehicles to finished their jobs
    # for t in threads:
    #     t.join()


def UpdateNS(objs, ns):
    # Debug
    for obj in objs:
        obj.UpdateNS(ns)
    return

    # threads = []
    # Update vehicles (Parellelized)
    # for obj in objs:
    #     threads.append(Thread(target=obj.UpdateNS, args=(ns,)))
    #     threads[-1].start()
    # Wait until all vehicles to finished their jobs
    # for t in threads:
    #     t.join()


def UpdateT(objs, ts):
    # Debug
    for obj in objs:
        obj.UpdateT(ts)
    return

    # threads = []
    # for obj in objs:
    #     threads.append(Thread(target=obj.UpdateT, args=(ts,)))
    #     threads[-1].start()
    # for t in threads:
    #     t.join()


def main(interest_config):
    # Prepare Simulation
    # - start traci
    traci.start([
        "sumo-gui" if SUMO_SIM_GUI else "sumo",
        "-c",
        os.getcwd() + "/ntust.sumocfg",
        "--quit-on-end",
        "--start",
        "--step-length",
        str(SUMO_SECONDS_PER_STEP),
        "--scale",
        str(interest_config.traffic_scale)
    ])

    # - skip to interest network condition
    for _ in range(SUMO_SKIP_STEPS):
        traci.simulationStep()

    # - initialize matlab context for simulation
    GE.InitializeSimulationContext()
    # - initialize simulation dependent global variables
    GV.InitializeSimulationVariables(interest_config)

    # - create base station icon and radius in SUMO
    for name, setting in GV.BS_SETTING.items():
        CreateBaseStationIndicator(name, setting)

    # - submit all base stations to the Network Model
    for name, setting in GV.BS_SETTING.items():
        GV.NET_STATION_CONTROLLER.append(
            BaseStationController(
                name,
                setting["pos"],
                setting["type"],
                len(GV.NET_STATION_CONTROLLER)
            )
        )

    # Start Simulation
    # - record vehicles
    vehicle_recorders = {}
    # - run
    for _ in range(SUMO_SIM_STEPS):
        # forward sumo simulation step
        traci.simulationStep()
        # fetch the newest sumo simulation informations
        GV.SUMO_SIM_INFO.UpdateSS()

        # remove ghost(non-exist) vehicles
        for ghost_vid in GV.SUMO_SIM_INFO.ghost_veh_ids:
            GV.DEBUG.Log(
                "[{}]: left the map.".format(ghost_vid),
                DebugMsgType.SUMO_VEH_INFO
            )
            vehicle_recorders[ghost_vid].Leave()
            vehicle_recorders.pop(ghost_vid)

        # add new vehicles
        for vid in GV.SUMO_SIM_INFO.new_veh_ids:
            GV.DEBUG.Log(
                "[{}]: joined the map.".format(vid),
                DebugMsgType.SUMO_VEH_INFO
            )
            vehicle_recorders[vid] = VehicleRecorder(vid)

        # reset network status cache because vehicle positions have updated,
        # which means the cqi/sinr should be re-estimated.
        GV.NET_STATUS_CACHE.Flush()

        # Update vehicle recorders & base stations for sumo simulation step
        UpdateSS(vehicle_recorders.values())
        UpdateSS(GV.NET_STATION_CONTROLLER)

        # Network simulations per sumo simulation step
        for ns in range(NET_STEPS_PER_SUMO_STEP):
            # Update sumo simulation info for network simulation step
            GV.SUMO_SIM_INFO.UpdateNS(ns)

            # Update vehicle recorders & base stations for each network simulation step
            UpdateNS(vehicle_recorders.values(), ns)
            UpdateNS(GV.NET_STATION_CONTROLLER, ns)

            # Time slots per network simulation step
            for ts in range(NET_TS_PER_NET_STEP+1):
                # Update sumo simulation info for each network timeslot step
                GV.SUMO_SIM_INFO.UpdateTS(ts)

                # Update vehicle recorders & base stations for each network timeslot step
                UpdateT(vehicle_recorders.values(), ts)
                UpdateT(GV.NET_STATION_CONTROLLER, ts)

    # End Simulation
    # - manually destruct vehicle recorder in order to close traci.
    for veh_rec in vehicle_recorders.values():
        veh_rec.Leave()
    # - close traci
    traci.close(wait=False)

    # - statistic report
    report = GV.STATISTIC_RECORDER.Report(interest_config)

    # - terminate global variables
    GV.TerminateSimulationVariables()

    return report


if __name__ == "__main__":
    cProfile.run(
        'main(InterestConfig(ResourceAllocatorType.NOMA_OPT,True,0.25,5157253))'
    )
    # main(
    #     InterestConfig(
    #         ResourceAllocatorType.NOMA_OPT,
    #         True,
    #         1
    #     )
    # )
