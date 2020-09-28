from datetime import datetime
from globs import SIM_INFO


class Logger:
    def __init__(self, file):
        self.file = open("log/"+file, "w")

    def Log(self, msg: str):
        log = "[{}s][{}n/{}t]{}".format(
            SIM_INFO.time,
            SIM_INFO.ns,
            SIM_INFO.ts,
            msg
        )
        self.file.write(log+'\n')
        print(log)


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
