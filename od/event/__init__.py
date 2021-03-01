from od.config import SUMO_SKIP_STEPS
import od.vars as GV


class SumoSimEvents:
    def __init__(self, ofs_ss, dur_ss):
        self.beg_ss = SUMO_SKIP_STEPS + ofs_ss
        self.end_ss = self.beg_ss + dur_ss
        pass

    def UpdateSS(self):
        if(GV.SUMO_SIM_INFO.ss == self.beg_ss):
            self.Begin()
        elif(GV.SUMO_SIM_INFO.ss == self.end_ss):
            self.End()

    def Begin(self):
        pass

    def End(self):
        pass
