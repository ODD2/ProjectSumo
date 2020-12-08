import os
import sys
import traci
import matlab.engine
import math
import numpy as np
from enum import IntEnum
from datetime import datetime
from globs import *
from threading import Thread
from net_model import BaseStationController, BASE_STATION_CONTROLLER, NET_STATUS_CACHE
from sim_stat import STATISTIC_RECORDER
from veh_rec import VehicleRecorder
from sim_log import DEBUG


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


def ParallelUpdateSS(objs):
    threads = []
    # Update vehicles (Parellelized)
    for obj in objs:
        threads.append(Thread(target=obj.UpdateSS))
        threads[-1].start()
    # Wait until all vehicles to finished their jobs
    for t in threads:
        t.join()


def ParallelUpdateNS(objs, ns):
    # Debug
    for obj in objs:
        obj.UpdateNS(ns)
    return

    threads = []
    # Update vehicles (Parellelized)
    for obj in objs:
        threads.append(Thread(target=obj.UpdateNS), args=(ns,))
        threads[-1].start()
    # Wait until all vehicles to finished their jobs
    for t in threads:
        t.join()


def ParallelUpdateT(objs, ts):
    # Debug
    for obj in objs:
        obj.UpdateT(ts)
    return

    threads = []
    for obj in objs:
        threads.append(Thread(target=obj.UpdateT, args=(ts,)))
        threads[-1].start()
    for t in threads:
        t.join()


def main():
    # Start Traci
    traci.start([
        "sumo-gui",
        "-c",
        os.getcwd() + "/osm.sumocfg",
        "--start",
        "--step-length",
        str(SUMO_SECONDS_PER_STEP),
        #  "--begin", "30"
    ])

    # Create Base Station Icon and Radius in SUMO
    for name, setting in BS_SETTINGS.items():
        CreateBaseStationIndicator(name, setting)

    # Submit all base stations to the Network Model
    for name, setting in BS_SETTINGS.items():
        BASE_STATION_CONTROLLER.append(
            BaseStationController(
                name,
                setting["pos"],
                setting["type"],
                len(BASE_STATION_CONTROLLER)
            )
        )

    # Vehicle Recorders
    vehicle_recorders = {}
    # try:
    # Start Simulation
    step = 0
    while step < SUMO_TOTAL_STEPS:
        traci.simulationStep()
        # Fetch the newest sumo simulation informations
        SUMO_SIM_INFO.UpdateSS()

        # Remove ghost(non-exist) vehicles
        for ghost in SUMO_SIM_INFO.ghost_veh_ids:
            DEBUG.Log("[{}]: left the map.".format(ghost))
            vehicle_recorders.pop(ghost)
        # Add new vehicles
        for v_id in SUMO_SIM_INFO.new_veh_ids:
            DEBUG.Log("[{}]: joined the map.".format(v_id))
            vehicle_recorders[v_id] = VehicleRecorder(v_id)

        # Reset network status cache because vehicle positions have updated,
        # which means the cqi/sinr should be re-estimated.
        NET_STATUS_CACHE.Flush()

        # Create vehicle_recorder list
        vehicles = list(vehicle_recorders.values())

        # Update vehicle recorders for sumo simulation
        ParallelUpdateSS(vehicles)
        # Network simulations per sumo simulation step
        for ns in range(NET_STEPS_PER_SUMO_STEP):
            # Update sumo simulation info for network simulation step
            SUMO_SIM_INFO.UpdateNS(ns)
            # Update vehicle recorders & base stations for each network simulation step
            ParallelUpdateNS(vehicles + BASE_STATION_CONTROLLER, ns)

            # Time slots per network simulation step
            for ts in range(0, NET_TS_PER_NET_STEP+1):
                # Update sumo simulation info for each network timeslot step
                SUMO_SIM_INFO.UpdateTS(ts)
                # Update vehicle recorders & base stations for each network timeslot step
                ParallelUpdateT(vehicles + BASE_STATION_CONTROLLER, ts)

        step += 1
    # except:
        # print("Exception Caught During Simulation")

    # End Simulation
    traci.close()

    # report
    STATISTIC_RECORDER.VehicleReceivedIntactAppdataReport()
    STATISTIC_RECORDER.BaseStationAppdataTXQReport()
    STATISTIC_RECORDER.BaseStationAppdataTXReport()


if __name__ == "__main__":
    main()
