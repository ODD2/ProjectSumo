"""
od/misc/siminfo.py - SUMO simulation state tracker.

SumoSimInfo is updated at each simulation time level (SUMO step, network step,
timeslot) and acts as the authoritative source of simulation time for all
other modules via getTime() and getTimeNS().
"""
from od.env.config import SUMO_SECONDS_PER_STEP, NET_SECONDS_PER_STEP, NET_SECONDS_PER_TS
from od import traci
import math

# Numeric Precision Settings
TIME_ROUND_DECIMAL = math.floor(abs(math.log(NET_SECONDS_PER_TS, 10))) + 1


class SumoSimInfo:
    """Tracks current simulation time across all three time scales.

    Attributes:
        new_veh_ids:   Vehicle IDs that appeared in the latest SUMO step.
        veh_ids:       All vehicle IDs currently on the map.
        ghost_veh_ids: Vehicle IDs that left the map in the latest SUMO step.
        st:  Simulation time in seconds (from SUMO).
        ss:  SUMO step index (st / SUMO_SECONDS_PER_STEP, rounded).
        ns:  Network step index within the current SUMO step.
        ts:  Timeslot index within the current network step.
    """
    def __init__(self):
        self.new_veh_ids = []
        self.veh_ids = []
        self.ghost_veh_ids = []
        self.st = 0
        self.ss = 0
        self.ns = 0
        self.ts = 0

    def UpdateSS(self):
        """Synchronise with SUMO at the start of each SUMO step.

        Queries TraCI for the current time and vehicle list, then computes
        the sets of newly arrived and departed vehicles.
        """
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
        """Advance to network step *ns* within the current SUMO step."""
        self.ns = ns
        self.ts = 0

    def UpdateTS(self, ts):
        """Advance to timeslot *ts* within the current network step."""
        self.ts = ts

    def getTimeNS(self):
        """Return the current time in seconds, resolved to the network-step level.

        Does not include the sub-network-step timeslot offset.
        """
        return round(
            (self.ss * SUMO_SECONDS_PER_STEP +
             self.ns * NET_SECONDS_PER_STEP),
            TIME_ROUND_DECIMAL
        )

    def getTime(self):
        """Return the current time in seconds at full (timeslot) resolution."""
        return round(
            (self.ss * SUMO_SECONDS_PER_STEP +
             self.ns * NET_SECONDS_PER_STEP +
             self.ts * NET_SECONDS_PER_TS),
            TIME_ROUND_DECIMAL
        )
