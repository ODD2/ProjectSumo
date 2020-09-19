import os
import sys
import traci
import matlab.engine
import math
import numpy as np
from net_model import BaseStationController, BASE_STATION_CONTROLLER
from veh_rec import VehicleRecorder
from enum import IntEnum
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


if __name__ == "__main__":
    # Create Matlab Engine
    eng = matlab.engine.start_matlab()

    # Add Matlab File Search Locations
    eng.addpath(os.getcwd() + "\\matlab\\")
    eng.addpath(os.getcwd() + "\\matlab\\SelectCQI_bySNR\\")

    # Setup Traci Environment
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        print(tools)
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # Start Traci
    traci.start(["sumo-gui",
                 "-c",
                 os.getcwd() + "\\osm.sumocfg",
                 "--start",
                 "--step-length", "0.001",
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

    # Start Simulation
    step = 0
    while step < 1000000:
        traci.simulationStep()
        # if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
        #     iduloop_v1id = traci.inductionloop.getLastStepVehicleIDs("0")[0]
        #     print("vehicle id:" + str(iduloop_v1id) + " (speed:" +
        #           str(traci.vehicle.getSpeed(iduloop_v1id)) + ")")

        # Loop Through All Vehicles
        for v_id in traci.vehicle.getIDList():
            # Newly Joined Vehicle: Create Vehicle Recorder For It
            if not v_id in vehicle_recorders:
                vehicle_recorders[v_id] = VehicleRecorder(v_id)
            # Update Vehicle
            vehicle_recorders[v_id].Update(eng)

        # Loop Through All BaseStations
        for base_station in BASE_STATION_CONTROLLER:
            base_station.Update(eng)

        # Find None-Updating Vehicles as Ghost Vehicles
        current_time = traci.simulation.getTime()
        ghost_vehicles = []
        for v_id, vr_obj in vehicle_recorders.items():
            if vr_obj.update_time < current_time:
                ghost_vehicles.append(v_id)

        # Remove Ghost Vehicles
        for v_id in ghost_vehicles:
            vehicle_recorders[v_id].Clear()
            vehicle_recorders.pop(v_id)

        step += 1
    # End Simulation
    traci.close()
