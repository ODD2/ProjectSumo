from od.env.config import SUMO_SECONDS_PER_STEP, NET_SECONDS_PER_STEP, NET_SECONDS_PER_TS
from od import traci
import math

# Numeric Precision Settings
TIME_ROUND_DECIMAL = math.floor(abs(math.log(NET_SECONDS_PER_TS, 10))) + 1


class SumoSimInfo:
    def __init__(self):
        self.new_veh_ids = []
        self.veh_ids = []
        self.ghost_veh_ids = []
        self.st = 0
        self.ss = 0
        self.ns = 0
        self.ts = 0

    def UpdateSS(self):
        # sumo simulation time
        self.st = traci.simulation.getTime()
        # simulation step
        self.ss = round(self.st/SUMO_SECONDS_PER_STEP)
        # net step
        self.ns = 0
        # time step
        self.ts = 0
        # vehicles currently on the map
        cur_veh_ids = traci.vehicle.getIDList()
        # Find the vehicles that've left the map
        self.ghost_veh_ids = [
            veh_id for veh_id in self.veh_ids if veh_id not in cur_veh_ids
        ]
        # Find the vehicles that've joined the map
        self.new_veh_ids = [
            veh_id for veh_id in cur_veh_ids if veh_id not in self.veh_ids
        ]
        # Update current vehicle ids
        self.veh_ids = cur_veh_ids

    def UpdateNS(self, ns):
        self.ns = ns
        self.ts = 0

    def UpdateTS(self, ts):
        self.ts = ts

    def getTimeNS(self):
        return round(
            (self.ss * SUMO_SECONDS_PER_STEP +
             self.ns * NET_SECONDS_PER_STEP),
            TIME_ROUND_DECIMAL
        )

    def getTime(self):
        return round(
            (self.ss * SUMO_SECONDS_PER_STEP +
             self.ns * NET_SECONDS_PER_STEP +
             self.ts * NET_SECONDS_PER_TS),
            TIME_ROUND_DECIMAL
        )
