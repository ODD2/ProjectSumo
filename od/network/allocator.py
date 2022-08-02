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
# def ResourceAllocatorNomaApprox(RES_CONF , QoS_GP_CONF):
#     # initialization

#     for qos in QoSLevel:
#         sort_gp_conf = [gp for gp in QoS_GP_CONF if gp.qos == qos].sort(key=gp["eager_rate"], reverse=True)
#         rb_req_ubw = BS_UMI_RB_BW_QoS[qos]
#         rb_req_ts = NET_RB_BW_REQ_TS[rb_req_ubw * NET_RB_BW_UNIT]
#         for gp in sort_gp_conf:
#             pass

class AsymNomaRbConfig:
    def __init__(self, inner_rbs, outer_rbs, outer_pwr_mW):
        self.inner_rbs = inner_rbs
        self.outer_rbs = outer_rbs
        self.outer_pwr_mW = outer_pwr_mW

    def __repr__(self):
        return "{{I:{},O:{}}}".format(self.inner_rbs, self.outer_rbs)


class SymNomaRbConfig:
    def __init__(self, inner_rb, outer_rb):
        self.inner_rb = inner_rb
        self.outer_rb = outer_rb

    def __repr__(self):
        return "{{I:{},O:{}}}".format(self.inner_rb, self.outer_rb)


class NomaRbConfig:
    def __init__(self, owner, cqi):
        self.cqi = cqi
        self.owner = owner

    def __repr__(self):
        return "(g{}:c{})".format(int(self.owner["gid"]), int(self.cqi))

    def __str__(self):
        return self.__repr__()


class InnerRbConfig(NomaRbConfig):
    def __init__(self, owner, cqi, rem_pwr_mW):
        self.rem_pwr_mW = rem_pwr_mW
        super().__init__(owner, cqi)

    def __repr__(self):
        return "({},rem_pwr:{})".format(super().__repr__(), self.rem_pwr_mW)


class OuterRbConfig(NomaRbConfig):
    def __init__(self, owner, cqi):
        super().__init__(owner, cqi)


