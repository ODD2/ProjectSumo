from od.social import SocialGroup
from od.network.types import LinkType
from od.network.application import AppData, AppDataHeader, NetworkCoreApplication
from od.network.package import NetworkPackage
from od.network.types import BroadcastObject, BaseStationType
from od.vehicle.request import UploadRequest, ResendRequest
from od.network.allocator import ResourceAllocatorOMA
from od.config import (NET_TS_PER_NET_STEP, NET_QOS_CHNLS, NET_RB_BW_REQ_TS,
                       NET_RB_SLOT_SYMBOLS, NET_RB_BW_UNIT,
                       BS_UMA_RB_BW, BS_UMI_RB_BW_SG,
                       BS_TOTAL_BANDWIDTH, BS_RADIUS,
                       BS_TRANS_PWR)
from od.engine import MATLAB_ENG
import od.vars as GV
import math
import io

# Base station controller: allocate resource for upload/download requests


class BaseStationController:
    def __init__(self, name, pos, bs_type, serial):
        # Base station paremeters
        self.name = name
        self.pos = pos
        self.type = bs_type
        self.radius = BS_RADIUS[bs_type]
        self.serial = serial

        # vehicles that've subscribed to specific social groups
        self.sg_sub_vehs = [[] for i in SocialGroup]

        # Upload/Download packages that're currently transmitting
        self.pkg_in_proc = [[] for i in LinkType]

        # upload requests
        self.sg_upload_req = ([{} for x in range(NET_QOS_CHNLS)])

        # broadcast reqeusts
        self.sg_brdcst_datas = ([{} for x in range(NET_QOS_CHNLS)])

        # TODO: resend requests
        # self.sg_resend_req = ([[] for x in SocialGroup])

    def __index__(self):
        return self.serial

    # Called every network step
    def UpdateNS(self, ns):
        self.ArrangeUplinkResource()
        self.ArrangeDownlinkResource()

    # Called every timeslot
    def UpdateT(self, ts):
        self.ProcessPackage(ts)

    # process uploading/downloading packages
    def ProcessPackage(self, timeslot):
        # Upload
        for pkg in self.pkg_in_proc[LinkType.UPLINK]:
            if timeslot == (pkg.offset_ts + pkg.trans_ts):
                # log
                GV.DEBUG.Log(
                    "[{}][package][{}]:receive.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg
                    )
                )
                self.PackageDelivered(pkg)
        # .remove delivered packages
        self.pkg_in_proc[LinkType.UPLINK] = [
            pkg
            for pkg in self.pkg_in_proc[LinkType.UPLINK]
            if (pkg.offset_ts+pkg.trans_ts) > timeslot
        ]
        # Download
        for pkg in self.pkg_in_proc[LinkType.DOWNLINK]:
            if(pkg.offset_ts == timeslot):
                GV.DEBUG.Log(
                    "[{}][package][{}]:deliver.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg
                    )
                )
        # . remove sent packages
        self.pkg_in_proc[LinkType.DOWNLINK] = [
            pkg
            for pkg in self.pkg_in_proc[LinkType.DOWNLINK]
            if(pkg.offset_ts) > timeslot
        ]

    # process delivered packages
    def PackageDelivered(self, package: NetworkPackage):
        GV.NET_CORE_CONTROLLER.PackageDelivered(package)

    # Function called by VehicleRecorder to submit upload requests to this base station
    def ReceiveUploadRequest(self, sender, social_group: SocialGroup, total_bits: int):
        if social_group not in self.sg_upload_req[social_group.qos]:
            self.sg_upload_req[social_group.qos][social_group] = []

        self.sg_upload_req[social_group.qos][social_group].append(
            UploadRequest(sender, total_bits)
        )

    # arrange uplink resource
    def ArrangeUplinkResource(self):
        # OMA resource allocator
        ra_oma = ResourceAllocatorOMA(
            BS_TOTAL_BANDWIDTH[self.type]*0.9,
            NET_TS_PER_NET_STEP
        )
        # Serve requests
        for qos in range(NET_QOS_CHNLS):
            for social_group in self.sg_upload_req[qos].keys():
                # Check if there exists pending requests
                if (len(self.sg_upload_req[qos][social_group]) > 0 and ra_oma.Spare()):
                    # fetch resource block trans size for every request
                    req_rbsize_pairs = []
                    for req in self.sg_upload_req[qos][social_group]:
                        rbsize = MATLAB_ENG.GetThroughputPerRB(
                            float(
                                GV.NET_STATUS_CACHE.GetNetStatus(
                                    (
                                        req.sender,
                                        self,
                                        social_group
                                    )
                                ).cqi
                            ),
                            int(NET_RB_SLOT_SYMBOLS)
                        )
                        req_rbsize_pairs.append((req, rbsize))
                    # sort with resource block size (the larger size the higher priority)
                    req_rbsize_pairs.sort(
                        reverse=True,
                        key=(
                            lambda req_rbsize_pair: req_rbsize_pair[1]
                        )
                    )
                    # required resource block bandwidth for social group msg
                    req_bw_per_rb = self.RequiredBandwidth(social_group)
                    # required timeslots for using this bandwidth
                    req_ts_per_rb = NET_RB_BW_REQ_TS[req_bw_per_rb]
                    # serve requests
                    for req_rbsize_pair in req_rbsize_pairs:
                        req = req_rbsize_pair[0]
                        rbsize = req_rbsize_pair[1]
                        total_req_rb = math.ceil(req.total_bits / rbsize)

                        for _ in range(total_req_rb):
                            # allocate
                            offset_ts = ra_oma.Allocate(
                                req_bw_per_rb, req_ts_per_rb
                            )

                            # unable to allocate
                            if(offset_ts < 0):
                                break

                            # notify request owner for granting resource
                            req.sender.UploadResourceGranted(
                                self,
                                social_group,
                                rbsize,
                                req_ts_per_rb,
                                offset_ts
                            )
                        else:
                            # if the allocation process above wasn't interrupted
                            # continue allocation for the same resource block settings
                            continue

                        # if the allocation process above was interrupted(break)
                        # then allocation for the same resource block settings(bandwidth,timeslots)
                        # will result in failure, too.
                        break
        # Clean requests
        self.sg_upload_req = ([{} for x in range(NET_QOS_CHNLS)])

    # arrange downlink resource
    def ArrangeDownlinkResource(self):
        # self.ArrangeDownlinkResourceOMA()
        self.ArrangeDownlinkResourceNOMA()

    # arrange downlink resource in OMA
    def ArrangeDownlinkResourceOMA(self):
        # OMA resource allocator
        ra_oma = ResourceAllocatorOMA(
            BS_TOTAL_BANDWIDTH[self.type]*0.9,
            NET_TS_PER_NET_STEP
        )
        # TODO: Serve Resend Requests

        # Serve Broadcast Appdatas
        for qos in range(NET_QOS_CHNLS):
            for social_group in self.sg_brdcst_datas[qos].keys():
                # if this base station has no subscribers in this social group
                if(len(self.sg_sub_vehs[social_group]) == 0):
                    # clear all broadcast appdatas of this social group
                    # cause there's no receiver
                    self.sg_brdcst_datas[qos][social_group] = []
                    continue
                # calculate the total bits for this social group to send all its broadcast appdatas
                sg_total_bits = 0
                for appdata in self.sg_brdcst_datas[qos][social_group]:
                    sg_total_bits += appdata.bits
                # if this social group has no data to broadcast
                if(sg_total_bits == 0):
                    continue
                # find the lowest cqi in the social group subscribers
                netstatus = GV.NET_STATUS_CACHE.GetMultiNetStatus([
                    (veh, self, social_group) for veh in self.sg_sub_vehs[social_group]
                ])
                lowest_cqi = netstatus[0].cqi
                for status in netstatus:
                    if(status.cqi < lowest_cqi):
                        lowest_cqi = status.cqi
                # calculate the resource block size for the cqi
                sg_rb_bits = MATLAB_ENG.GetThroughputPerRB(
                    float(lowest_cqi),
                    int(NET_RB_SLOT_SYMBOLS)
                )
                # required resource block bandwidth for this social group msg
                sg_rb_bw = self.RequiredBandwidth(social_group)
                # required timeslots for using this bandwidth
                sg_rb_ts = NET_RB_BW_REQ_TS[sg_rb_bw]
                # total required resource blocks for this social group
                sg_total_req_rb = math.ceil(sg_total_bits/sg_rb_bits)
                # allocate resource blocks
                for _ in range(sg_total_req_rb):
                    offset_ts = ra_oma.Allocate(
                        sg_rb_bw, sg_rb_ts
                    )
                    # unable to allocate
                    if(offset_ts < 0):
                        break
                    # collect appdatas this package is delivering
                    package_appdatas = []
                    remain_bits = sg_rb_bits
                    # the appdata index that is currently collecting
                    data_delivering = 0
                    # the total amount of appdatas
                    datas_count = len(self.sg_brdcst_datas[qos][social_group])
                    # start appdata collection
                    while(data_delivering < datas_count and remain_bits > 0):
                        appdata = self.sg_brdcst_datas[qos][social_group][data_delivering]
                        trans_bits = appdata.bits if appdata.bits < remain_bits else remain_bits
                        package_appdatas.append(
                            AppData(
                                appdata.header,
                                trans_bits,
                                appdata.offset
                            )
                        )
                        # consume remain bits
                        remain_bits -= trans_bits
                        # consume bits to deliver
                        appdata.bits -= trans_bits
                        # add delivered bits
                        appdata.offset += trans_bits
                        # if there's no bits to deliver move on to the next appdata
                        if(appdata.bits == 0):
                            data_delivering += 1
                    # collection done, remove appdatas that have been delivered
                    self.sg_brdcst_datas[qos][social_group] = self.sg_brdcst_datas[qos][social_group][data_delivering:]
                    # create package
                    package = NetworkPackage(
                        self,
                        BroadcastObject,
                        social_group,
                        sg_rb_bits-remain_bits,
                        package_appdatas,
                        sg_rb_ts,
                        offset_ts
                    )
                    # send package
                    for veh in self.sg_sub_vehs[social_group]:
                        veh.ReceivePackage(package)
                    # put package in process list
                    self.pkg_in_proc[LinkType.DOWNLINK].append(package)

    # arrange downlink resource in NOMA
    def ArrangeDownlinkResourceNOMA(self):
        # TODO: Serve Resend Requests

        # Simulation config for matlab optimizer
        SIM_CONF = {
            "rbf_h": float(100),
            "rbf_w": float(2),
            "max_pwr": float(BS_TRANS_PWR[self.type]),
        }
        # Qos group config for optimizer
        QoS_GP_CONF = []

        # Collect group configs
        for qos in range(NET_QOS_CHNLS):
            # a group config type in python
            QoS_GP_CONF.append([])
            for social_group in self.sg_brdcst_datas[qos].keys():
                # if this base station has no subscribers in this social group
                group_size = len(self.sg_sub_vehs[social_group])
                if(group_size == 0):
                    # clear all broadcast appdatas of this social group
                    # cause there's no receiver
                    self.sg_brdcst_datas[qos][social_group] = []
                    continue
                # calculate the total bits for this social group to send all its broadcast appdatas
                sg_total_bits = 0
                for appdata in self.sg_brdcst_datas[qos][social_group]:
                    sg_total_bits += appdata.bits
                # if this social group has no data to broadcast
                if(sg_total_bits == 0):
                    continue
                # find the lowest cqi in the social group subscribers
                netstatus = GV.NET_STATUS_CACHE.GetMultiNetStatus([
                    (veh, self, social_group) for veh in self.sg_sub_vehs[social_group]
                ])
                lowest_sinr = netstatus[0].sinr
                for status in netstatus:
                    if(status.sinr < lowest_sinr):
                        lowest_sinr = status.sinr
                # required resource block bandwidth for this social group msg
                sg_rb_bw = self.RequiredBandwidth(social_group)
                # required timeslots for using this bandwidth
                sg_rb_ts = NET_RB_BW_REQ_TS[sg_rb_bw]

                QoS_GP_CONF[-1].append({
                    "gid": float(social_group.gid),
                    "rbf_w": float(sg_rb_ts),
                    "rbf_h": float(sg_rb_bw/NET_RB_BW_UNIT),
                    "sinr_max": float(lowest_sinr),
                    "rem_bits": float(sg_total_bits),
                    "mem_num": float(group_size),
                })
            # if this qos has nothing to allocate, remove it.
            if(len(QoS_GP_CONF[-1]) == 0):
                QoS_GP_CONF.pop()

        # if none of the qos needs resource, end allocation  process.
        if(len(QoS_GP_CONF) == 0):
            return

        # create stdout receiver, save output for debug
        out = io.StringIO()
        # optimize allocation request
        gid_req_res, exitflag = MATLAB_ENG.NomaPlannerV1(
            SIM_CONF, QoS_GP_CONF, nargout=2, stdout=out
        )
        #  save output for debug
        GV.DEBUG.Log(
            "[{}][alloc]:report.\n{}".format(
                self.name,
                out.getvalue()
            )
        )

        # deliver package according to optimized allocate resource
        # TODO: improve approach(only iterate through gid_req_res rather than the whole qos).
        for qos in range(NET_QOS_CHNLS):
            for social_group in self.sg_brdcst_datas[qos].keys():
                gname = "g"+str(social_group.gid)
                if (gname in gid_req_res):
                    for t_name, val_cqi in gid_req_res[gname].items():
                        for cqi_name, rb_num in val_cqi.items():
                            # required resource block bandwidth for this social group msg
                            sg_rb_bw = self.RequiredBandwidth(social_group)
                            # required timeslots for using this bandwidth
                            sg_rb_ts = NET_RB_BW_REQ_TS[sg_rb_bw]
                            # social group resource block cqi
                            sg_rb_cqi = int(cqi_name[1:])
                            # social group rosource block size for the specified cqi
                            sg_rb_bits = MATLAB_ENG.GetThroughputPerRB(
                                sg_rb_cqi, NET_RB_SLOT_SYMBOLS
                            )
                            # the offset timeslot of the package
                            offset_ts = int(t_name[1:])

                            # start collect appdata for remaining resource
                            for _ in range(rb_num):
                                # total bits allocated for this social group
                                remain_bits = sg_rb_bits
                                # currently delivering appdata index in group
                                deliver_index = 0
                                # the total number of appdatas waiting to deliver
                                appdata_num = len(
                                    self.sg_brdcst_datas[qos][social_group]
                                )
                                # the appdatas this group cast package is going to deliver
                                package_appdatas = []
                                while(deliver_index < appdata_num and remain_bits > 0):
                                    appdata = self.sg_brdcst_datas[qos][social_group][deliver_index]
                                    # ===STATISTIC===
                                    if(appdata.offset == 0):
                                        GV.STATISTIC_RECORDER.BaseStationAppdataExitTXQ(
                                            social_group, self, appdata.header
                                        )
                                        GV.STATISTIC_RECORDER.BaseStationAppdataStartTX(
                                            social_group, self, appdata.header, offset_ts
                                        )

                                    # calculate the total bits that could actually transmit
                                    trans_bits = appdata.bits if appdata.bits < remain_bits else remain_bits
                                    # add data into package
                                    package_appdatas.append(
                                        AppData(
                                            appdata.header,
                                            trans_bits,
                                            appdata.offset
                                        )
                                    )
                                    # consume remain bits
                                    remain_bits -= trans_bits
                                    # consume bits to deliver
                                    appdata.bits -= trans_bits
                                    # add delivered bits
                                    appdata.offset += trans_bits
                                    # if there's no bits to deliver move on to the next appdata
                                    if(appdata.bits == 0):
                                        deliver_index += 1
                                        #  ===STATISTIC===
                                        GV.STATISTIC_RECORDER.BaseStationAppdataEndTX(
                                            social_group, self, appdata.header, offset_ts + sg_rb_ts
                                        )

                                # collection done, remove appdatas that have been delivered
                                self.sg_brdcst_datas[qos][social_group] = self.sg_brdcst_datas[qos][social_group][deliver_index:]
                                # create package
                                package = NetworkPackage(
                                    self,
                                    BroadcastObject,
                                    social_group,
                                    sg_rb_bits-remain_bits,
                                    package_appdatas,
                                    sg_rb_ts,
                                    offset_ts
                                )
                                # send package
                                for veh in self.sg_sub_vehs[social_group]:
                                    veh.ReceivePackage(package)
                                # put package in process list
                                self.pkg_in_proc[LinkType.DOWNLINK].append(
                                    package
                                )
                else:
                    continue

    # Function called by VehicleRecorder to deliver package to this base station
    def ReceivePackage(self, package: NetworkPackage):
        self.pkg_in_proc[LinkType.UPLINK].append(package)

    # Function called by NetworkCoreController to propagate appdata
    def ReceivePropagation(self, social_group: SocialGroup, header: AppDataHeader):
        if(social_group not in self.sg_brdcst_datas[social_group.qos]):
            self.sg_brdcst_datas[social_group.qos][social_group] = []

        self.sg_brdcst_datas[social_group.qos][social_group].append(
            AppData(
                header,
                header.total_bits,
                0
            )
        )
        # STATISTIC
        GV.STATISTIC_RECORDER.BaseStationAppdataEnterTXQ(
            social_group, self, header
        )

    # Function called by VehicleRecorder to subscribe to a specific social group on this base station
    def VehicleSubscribe(self, vehicle, social_group: SocialGroup):
        if (vehicle not in self.sg_sub_vehs[social_group]):
            self.sg_sub_vehs[social_group].append(vehicle)
        else:
            GV.ERROR.Log(
                "veh:{} subscription to bs:{} duplicated.".format(
                    vehicle.name,
                    self.name
                )
            )

    # Function called by VehicleRecorder to unsubscribe to a specific social group on this base station
    def VehicleUnsubscribe(self, vehicle, social_group: SocialGroup):
        if (vehicle in self.sg_sub_vehs[social_group]):
            self.sg_sub_vehs[social_group].remove(vehicle)
        else:
            GV.ERROR.Log(
                "veh:{} try to unsubscribe from bs:{}, but not yet subscribed.".format(
                    vehicle.name, self.name
                )
            )

    # Helper functions
    def RequiredBandwidth(self, social_group: SocialGroup):
        if (self.type == BaseStationType.UMA):
            return BS_UMA_RB_BW
        elif (self.type == BaseStationType.UMI):
            return BS_UMI_RB_BW_SG[social_group]


# The Central controller of the base station network
class NetworkCoreController:
    def __init__(self):
        self.name = "core"
        self.data_owners = {}
        self.app = NetworkCoreApplication(self)

    def PackageDelivered(self, package: NetworkPackage):
        for appdata in package.appdatas:
            self.app.RecvData(package.social_group, appdata)

    def StartPropagation(self, social_group: SocialGroup, header: AppDataHeader):
        for bs_ctrlr in GV.NET_STATION_CONTROLLER:
            bs_ctrlr.ReceivePropagation(social_group, header)
