from od.event.config import SumoSimEventConf
from od.config import SUMO_SIM_SECONDS, SUMO_SKIP_STEPS, SUMO_NET_WARMUP_STEPS
import od.vars as GV


class SumoSimEvent:
    def __init__(self, config: SumoSimEventConf):
        self.beg_ss = SUMO_SKIP_STEPS + SUMO_NET_WARMUP_STEPS + int(round(config.ofs_sec/oc.SUMO_SECONDS_PER_STEP))
        self.end_ss = self.beg_ss + int(round(config.dur_sec/oc.SUMO_SECONDS_PER_STEP))

    def UpdateSS(self):
        if(GV.SUMO_SIM_INFO.ss == self.beg_ss):
            self.Begin()
        elif(GV.SUMO_SIM_INFO.ss == self.end_ss):
            self.End()

    def Begin(self):
        pass

    def End(self):
        pass
