import sys
from sim_log import DEBUG
from globs import NET_TS_PER_NET_STEP, NET_RB_BW_UNIT


# Resource Allocator for OMA
class ResourceAllocatorOMA:
    # like a 2d rectangle:
    # height - the total bandwidth available
    # width - the total timeslots
    def __init__(self, max_bandwidth):
        if(NET_TS_PER_NET_STEP != 2):
            DEBUG.Log(
                "Error!! This allocator only works on 2 timeslots per network step condition."
            )
            sys.exit()

        self.max_bandwidth = max_bandwidth
        self.max_timeslots = NET_TS_PER_NET_STEP
        self.alloc_resources = [
            max_bandwidth for i in range(self.max_timeslots)
        ]

    # returns the offset timeslots of this resource block
    # returns negative value indicates unable to allocate
    def Allocate(self, bandwidth, timeslots):
        offset_timeslot = -1
        if(bandwidth == NET_RB_BW_UNIT*1 and timeslots == 2):
            if(self.alloc_resources[0] >= bandwidth and
               self.alloc_resources[1] >= bandwidth):
                self.alloc_resources[0] -= bandwidth
                self.alloc_resources[1] -= bandwidth
                offset_timeslot = 0
        elif (bandwidth == NET_RB_BW_UNIT*2 and timeslots == 1):
            for ts in range(self.max_timeslots):
                if(self.alloc_resources[ts] >= bandwidth):
                    self.alloc_resources[ts] -= bandwidth
                    offset_timeslot = ts
                    break
        else:
            DEBUG.Log(
                "Error!! This allocator only works on 2x1 or 1x2 resource block allocation"
            )
            sys.exit()
        return offset_timeslot

    # Whether there's spare space for allocation
    def Spare(self):
        if(self.alloc_resources[0] == 0 and self.alloc_resources[1] == 0):
            return False
        else:
            return True
