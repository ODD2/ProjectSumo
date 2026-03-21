"""
od/vehicle/monitor.py - Per-vehicle network traffic counters.
"""


class NetworkStatusMonitor:
    """Simple counter set for tracking a vehicle's packet send/receive activity.

    Attributes:
        total_recv_package: Cumulative downlink packages received.
        total_send_package: Cumulative uplink packages sent.
        step_recv_package:  Downlink packages received in the current step.
        step_send_package:  Uplink packages sent in the current step.
    """
    def __init__(self):
        self.total_recv_package = 0
        self.total_send_package = 0
        self.step_recv_package = 0
        self.step_send_package = 0


