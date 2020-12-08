import os
from datetime import datetime
from globs import SUMO_SIM_INFO


class Logger:
    def __init__(self, file):
        dirpath = "log/"
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        self.file = open(dirpath+file, "w")

    def Log(self, msg: str):
        log = "[{}s][{}n/{}t]{}".format(
            SUMO_SIM_INFO.getTime(),
            SUMO_SIM_INFO.ns,
            SUMO_SIM_INFO.ts,
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


DEBUG = Logger(
    "Debug ({}).txt".format(
        datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    )
)

ERROR = Printer(
    "Error ({}).txt".format(
        datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    )
)

STATISTIC = Logger(
    "Statistic ({}).txt".format(
        datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    )
)
