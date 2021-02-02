# Custom
from od.config import NET_TS_PER_NET_STEP, NET_RB_BW_UNIT
import od.vars as GV
# STD
import sys


# Resource Allocator for OMA
class ResourceAllocatorOMA:
    # like a 2d rectangle:
    # height - the total bandwidth available
    # width - the total timeslots
    def __init__(self, max_bandwidth, max_timeslots):
        if(NET_TS_PER_NET_STEP != 2):
            GV.ERROR.Log(
                "Error!! This allocator only works on 2 timeslots per network step condition."
            )
            sys.exit()

        self.max_bandwidth = max_bandwidth
        self.max_timeslots = max_timeslots
        self.alloc_resources = [
            max_bandwidth for i in range(self.max_timeslots)
        ]

    # returns the offset timeslots of this resource block
    # returns negative value indicates unable to allocate
    def Allocate(self, bandwidth, timeslots):
        offset_timeslot = -1
        if(bandwidth == NET_RB_BW_UNIT*1 and timeslots == 2):
            if(self.alloc_resources[0] >= bandwidth and self.alloc_resources[1] >= bandwidth):
                self.alloc_resources[0] -= bandwidth
                self.alloc_resources[1] -= bandwidth
                offset_timeslot = 0
        elif (bandwidth == NET_RB_BW_UNIT*2 and timeslots == 1):
            # time critical allocation type
            for i in range(NET_TS_PER_NET_STEP):
                if(self.alloc_resources[i] >= bandwidth):
                    self.alloc_resources[i] -= bandwidth
                    offset_timeslot = i
                    break
            # capacity critical allocation type
            # higer_bandwidth_ts = 0
            # for ts in range(self.max_timeslots):
            #     if self.alloc_resources[ts] > self.alloc_resources[higer_bandwidth_ts]:
            #         higer_bandwidth_ts = ts

            # if(self.alloc_resources[higer_bandwidth_ts] >= bandwidth):
            #     self.alloc_resources[higer_bandwidth_ts] -= bandwidth
            #     offset_timeslot = higer_bandwidth_ts

        else:
            GV.ERROR.Log(
                "Error!! This allocator only works on 2x1 or 1x2 resource block allocation"
            )
            sys.exit()
        return offset_timeslot

    # Whether there's spare space for allocation
    def Spare(self, bandwidth, timeslots):
        for i in range(0, NET_TS_PER_NET_STEP, timeslots):
            for j in range(timeslots):
                if(self.alloc_resources[i+j] < bandwidth):
                    break
            else:
                return True
        return False
