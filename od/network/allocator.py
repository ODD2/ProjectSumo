# Custom
from math import log10
from od.env.config import (NET_TS_PER_NET_STEP, NET_RB_BW_UNIT, NET_RB_BW_REQ_TS,
                           BS_UMI_RB_BW_QoS, NET_RB_SLOT_SYMBOLS)
from od.social.group import QoSLevel, SocialGroup
import od.vars as GV
import od.engine as GE
# STD
import sys


# allocation parameters provided by external system.
class ExternAllocParam:
    def __init__(self):
        self.reset()

    def reset(self):
        self.tval = 1


# Approximation Allocator Specifically for 1x2 and 2x1 geometric resource blocks in a 2 timeslot
# def ResourceAllocatorNomaApprox(RES_CONF, QoS_GP_CONF):
#     # initialization

#     for qos in QoSLevel:
#         sort_gp_conf = [gp for gp in QoS_GP_CONF if gp.qos == qos].sort(key=gp["eager_rate"], reverse=True)
#         rb_req_ubw = BS_UMI_RB_BW_QoS[qos]
#         rb_req_ts = NET_RB_BW_REQ_TS[rb_req_ubw * NET_RB_BW_UNIT]
#         for gp in sort_gp_conf:
#             pass

class NomaRbConfig:
    def __init__(self, owner, cqi):
        self.cqi = cqi
        self.rbfc = []
        self.owner = owner


class NomaRbfConfig:
    def __init__(self, rem_pwr_mW):
        self.rem_pwr_mW = rem_pwr_mW
        self.layer_rb = [None for _ in range(2)]

    def __getitem__(self, key):
        return self.layer_rb[key]

    def __setitem__(self, key, value):
        self.layer_rb[key] = value


