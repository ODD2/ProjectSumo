"""
od/misc/logger.py - Simulation logging utilities.

Three logger classes are provided:

  Logger   – writes timestamped messages to a file.
  Printer  – Logger that also prints to stdout.
  Debugger – Logger whose output is gated by a bitmask of DebugMsgType flags,
             allowing fine-grained control over which subsystems produce output
             without removing log calls from the source code.
"""
import os
import od.vars as GV
from od.env.config import DEBUG_MSG_FLAGS
from od.misc.types import DebugMsgType


class Logger:
    """File-based logger that prepends a simulation timestamp to each entry.

    Creates the output directory if it does not already exist.
    """
    def __init__(self, dirpath, file):
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        self.file = open(dirpath + file, "w")

    def Encapsulate(self):
        """Close the underlying log file."""
        self.file.close()

    def Doc(self, msg: str):
        """Write *msg* to the log without a timestamp prefix."""
        self.file.write(msg + '\n')
        return msg

    def Log(self, msg: str):
        """Write *msg* to the log with a simulation-time prefix.

        Format: ``[<time>s][<ns>n/<ts>t]<msg>``
        """
        log = "[{:.4f}s][{:.0f}n/{:.0f}t]{}".format(
            GV.SUMO_SIM_INFO.getTime(),
            GV.SUMO_SIM_INFO.ns,
            GV.SUMO_SIM_INFO.ts,
            msg
        )
        self.file.write(log + '\n')
        return log


class Printer(Logger):
    """Logger subclass that mirrors every log entry to stdout."""
    def __init__(self, dirpath, file):
        super().__init__(dirpath, file)

    def Log(self, msg: str):
        msg = Logger.Log(self, msg)
        print(msg)
        return msg


class Debugger(Logger):
    """Logger subclass whose output is filtered by a DebugMsgType bitmask.

    Only messages whose *level* flag overlaps with the global DEBUG_MSG_FLAGS
    constant are actually written.  This allows per-subsystem debug output to
    be enabled or disabled at configuration time without changing call sites.
    """
    def __init__(self, dirpath, file):
        super().__init__(dirpath, file)

    def Doc(self, msg_fmt, msg_args, level: DebugMsgType):
        if(level & DEBUG_MSG_FLAGS > 0):
            return Logger.Doc(self, msg_fmt.format(*msg_args))
        return ""

    def Log(self, msg_fmt, msg_args, level: DebugMsgType):
        if(level & DEBUG_MSG_FLAGS > 0):
            return Logger.Log(self, msg_fmt.format(*msg_args))
        return ""
