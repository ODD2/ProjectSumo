from datetime import datetime
from globs import SUMO_STEP_INFO


class Logger:
    def __init__(self, file):
        self.file = open("log/"+file, "w")

    def Log(self, msg: str):
        self.file.write("[{}]".format(SUMO_STEP_INFO.time) + msg+"\n")
        print("[{}]".format(SUMO_STEP_INFO.time) + msg+"\n")


class Printer(Logger):
    def __init__(self, file):
        super().__init__(file)

    def Log(self, msg: str):
        Logger.Log(self, msg)
        print("[{}]".format(SUMO_STEP_INFO.time) + msg+"\n")


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
