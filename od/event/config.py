"""
od/event/config.py - Simulation event configuration container.
"""


class SumoSimEventConf:
    """Timing descriptor for a simulation event.

    Args:
        ofs_sec: Offset in seconds after the warmup period before the event begins.
        dur_sec: Duration of the event in seconds.
    """
    def __init__(self, ofs_sec, dur_sec):
        self.ofs_sec = ofs_sec
        self.dur_sec = dur_sec
