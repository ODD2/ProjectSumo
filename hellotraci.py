
import os
import sys
import traci
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "D:/Sumo/osm/osm.sumocfg", "--start"]
traci.start(sumoCmd)
step = 0
while step < 1000:
    traci.simulationStep()
    if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
        iduloop_v1id = traci.inductionloop.getLastStepVehicleIDs("0")[0]
        print("vehicle id:" + str(iduloop_v1id) +
              " (speed:"+str(traci.vehicle.getSpeed(iduloop_v1id))+")")
    step += 1

traci.close()