class ResourceAllocatorNomaApprox:
    def __init__(self, RES_CONF, QoS_GP_CONF):
        self.RES_CONF = RES_CONF
        self.QoS_GP_CONF = QoS_GP_CONF
        self.frbf_h = round(RES_CONF["rbf_h"])
        self.frbf_w = round(RES_CONF["rbf_w"])
        self.max_pwr_mW = pow(10, RES_CONF["max_pwr_dBm"]/10)
        self.grid = [
            [
                NomaRbfConfig(self.max_pwr_mW) for _ in range(self.frbf_w)
            ] for _ in range(self.frbf_h)
        ]
        self.spare_inner_rb = {
            2: {1: []},
            1: {2: []}
        }
        self.validations = [
            self.CheckValidSymetricGeo,
            self.CheckValidSpareOuter,
            self.CheckValidSpareInner
        ]

    def CheckValidSymetricGeo(self, gp_conf, min_req_pwr, rbf_h, rbf_w):
        frbf_h, frbf_w = self.frbf_h, self.frbf_w
        if(len(self.spare_inner_rb[rbf_h][rbf_w]) == 0):
            return -1, -1, -1
        # sort the resource blocks in a descedent order.
        self.spare_inner_rb[rbf_h][rbf_w].sort(key=lambda x: x.rbfc[0].rem_pwr_mW, reverse=True)
        # check if the maximum valid resource block provides a valid power
        if(self.spare_inner_rb[rbf_h][rbf_w][0].rbfc[0].rem_pwr_mW < min_req_pwr):
            return -1, -1, -1
        target_rb = self.spare_inner_rb[rbf_h][rbf_w][0]
        # remove rb from list, it's no longer a spare rb
        self.spare_inner_rb[rbf_h][rbf_w] = self.spare_inner_rb[rbf_h][rbf_w][1:]
        for x in range(frbf_w):
            for y in range(frbf_h):
                if(self.grid[y][x][0] == target_rb):
                    return y, x, 1
        else:
            raise Exception("Unknown Error! Cannot Find Target RB in inner layer grid.")

    def CheckValidSpareOuter(self,  gp_conf, min_req_pwr, rbf_h, rbf_w):
        frbf_h, frbf_w = self.frbf_h, self.frbf_w
        for x in range(frbf_w-rbf_w+1):
            for y in range(frbf_h-rbf_h+1):
                for _x in range(rbf_w):
                    for _y in range(rbf_h):
                        rbfc = self.grid[y+_y][x+_x]
                        if(rbfc[0] == None or rbfc[0].owner == gp_conf or
                           not rbfc[1] == None or rbfc.rem_pwr_mW < min_req_pwr):
                            break
                    else:
                        continue
                    break
                else:
                    return y, x, 1
                continue
        return -1, -1, -1

    def CheckValidSpareInner(self, gp_conf, min_req_pwr, rbf_h, rbf_w):
        frbf_h, frbf_w = self.frbf_h, self.frbf_w
        for x in range(frbf_w-rbf_w+1):
            for y in range(frbf_h-rbf_h+1):
                # 1x2 resource block search in a reverse direction
                # for better resource arrangment
                if(y == 2 and x == 1):
                    y = frbf_h - 2 - y
                for _y in range(rbf_h):
                    for _x in range(rbf_w):
                        if(not self.grid[y+_y][x+_x][0] == None):
                            break
                    else:
                        continue
                    break
                else:
                    return y, x, 0
        return -1, -1, -1

    def __call__(self):
        return self.ArrangeResource()

    def ArrangeResource(self):
        alloc_report = {}
        # allocate resource
        for gp_confs in self.QoS_GP_CONF:
            if(len(gp_confs) == 0):
                continue
            # sort group configs according to its eager rate, higer rate indicates higher priority.
            sort_gp_confs = sorted(gp_confs, key=lambda x: x["eager_rate"], reverse=True)
            for gp_conf in sort_gp_confs:
                # preparation
                rbf_w, rbf_h = round(gp_conf["rbf_w"]), round(gp_conf["rbf_h"])
                gp_spare_inner_rb = []
                max_sinr = gp_conf["sinr_max"]
                max_sinr_noise_reciprocal = (
                    pow(10, max_sinr/10) / self.max_pwr_mW
                )
                max_cqi = GE.MATLAB_ENG.SelectCQI_BLER10P(max_sinr)
                max_sinr_req_pwr_mW = pow(10, gp_conf["pwr_req_dBm"]/10)
                max_sinr_ext_pwr_mW = pow(10, gp_conf["pwr_ext_dBm"]/10)
                min_sinr_req_pwr_mW = pow(10, -6.9/10)/max_sinr_noise_reciprocal
                # allocate resource
                while(gp_conf["rem_bits"] > 0):
                    x, y, z = -1, -1, -1
                    v = 0
                    # run through validation list for valid RB allocation.
                    for validation in self.validations:
                        v += 1
                        y, x, z = validation(gp_conf, min_sinr_req_pwr_mW, rbf_h, rbf_w)
                        if(x > -1 and y > -1 and z > -1):
                            break
                    else:
                        # if all validation fails, the allocation fails.
                        break

                    # calculate acquire power and cqi settings
                    rb_cqi = 0
                    req_pwr_mW = 0
                    rem_pwr_mW = self.max_pwr_mW
                    if(z == 0):
                        req_pwr_mW = max_sinr_req_pwr_mW
                        rem_pwr_mW = max_sinr_ext_pwr_mW
                        rb_cqi = max_cqi
                    else:
                        rem_pwr_mW_list = [
                            self.grid[y+_y][x+_x].rem_pwr_mW
                            for _x in range(rbf_w) for _y in range(rbf_h)
                        ]
                        req_pwr_mW = min(rem_pwr_mW_list)
                        rem_pwr_mW = 0
                        rb_cqi = GE.MATLAB_ENG.SelectCQI_BLER10P(
                            10*log10(req_pwr_mW*max_sinr_noise_reciprocal)
                        )
                    # if maximum valid cqi is 0, the allocation fails.
                    if(rb_cqi == 0):
                        raise Exception("Error!RBF selection has been filtered, resource block CQI should not be 0.")
                    # create resource block
                    rb = NomaRbConfig(gp_conf, rb_cqi)
                    # assign resource block to the grid
                    for _x in range(rbf_w):
                        for _y in range(rbf_h):
                            rbfc = self.grid[y+_y][x+_x]
                            rbfc[z] = rb
                            rb.rbfc.append(rbfc)
                            rbfc.rem_pwr_mW = rem_pwr_mW
                    # reduce claimed resource
                    gp_conf["rem_bits"] -= GE.MATLAB_ENG.GetThroughputPerRB(
                        float(rb_cqi),
                        int(NET_RB_SLOT_SYMBOLS)
                    )
                    # record newly created inner resource block as spare resource block.
                    if(z == 0):
                        gp_spare_inner_rb.append(rb)
                    # record the resource assignment
                    key_gid = "g{}".format(int(gp_conf["gid"]))
                    key_ofs_ts = "t{}".format(int(x))
                    key_cqi = "c{}".format(int(rb_cqi))
                    if(key_gid not in alloc_report):
                        alloc_report[key_gid] = {}
                    if(key_ofs_ts not in alloc_report[key_gid]):
                        alloc_report[key_gid][key_ofs_ts] = {}
                    if(key_cqi not in alloc_report[key_gid][key_ofs_ts]):
                        alloc_report[key_gid][key_ofs_ts][key_cqi] = 0
                    alloc_report[key_gid][key_ofs_ts][key_cqi] += 1
                # record newly added inner rb according to its geometry
                self.spare_inner_rb[rbf_h][rbf_w] += gp_spare_inner_rb
        return alloc_report


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
