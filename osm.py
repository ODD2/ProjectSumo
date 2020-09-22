import os
import sys
import traci
import matlab.engine
import math
import numpy as np
from threading import Thread
from multiprocessing import Process
from net_model import BaseStationController, BASE_STATION_CONTROLLER
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
    # Setup Traci Environment
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        print(tools)
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

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
                 ])

    # Create Base Station Icon and Radius in SUMO
    for name, setting in BS_SETTINGS.items():
        CreateBaseStationIndicator(name, setting)

    # Submit all base stations to the Network Model
    for name, setting in BS_SETTINGS.items():
        BASE_STATION_CONTROLLER.append(BaseStationController(
            name,
            setting["pos"], setting["type"]))

    # Vehicle Recorders
    vehicle_recorders = {}

    # Frequently used constants
    TIMESLOTS_PER_STEP = int(SIM_SECONDS_PER_STEP/NET_SECONDS_PER_STEP)

    # Start Simulation
    step = 0
    while step < 1000:
        traci.simulationStep()
        traci_vids = traci.vehicle.getIDList()
        # Loop Through All Vehicles
        for v_id in traci_vids:
            # Newly Joined Vehicle: Create Vehicle Recorder For It
            if not v_id in vehicle_recorders:
                vehicle_recorders[v_id] = VehicleRecorder(v_id)
                print("{}: joined the map.".format(v_id))

        for i in range(TIMESLOTS_PER_STEP):
            veh_prls = []
            # Update Vehicles (Parellelized)
            for v_id in traci_vids:
                t = Thread(target=vehicle_recorders[v_id].Update)
                t.start()
                veh_prls.append(t)
            # Wait all vehicles to finish their jobs
            for t in veh_prls:
                t.join()

            bs_prls = []
            # Update all BaseStations  (Parellelized)
            for base_station in BASE_STATION_CONTROLLER:
                t = Thread(target=base_station.Update)
                t.start()
                bs_prls.append(t)
            # Wait all base stations to finish their jobs
            for t in bs_prls:
                t.join()

          # Find None-Updating Vehicles as Ghost Vehicles
        current_time = traci.simulation.getTime()
        ghost_vehicles = []
        for v_id, vr_obj in vehicle_recorders.items():
            if vr_obj.sync_time < current_time:
                ghost_vehicles.append(v_id)

        # Remove Ghost Vehicles
        for v_id in ghost_vehicles:
            print("{}: left the map.".format(v_id))
            vehicle_recorders[v_id].Clear()
            vehicle_recorders.pop(v_id)

        step += 1
    # End Simulation
    traci.close()


def Job(mutex):
    mutex.acquire()
    print(traci.simulation.getTime())
    mutex.release()


def test():
    # Setup Traci Environment
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        print(tools)
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # Check Basic Requirements
    if SIM_SECONDS_PER_STEP / NET_SECONDS_PER_STEP < 0:
        print("Error: seconds per simulation step should be larger than the value of seconds per network step.")
        return
    if SIM_SECONDS_PER_STEP/NET_SECONDS_PER_STEP % 1 != 0:
        print("Error: seconds per simulation step should be totally devided by the value of seconds per network step.")
        return

    # Start Traci
    traci.start(["sumo-gui",
                 "-c",
                 os.getcwd() + "\\osm.sumocfg",
                 "--start",
                 "--step-length", str(SIM_SECONDS_PER_STEP),
                 ])
    step = 0
    while step < 1000000:
        traci.simulationStep()
        l = []
        for i in range(10):
            t = Thread(target=Job, args=())
            t.start()
            l.append(t)
        for t in l:
            t.join()

        step += 1


if __name__ == "__main__":
    main()
    # test()