class ResourceAllocatorNomaApprox:
    def __init__(self, RES_CONF, QoS_GP_CONF):
        self.RES_CONF = RES_CONF
        self.QoS_GP_CONF = QoS_GP_CONF
        self.frbf_h = round(RES_CONF["rbf_h"])
        self.frbf_w = round(RES_CONF["rbf_w"])
        self.max_pwr_mW = pow(10, RES_CONF["max_pwr_dBm"] / 10)

        self.spare_inner_rb = {2: {1: []}, 1: {2: []}}
        self.spare_hybrid_rb = {2: {1: []}, 1: {2: []}}
        self.solid_hybrid_rb = {2: {1: []}, 1: {2: []}}
        self.solid_normal_rb = {2: {1: []}, 1: {2: []}}

        self.procedures = [
            self.CheckValidSymetricGeo,
            self.CheckValidSpareInner,
            self.CheckValidSpareOuter
        ]

    def CheckValidSymetricGeo(self, gp_conf, rbf_h, rbf_w, gp_pwr_conf):

        if(len(self.spare_inner_rb[rbf_h][rbf_w]) == 0):
            return False
        # classify valid/defect spare inner resource block for specify group.
        valid_spare_inner_rb = []
        defect_spare_inner_rb = []
        for inner_rb in self.spare_inner_rb[rbf_h][rbf_w]:
            if (not inner_rb.owner == gp_conf) and (inner_rb.rem_pwr_mW > gp_pwr_conf["min_sinr_req_pwr_mW"]):
                valid_spare_inner_rb.append(inner_rb)
            else:
                defect_spare_inner_rb.append(inner_rb)
        print(gp_conf, self.spare_inner_rb[rbf_h][rbf_w], gp_pwr_conf)
        # checking for existence of valid spare inner resource block
        if(len(valid_spare_inner_rb) == 0):
            return False

        # sort all valid spare inner resource block according to its remaining power
        valid_spare_inner_rb.sort(key=lambda x: x.rem_pwr_mW, reverse=True)
        # get the target spare inner resource block
        target_rb = valid_spare_inner_rb[0]

        # remove target RB from spare inner resource block list, it's no longer a spare RB.
        self.spare_inner_rb[rbf_h][rbf_w] = valid_spare_inner_rb[1:] + defect_spare_inner_rb
        # add target RB to solid inner resource block list.
        rb_cqi = GE.SelectCQI_BLER10P(
            10 * log10(target_rb.rem_pwr_mW * gp_pwr_conf["max_sinr_noise_reciprocal"])
        )
        self.solid_normal_rb[rbf_h][rbf_w].append(
            SymNomaRbConfig(
                target_rb,
                OuterRbConfig(
                    gp_conf,
                    rb_cqi
                )
            )
        )
        gp_conf["rem_bits"] -= GE.GetThroughputPerRB(
            float(rb_cqi),
            int(NET_RB_SLOT_SYMBOLS)
        )
        return True

    def CheckValidSpareOuter(self, gp_conf, rbf_h, rbf_w, gp_pwr_conf):
        # check for hybrid resource blocks to convert into a solid one.
        if(len(self.spare_hybrid_rb[rbf_w][rbf_h]) > 0):
            # find resource block providing best power condition
            self.spare_hybrid_rb[rbf_w][rbf_h].sort(key=lambda x: x.outer_pwr_mW, reverse=True)
            target_rb = self.spare_hybrid_rb[rbf_w][rbf_h][0]
            # add outer resource block configuration
            rb_cqi = GE.SelectCQI_BLER10P(
                10 * log10(
                    target_rb.outer_pwr_mW * gp_pwr_conf["max_sinr_noise_reciprocal"]
                )
            )
            target_rb.outer_rbs.append(
                OuterRbConfig(
                    gp_conf,
                    rb_cqi
                )
            )
            gp_conf["rem_bits"] -= GE.GetThroughputPerRB(
                float(rb_cqi),
                int(NET_RB_SLOT_SYMBOLS)
            )
            # remove from hybrid RB list, due to it has become a solid RB.
            self.spare_hybrid_rb[rbf_w][rbf_h] = self.spare_hybrid_rb[rbf_w][rbf_h][1:]
            # add into solid RB list.
            self.solid_hybrid_rb[rbf_w][rbf_h].append(target_rb)
            return True

        # check for spare resource blocks to construct into a hybrid one.
        if(len(self.spare_inner_rb[rbf_w][rbf_h]) >= 2):
            # find the best power condition spare inner resource block
            self.spare_inner_rb[rbf_w][rbf_h].sort(key=lambda x: x.rem_pwr_mW, reverse=True)
            # fetch the required inner RB
            inner_rbs = self.spare_inner_rb[rbf_w][rbf_h][:2]
            # calculate maximum valid power
            valid_pwr_mW = min([x.rem_pwr_mW for x in inner_rbs])
            # no valid power in current condition, end procedure.
            if(valid_pwr_mW < gp_pwr_conf["min_sinr_req_pwr_mW"]):
                return False
            # remove from spare inner RB list, due to they have become a hybrid RB
            self.spare_inner_rb[rbf_w][rbf_h] = self.spare_inner_rb[rbf_w][rbf_h][2:]
            # add into hybrid RB list
            rb_cqi = GE.SelectCQI_BLER10P(
                10 * log10(
                    valid_pwr_mW * gp_pwr_conf["max_sinr_noise_reciprocal"]
                )
            )
            self.spare_hybrid_rb[rbf_w][rbf_h].append(
                AsymNomaRbConfig(
                    inner_rbs,
                    [
                        OuterRbConfig(
                            gp_conf,
                            rb_cqi
                        )
                    ],
                    valid_pwr_mW
                )
            )
            gp_conf["rem_bits"] -= GE.GetThroughputPerRB(
                float(rb_cqi),
                int(NET_RB_SLOT_SYMBOLS)
            )
            return True
        return False

    def CheckValidSpareInner(self, gp_conf, rbf_h, rbf_w, gp_pwr_conf):
        # calculate resource occupation
        num_random_2_1_rb = (
            len(self.spare_inner_rb[2][1]) +
            len(self.solid_normal_rb[2][1])
        )
        num_static_2_1_rb = (
            len(self.spare_hybrid_rb[2][1]) +
            len(self.solid_hybrid_rb[2][1])
        )
        num_1_2_rb = (
            len(self.spare_inner_rb[1][2]) +
            len(self.spare_hybrid_rb[1][2]) * 2 +
            len(self.solid_hybrid_rb[1][2]) * 2 +
            len(self.solid_normal_rb[1][2])
        )
        # construct valid remaining resource block fractions per timeslot.
        rem_rbf_ts = [
            (
                self.frbf_h -
                num_1_2_rb -
                (int(num_random_2_1_rb / 2) + (num_random_2_1_rb % 2) + num_static_2_1_rb) * 2
            ),
            (
                self.frbf_h -
                num_1_2_rb -
                (int(num_random_2_1_rb / 2) + num_static_2_1_rb) * 2
            )
        ]
        # examine valid resource space
        for x in range(self.frbf_w):
            for _x in range(rbf_w):
                if((x + _x) < self.frbf_w and rem_rbf_ts[x + _x] >= rbf_h):
                    continue
                else:
                    break
            else:
                # create if resource sufficient.
                self.spare_inner_rb[rbf_h][rbf_w].append(
                    InnerRbConfig(
                        gp_conf,
                        gp_pwr_conf["max_cqi"],
                        gp_pwr_conf["max_sinr_ext_pwr_mW"]
                    )
                )
                gp_conf["rem_bits"] -= GE.GetThroughputPerRB(
                    float(gp_pwr_conf["max_cqi"]),
                    int(NET_RB_SLOT_SYMBOLS)
                )
                return True
        return False

    def __call__(self):
        return self.AllocateResource()

    def AllocateResource(self):
        # allocate resource
        for gp_confs in self.QoS_GP_CONF:
            if(len(gp_confs) == 0):
                continue
            # sort group configs according to its eager rate, higer rate indicates higher priority.
            sort_gp_confs = sorted(
                gp_confs,
                # key=lambda x: x["eager_rate"] * (pow(10, x["sinr_max"] / 10) / (pow(10, x["pwr_req_dBm"] / 10))),
                key=lambda x: x["eager_rate"] * x["sinr_max"],
                reverse=True
            )
            print([(gp_conf["gid"], gp_conf["eager_rate"] * gp_conf["sinr_max"]) for gp_conf in gp_confs])
            for gp_conf in sort_gp_confs:

                # preparation
                rbf_w, rbf_h = round(gp_conf["rbf_w"]), round(gp_conf["rbf_h"])
                max_sinr = gp_conf["sinr_max"]
                max_sinr_req_pwr_mW = pow(10, gp_conf["pwr_req_dBm"] / 10)
                max_sinr_noise_reciprocal = pow(10, max_sinr / 10) / max_sinr_req_pwr_mW
                pwr_conf = {
                    "max_sinr_noise_reciprocal": max_sinr_noise_reciprocal,
                    "max_cqi": GE.SelectCQI_BLER10P(max_sinr),
                    "max_sinr_req_pwr_mW": max_sinr_req_pwr_mW,
                    "max_sinr_ext_pwr_mW": pow(10, gp_conf["pwr_ext_dBm"] / 10),
                    "min_sinr_req_pwr_mW": pow(10, -6.9 / 10) / max_sinr_noise_reciprocal
                }
                print("Allocate For:\n{}\n{}".format(gp_conf, pwr_conf))
                # allocate resource
                while(gp_conf["rem_bits"] > 0):
                    # run through validation list for valid RB allocation.
                    for procedure in self.procedures:
                        if(procedure(gp_conf, rbf_h, rbf_w, pwr_conf)):
                            break
                    else:
                        # if all validation fails, the allocation fails.
                        break
        # create report
        alloc_report = self.CreateAllocationReport()
        return alloc_report

    def CreateAllocationReport(self):
        alloc_report = {}
        # allocation assignment report for all 1x2 geo resource blocks
        all_1_2_rbs = (
            [rb for rb in self.spare_inner_rb[1][2]] +
            [rb for asym_rb in self.spare_hybrid_rb[1][2] for rb in asym_rb.inner_rbs] +
            [rb for asym_rb in self.spare_hybrid_rb[2][1] for rb in asym_rb.outer_rbs] +
            [sym_rb.inner_rb for sym_rb in self.solid_normal_rb[1][2]] +
            [sym_rb.outer_rb for sym_rb in self.solid_normal_rb[1][2]] +
            [rb for asym_rb in self.solid_hybrid_rb[1][2] for rb in asym_rb.inner_rbs] +
            [rb for asym_rb in self.solid_hybrid_rb[2][1] for rb in asym_rb.outer_rbs]
        )
        # add 1x2 geo resource blocks into report
        for rb in all_1_2_rbs:
            # record the resource assignment
            self.ConstructReportEntity(alloc_report, rb.owner["gid"], 0, rb.cqi)

        # allocation assignment report for all 2x1 geo resource blocks
        all_2_1_rbs = [[] for _ in range(2)]
        # 2x1 resource blocks that could be arrange in desire.
        random_2_1_rbs = (
            [SymNomaRbConfig(rb, None) for rb in self.spare_inner_rb[2][1]] +
            [sym_rb for sym_rb in self.solid_normal_rb[2][1]]
        )
        # 2x1 resource blocks that had been arranged specifically.
        static_2_1_rbs = (
            [asym_rb.inner_rbs for asym_rb in self.spare_hybrid_rb[2][1]] +
            [asym_rb.outer_rbs for asym_rb in self.spare_hybrid_rb[1][2]] +
            [asym_rb.inner_rbs for asym_rb in self.solid_hybrid_rb[2][1]] +
            [asym_rb.outer_rbs for asym_rb in self.solid_hybrid_rb[1][2]]
        )
        # arrange random 2x1 resource blocks(higher qos priority has earlier timeslot offset advantage.)
        random_2_1_rbs.sort(key=lambda x: x.inner_rb.owner["gid"])
        max_2_1_rb_per_col = int(len(random_2_1_rbs) / 2) + len(random_2_1_rbs) % 2
        for i, sym_rb in enumerate(random_2_1_rbs):
            ofs_ts = int(i / max_2_1_rb_per_col)
            all_2_1_rbs[ofs_ts].append(sym_rb.inner_rb)
            if(sym_rb.outer_rb):
                all_2_1_rbs[ofs_ts].append(sym_rb.outer_rb)
        # arrange dependent 2x1 resource blocks(higher qos priority has earlier timeslot offset advantage.)
        for pair_rbs in static_2_1_rbs:
            pair_rbs.sort(key=lambda x: x.owner["gid"])
            for ofs_ts, rb in enumerate(pair_rbs):
                all_2_1_rbs[ofs_ts].append(rb)
        # add 1x2 geo resource blocks into report
        for ofs_ts, rbs in enumerate(all_2_1_rbs):
            for rb in rbs:
                # record the resource assignment
                self.ConstructReportEntity(alloc_report, rb.owner["gid"], ofs_ts, rb.cqi)
        return alloc_report

    def ConstructReportEntity(self, alloc_report, gid, ofs_ts, cqi):
        key_gid = "g{}".format(int(gid))
        key_ofs_ts = "t{}".format(int(ofs_ts))
        key_cqi = "c{}".format(int(cqi))
        if(key_gid not in alloc_report):
            alloc_report[key_gid] = {}
        if(key_ofs_ts not in alloc_report[key_gid]):
            alloc_report[key_gid][key_ofs_ts] = {}
        if(key_cqi not in alloc_report[key_gid][key_ofs_ts]):
            alloc_report[key_gid][key_ofs_ts][key_cqi] = 0
        alloc_report[key_gid][key_ofs_ts][key_cqi] += 1


