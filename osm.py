import os
import sys
import traci
import matlab.engine
import math
import numpy as np
from threading import Thread
from multiprocessing import Process
from net_model import BaseStationController, BASE_STATION_CONTROLLER, CQI_SINR_BUF
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
        print("Error: seconds per simulation step should be larger than the value of seconds per network step.")
        return
    if SIM_SECONDS_PER_STEP/NET_SECONDS_PER_STEP % 1 != 0:
        print("Error: seconds per simulation step should be totally devided by the value of seconds per network step.")
        return

    # Start Traci
    traci.start(["sumo",
                 "-c",
                 os.getcwd() + "\\osm.sumocfg",
                 "--start",
                 "--step-length", str(SIM_SECONDS_PER_STEP),
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
                setting["pos"], setting["type"],
                len(BASE_STATION_CONTROLLER)
            )
        )

    # Vehicle Recorders
    vehicle_recorders = {}

    # Frequently used constants
    TIMESLOTS_PER_STEP = int(SIM_SECONDS_PER_STEP/NET_SECONDS_PER_STEP)

    # Start Simulation
    step = 0
    while step < 1000:
        traci.simulationStep()
        SIM_STEP_INFO.Update()
        # Remove ghost vehicles
        for ghost in SIM_STEP_INFO.ghost_veh_ids:
            vehicle_recorders.pop(ghost)

        # Add new vehicles
        for v_id in SIM_STEP_INFO.new_veh_ids:
            vehicle_recorders[v_id] = VehicleRecorder(v_id)

        # Network simulations
        for i in range(TIMESLOTS_PER_STEP):
            CQI_SINR_BUF.Initialize()

            veh_prls = []
            # Update Vehicles (Parellelized)
            for v_id in SIM_STEP_INFO.veh_ids:
                t = Thread(target=vehicle_recorders[v_id].Update)
                t.start()
                veh_prls.append(t)
            # Wait until all vehicles to finished their jobs
            for t in veh_prls:
                t.join()

            # bs_prls = []
            # # Update all BaseStations  (Parellelized)
            # for base_station in BASE_STATION_CONTROLLER:
            #     t = Thread(target=base_station.Update)
            #     t.start()
            #     bs_prls.append(t)
            # # Wait until all base stations finished their jobs
            # for t in bs_prls:
            #     t.join()

        step += 1
    # End Simulation
    traci.close()


if __name__ == "__main__":
    main()
