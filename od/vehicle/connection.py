"""
od/vehicle/connection.py - Vehicle-to-BS connection state and SUMO GUI lines.

ConnectionRecorder draws and updates a coloured line in the SUMO GUI between
a vehicle and a base station, encoding the current link state as a colour:
  black  – idle / connected but no traffic.
  orange – actively transmitting.
  green  – transmission just completed successfully.

SharedConnection wraps a ConnectionRecorder with a reference count so that
the line is kept alive as long as at least one social group subscription
exists for that vehicle–BS pair, and removed when the last subscription ends.
"""
from enum import IntEnum
from od.layer import NetObjLayer
from od.env.config import SUMO_SIM_GUI
import od.vars as GV
from od import traci


class ConnectionState(IntEnum):
    """Ordered link states used to drive connection-line colour in the SUMO GUI.

    Higher values take priority: a Transmit state will not be overwritten by
    a Connect state within the same timeslot.
    """
    Unknown = 0
    Connect = 1,
    Deny = 2,
    Transmit = 3,
    Success = 4


class SharedConnection:
    """Reference-counted wrapper for a ConnectionRecorder.

    share counts how many active social group subscriptions share this
    vehicle–BS connection line.  The line is removed when share reaches 0.
    """
    def __init__(self, rec):
        self.share = 0
        self.rec = rec


class ConnectionRecorder:
    """Manages the SUMO GUI polygon line representing one vehicle–BS connection.

    Only active when SUMO_SIM_GUI is True; all methods are no-ops otherwise.
    """
    def __init__(self, s1, s2):
        if(SUMO_SIM_GUI):
            self.s1 = s1
            self.s2 = s2
            self.state = ConnectionState.Connect
            self.state_color = (0, 0, 0, 255)
            self.name = "con_{}_{}".format(s1.name, s2.name)
            GV.TRACI_LOCK.acquire()
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
            GV.TRACI_LOCK.acquire()
            traci.polygon.remove(self.name)
            GV.TRACI_LOCK.release()