# Resource Allocator for OMA
class ResourceAllocatorOMA:
    # like a 2d rectangle:
    # height - the total bandwidth available
    # width - the total timeslots
    def __init__(self, max_bandwidth, max_timeslots):
        if(NET_TS_PER_NET_STEP != 2):
            msg = "Error!! This allocator only works on 2 timeslots per network step condition."
            GV.ERROR.Log(msg)
            raise Exception(msg)

        self.max_bandwidth = max_bandwidth
        self.max_timeslots = max_timeslots
        self.alloc_resources = [
            max_bandwidth for i in range(self.max_timeslots)
        ]

    # returns the offset timeslots of this resource block
    # returns negative value indicates unable to allocate
    def Allocate(self, bandwidth, timeslots):
        offset_timeslot = -1
        if(bandwidth == NET_RB_BW_UNIT * 1 and timeslots == 2):
            if(self.alloc_resources[0] >= bandwidth and self.alloc_resources[1] >= bandwidth):
                self.alloc_resources[0] -= bandwidth
                self.alloc_resources[1] -= bandwidth
                offset_timeslot = 0
        elif (bandwidth == NET_RB_BW_UNIT * 2 and timeslots == 1):
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
            msg = "Error!! This allocator only works on 2x1 or 1x2 resource block allocation"
            GV.ERROR.Log(
                msg
            )
            raise Exception(msg)
        return offset_timeslot

    # Whether there's spare space for allocation
    def Spare(self, bandwidth, timeslots):
        for i in range(0, NET_TS_PER_NET_STEP, timeslots):
            for j in range(timeslots):
                if(self.alloc_resources[i + j] < bandwidth):
                    break
            else:
                return True
        return False
