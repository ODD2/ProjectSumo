from enum import IntEnum
from od.layer import NetObjLayer
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
        self.s1 = s1
        self.s2 = s2
        self.state = ConnectionState.Connect
        self.name = "con_{}_{}".format(s1.name, s2.name)
        GV.TRACI_LOCK.acquire()
        # Create line
        traci.polygon.add(self.name, [(0, 0), (0, 0)], (0, 0, 0, 255), False,
                          "Line", NetObjLayer.CON_LINE, 0.1)
        GV.TRACI_LOCK.release()

    def Update(self):
        GV.TRACI_LOCK.acquire()
        traci.polygon.setShape(self.name, [self.s1.pos, self.s2.pos])
        GV.TRACI_LOCK.release()

    def ChangeState(self, state: ConnectionState, force=False):
        if (not force and self.state > state):
            return

        self.state = state

        GV.TRACI_LOCK.acquire()
        if (state == ConnectionState.Transmit):
            traci.polygon.setColor(self.name, (255, 165, 0, 255))
        elif (state == ConnectionState.Success):
            traci.polygon.setColor(self.name, (0, 255, 0, 255))
        else:
            traci.polygon.setColor(self.name, (0, 0, 0, 255))
        GV.TRACI_LOCK.release()

    def Clean(self):
        GV.TRACI_LOCK.acquire()
        traci.polygon.remove(self.name)
        GV.TRACI_LOCK.release()
