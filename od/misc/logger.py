import os
import od.vars as GV


class Logger:
    def __init__(self, file):
        dirpath = "log/"
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        self.file = open(dirpath+file, "w")

    def Log(self, msg: str):
        log = "[{:.2f}s][{:.0f}n/{:.0f}t]{}".format(
            GV.SUMO_SIM_INFO.getTime(),
            GV.SUMO_SIM_INFO.ns,
            GV.SUMO_SIM_INFO.ts,
            msg
        )
        self.file.write(log+'\n')
        return log


class Printer(Logger):
    def __init__(self, file):
        super().__init__(file)

    def Log(self, msg: str):
        msg = Logger.Log(self, msg)
        print(msg)
        return msg