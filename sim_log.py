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
            SUMO_SIM_INFO.time,
            SUMO_SIM_INFO.ns,
            SUMO_SIM_INFO.ts,
            msg
        )
        self.file.write(log+'\n')
        # print(log)


class Printer(Logger):
    def __init__(self, file):
        super().__init__(file)

    def Log(self, msg: str):
        Logger.Log(self, msg)


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