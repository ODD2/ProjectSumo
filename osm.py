import os
import sys
import traci
import matlab.engine
import math
import numpy as np
from threading import Thread
from multiprocessing import Process
from net_model import BaseStationController, BASE_STATION_CONTROLLER, NET_STATUS_CACHE
from veh_rec import VehicleRecorder
from enum import IntEnum
from datetime import datetime
from globs import *

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
    if bs_type == BaseStationType.UMI:
        radius_layer = NetObjLayer.BS_RAD_UMI
        radius_color = BS_UMI_RADIUS_COLOR
        radius = BS_UMI_RADIUS
    else:
        radius_layer = NetObjLayer.BS_RAD_UMA
        radius_color = BS_UMA_RADIUS_COLOR
        radius = BS_UMA_RADIUS

    traci.polygon.add("poly_" + name + "_radius",
                      [(x - radius * coef, y + radius / 2),
                       (x - radius * coef, y - radius / 2), (x, y - radius),
                       (x + radius * coef, y - radius / 2),
                       (x + radius * coef, y + radius / 2), (x, y + radius)],
                      radius_color, True, "net_bs_radius", radius_layer)


def main():

    # Check Basic Requirements
    if SIM_SECONDS_PER_STEP / NET_SECONDS_PER_STEP < 0:
        print(
            "Error: seconds per simulation step should be larger than the value of seconds per network step."
        )
        return
    if SIM_SECONDS_PER_STEP / NET_SECONDS_PER_STEP % 1 != 0:
        print(
            "Error: seconds per simulation step should be totally devided by the value of seconds per network step."
        )
        return

    # Start Traci
    traci.start([
        "sumo",
        "-c",
        os.getcwd() + "\\osm.sumocfg",
        "--start",
        "--step-length",
        str(SIM_SECONDS_PER_STEP),
        #  "--begin", "30"
    ])

    # Create Base Station Icon and Radius in SUMO
    for name, setting in BS_SETTINGS.items():
        CreateBaseStationIndicator(name, setting)

    # Submit all base stations to the Network Model
    for name, setting in BS_SETTINGS.items():
        BASE_STATION_CONTROLLER.append(
            BaseStationController(name, setting["pos"], setting["type"],
                                  len(BASE_STATION_CONTROLLER)))

    # Vehicle Recorders
    vehicle_recorders = {}

    # Frequently used constants
    NET_STEPS_PER_SIM_STEP = int(SIM_SECONDS_PER_STEP / NET_SECONDS_PER_STEP)
    TOTAL_SIM_STEPS = (1 / SIM_SECONDS_PER_STEP) * 100

    # Start Simulation
    step = 0
    while step < TOTAL_SIM_STEPS:
        traci.simulationStep()
        SIM_STEP_INFO.Update()
        # Flush NetStatusCache because the vehicles might move in this step.
        NET_STATUS_CACHE.Flush()

        # Remove ghost vehicles
        for ghost in SIM_STEP_INFO.ghost_veh_ids:
            vehicle_recorders.pop(ghost)

        # Add new vehicles
        for v_id in SIM_STEP_INFO.new_veh_ids:
            vehicle_recorders[v_id] = VehicleRecorder(v_id)

        # Network simulations
        for _ in range(NET_STEPS_PER_SIM_STEP):
            # Time slots per network simulation step
            for ts in range(1, NET_TS_PER_STEP+1):
                veh_thrds = []
                # Update vehicles (Parellelized)
                for v_id in SIM_STEP_INFO.veh_ids:
                    t = Thread(
                        target=vehicle_recorders[v_id].Update,
                        args=(ts)
                    )
                    t.start()
                    veh_thrds.append(t)
                # Wait until all vehicles to finished their jobs
                for t in veh_thrds:
                    t.join()

                bs_thrds = []
                # Update all base stations  (Parellelized)
                for base_station in BASE_STATION_CONTROLLER:
                    t = Thread(
                        target=base_station.Update,
                        args=(ts)
                    )
                    t.start()
                    bs_thrds.append(t)
                # Wait until all base stations finished their jobs
                for t in bs_thrds:
                    t.join()

        step += 1
    # End Simulation
    traci.close()


if __name__ == "__main__":
    main()
