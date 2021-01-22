import os
import od.vars as GV
from od.config import DEBUG_MSG_FLAGS
from od.misc.types import DebugMsgType


class Logger:
    def __init__(self, dirpath, file):
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        self.file = open(dirpath+file, "w")

    def Encapsulate(self):
        self.file.close()

    def Doc(self, msg: str):
        self.file.write(msg+'\n')
        return msg

    def Log(self, msg: str):
        log = "[{:.4f}s][{:.0f}n/{:.0f}t]{}".format(
            GV.SUMO_SIM_INFO.getTime(),
            GV.SUMO_SIM_INFO.ns,
            GV.SUMO_SIM_INFO.ts,
            msg
        )
        self.file.write(log+'\n')
        return log


class Printer(Logger):
    def __init__(self, dirpath, file):
        super().__init__(dirpath, file)

    def Log(self, msg: str):
        msg = Logger.Log(self, msg)
        print(msg)
        return msg


class Debugger(Logger):
    def __init__(self, dirpath, file):
        super().__init__(dirpath, file)

    def Doc(self, msg, level: DebugMsgType):
        if(level & DEBUG_MSG_FLAGS > 0):
            return Logger.Doc(self, msg)
        return ""

    def Log(self, msg, level: DebugMsgType):
        if(level & DEBUG_MSG_FLAGS > 0):
            return Logger.Log(self, msg)
        return ""
