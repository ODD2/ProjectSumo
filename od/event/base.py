"""
od/event/base.py - Abstract base class for SUMO simulation events.

Events are triggered by the SUMO step counter.  Begin() is called on the
SUMO step matching beg_ss and End() is called on end_ss.
"""
from od.event.config import SumoSimEventConf
from od.env.config import SUMO_SECONDS_PER_STEP, SUMO_SKIP_STEPS, SUMO_NET_WARMUP_STEPS
import od.vars as GV


class SumoSimEvent:
    """Base class for time-bounded simulation events.

    Subclasses override Begin() and End() to implement event-specific effects.

    Attributes:
        beg_ss: SUMO step index at which Begin() is triggered.
        end_ss: SUMO step index at which End() is triggered.
    """
    def __init__(self, config: SumoSimEventConf):
        self.beg_ss = SUMO_SKIP_STEPS + SUMO_NET_WARMUP_STEPS + int(round(config.ofs_sec/SUMO_SECONDS_PER_STEP))
        self.end_ss = self.beg_ss + int(round(config.dur_sec/SUMO_SECONDS_PER_STEP))

    def UpdateSS(self):
        if(GV.SUMO_SIM_INFO.ss == self.beg_ss):
            self.Begin()
        elif(GV.SUMO_SIM_INFO.ss == self.end_ss):
            self.End()

    def Begin(self):
        pass

    def End(self):
        pass
