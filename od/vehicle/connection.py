from enum import IntEnum
from od.layer import NetObjLayer
from od.env.config import SUMO_SIM_GUI
import od.vars as GV
import traci


class ConnectionState(IntEnum):
    Unknown = 0
    Connect = 1,
    Deny = 2,
    Transmit = 3,
    Success = 4


class SharedConnection:
    def __init__(self, rec):
        self.share = 0
        self.rec = rec


class ConnectionRecorder:
    def __init__(self, s1, s2):
        if(SUMO_SIM_GUI):
            self.s1 = s1
            self.s2 = s2
            self.state = ConnectionState.Connect
            self.state_color = (0, 0, 0, 255)
            self.name = "con_{}_{}".format(s1.name, s2.name)
            GV.TRACI_LOCK.acquire()
            # # Create line
            traci.polygon.add(self.name, [(0, 0), (0, 0)], (0, 0, 0, 255), False,
                              "Line", NetObjLayer.CON_LINE, 0.1)
            GV.TRACI_LOCK.release()

    def Update(self):
        if(SUMO_SIM_GUI):
            # Update
            GV.TRACI_LOCK.acquire()
            traci.polygon.setShape(self.name, [self.s1.pos, self.s2.pos])
            traci.polygon.setColor(self.name, self.state_color)
            GV.TRACI_LOCK.release()
            # Reset
            self.ChangeState(ConnectionState.Connect, True)

    def ChangeState(self, state: ConnectionState, force=False):
        if(SUMO_SIM_GUI):
            if (not force and self.state > state):
                return
            self.state = state
            if (state == ConnectionState.Transmit):
                self.state_color = (255, 165, 0, 255)
            elif (state == ConnectionState.Success):
                self.state_color = (0, 255, 0, 255)
            else:
                self.state_color = (0, 0, 0, 255)

    def Clean(self):
        if(SUMO_SIM_GUI):
            # pass
            GV.TRACI_LOCK.acquire()
            traci.polygon.remove(self.name)
            GV.TRACI_LOCK.release()
