
import os
import sys
import traci
import matlab.engine
import math
import numpy as np
# Create Matlab Engine
eng = matlab.engine.start_matlab()
# Add Matlab File Search Locations
eng.addpath(os.getcwd()+"\\matlab\\")
eng.addpath(os.getcwd()+"\\matlab\\SelectCQI_bySNR\\")


def GET_BS_CQI_Vector(BS_POSITIONS, UE_POSITION):
    MACRO_BS_NUM = 0
    N_BS = len(BS_POSITIONS)
    CQI_Iter = np.zeros(N_BS, dtype=float)
    SINR_Iter = np.zeros(N_BS, dtype=float)

    for tx_BS_num in range(N_BS):
        Intf_dist = []
        Intf_pwr_dBm = []
        Intf_h_BS = []
        Intf_h_MS = []
        # Intf_DS_Desired = []

        # Confirm settings with 3GPP specs
        h_BS = 25
        h_MS = 0.8
        if(tx_BS_num == MACRO_BS_NUM):
            tx_p_dBm = 23
            CP = 4.69
            bandwidth = 180000
        else:
            tx_p_dBm = 10
            CP = 2.34
            bandwidth = 360000

        UE_dist = pow((BS_POSITIONS[tx_BS_num][0]-UE_POSITION[0])**2 +
                      (BS_POSITIONS[tx_BS_num][0]-UE_POSITION[0])**2, 0.5)

        # up to 4 us
        DS_Desired = np.random.normal(0, 4)

        for intf_BS_num in range(N_BS):
            if(intf_BS_num == tx_BS_num):
                continue

            if(intf_BS_num == MACRO_BS_NUM):
                Intf_h_BS.append(25.0)
                Intf_h_MS.append(0.8)
                Intf_pwr_dBm.append(23)
            else:
                Intf_h_BS.append(10.0)
                Intf_h_MS.append(0.8)
                Intf_pwr_dBm.append(18)

            # GHz
            fc = 2.0

            # Locations
            Intf_dist.append((pow((BS_POSITIONS[intf_BS_num][0]-UE_POSITION[0])**2 +
                                  (BS_POSITIONS[intf_BS_num][0]-UE_POSITION[0])**2, 0.5)))

            (CQI_Iter[tx_BS_num], SINR_Iter[tx_BS_num]) = eng.SINR_Channel_Model_Multi_Var_BS(
                float(UE_dist), float(h_BS), float(h_MS),
                float(fc), float(tx_p_dBm), float(bandwidth),
                matlab.double(Intf_h_BS),
                matlab.double(Intf_h_MS),
                matlab.double(Intf_dist),
                matlab.double(Intf_pwr_dBm),
                float(DS_Desired), float(CP), nargout=2)
    return CQI_Iter


if __name__ == "__main__":
    # Setup Traci Environment
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        print(tools)
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    # Start Traci
    traci.start(["sumo-gui", "-c", "D:/Sumo/osm/osm.sumocfg", "--start"])

    # Fetch Base Station 2D Locations In Advance
    bs_positions = []
    for bs_id in ["poi_1", "poi_2", "poi_3", "poi_4", "poi_5"]:
        bs_positions.append(traci.poi.getPosition(bs_id))

    # Start Simulation
    step = 0
    while step < 1000:
        traci.simulationStep()
        if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
            iduloop_v1id = traci.inductionloop.getLastStepVehicleIDs("0")[0]
            print("vehicle id:" + str(iduloop_v1id) +
                  " (speed:"+str(traci.vehicle.getSpeed(iduloop_v1id))+")")
        for v_id in traci.vehicle.getIDList():
            CQI_Vec = GET_BS_CQI_Vector(bs_positions,
                                        traci.vehicle.getPosition(v_id))
            lerp = max(CQI_Vec)/30
            traci.vehicle.setColor(v_id, (255*(1-lerp), 255*lerp, 0, 255))
        # for v_id in traci.vehicle.getIDList():
        #     shortDistance = 1e10
        #     for bs_position in bs_positions:
        #         veh_position = traci.vehicle.getPosition(v_id)
        #         delta_position = [veh_position[0] -
        #                           bs_position[0], veh_position[1]-bs_position[1]]
        #         distance = pow(pow(delta_position[0], 2) +
        #                        pow(delta_position[1], 2), 0.5)
        #         shortDistance = shortDistance if shortDistance < distance else distance
        #     lerp = shortDistance/50
        #     if(lerp > 1):
        #         lerp = 1
        #     traci.vehicle.setColor(v_id, (255*lerp, 255*(1-lerp), 0, 255))

        step += 1
    # End Simulation
    traci.close()
