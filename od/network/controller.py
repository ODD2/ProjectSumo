from od.social import SocialGroup
from od.network.types import LinkType
from od.network.application import NetworkCoreApplication, BaseStationApplication
from od.network.appdata import AppData, AppDataHeader
from od.network.package import NetworkPackage
from od.network.types import BroadcastObject, BaseStationType, ResourceAllocatorType
from od.vehicle.request import UploadRequest, ResendRequest
from od.network.allocator import ResourceAllocatorOMA
from od.misc.types import DebugMsgType
from od.config import (NET_TS_PER_NET_STEP, NET_QOS_CHNLS, NET_RB_BW_REQ_TS,
                       NET_RB_SLOT_SYMBOLS, NET_RB_BW_UNIT,
                       BS_UMA_RB_BW, BS_UMI_RB_BW_SG,
                       BS_TOTAL_BAND, BS_RADIUS,
                       BS_TRANS_PWR)
import od.engine as GE
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

        # Base station application
        self.app = BaseStationApplication(self)

        # Vehicles that've subscribed to specific social groups
        self.sg_sub_vehs = [[] for i in SocialGroup]

        # Upload/Download packages that're currently transmitting
        self.pkg_in_proc = [[] for i in LinkType]

        # upload requests
        self.sg_upload_req = ([{} for x in range(NET_QOS_CHNLS)])
        for sg in SocialGroup:
            self.sg_upload_req[sg.qos][sg] = []

        # broadcast reqeusts
        self.sg_brdcst_datas = ([{} for x in range(NET_QOS_CHNLS)])
        for sg in SocialGroup:
            self.sg_brdcst_datas[sg.qos][sg] = []

        # TODO: resend requests
        # self.sg_resend_req = ([[] for x in SocialGroup])

    def __index__(self):
        return self.serial

    # Called every sumo step
    def UpdateSS(self):
        pass

    # Called every network step
    def UpdateNS(self, ns):
        self.ArrangeUplinkResource()
        self.ArrangeDownlinkResource()

    # Called every timeslot
    def UpdateT(self, ts):
        self.ProcessPackage(ts)

    # process packages
    def ProcessPackage(self, timeslot):
        self.ProcessUplinkPackage(timeslot)
        self.ProcessDownlinkPackage(timeslot)

    # process uplink packages
    def ProcessUplinkPackage(self, timeslot):
        if(len(self.pkg_in_proc[LinkType.UPLINK]) == 0):
            return
        # Define
        pkg_in_proc = []
        # Upload
        for pkg in self.pkg_in_proc[LinkType.UPLINK]:
            if timeslot == pkg.end_ts:
                # log
                GV.DEBUG.Log(
                    "[{}][package][{}]:receive.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg
                    ),
                    DebugMsgType.NET_PKG_INFO
                )
                self.PackageDelivered(pkg)
            else:
                pkg_in_proc.append(pkg)
        # Remove packages delivered
        self.pkg_in_proc[LinkType.UPLINK] = pkg_in_proc

    # process downlink packages
    def ProcessDownlinkPackage(self, timeslot):
        if(len(self.pkg_in_proc[LinkType.DOWNLINK]) == 0):
            return
        # Define variables
        stats_appdata_trans_beg = [set() for _ in SocialGroup]  # statistic
        stats_appdata_trans_end = [set() for _ in SocialGroup]  # statistic
        pkg_in_proc = []
        # Download
        for pkg in self.pkg_in_proc[LinkType.DOWNLINK]:
            # package end transmission
            if(timeslot == pkg.end_ts):
                # record the application data that ended transmission at current timeslot
                stats_appdata_trans_end[pkg.social_group].update(
                    list(map(
                        lambda x: x.header,
                        pkg.appdatas
                    ))
                )
            # package start transmission
            elif(timeslot == pkg.offset_ts):
                GV.DEBUG.Log(
                    "[{}][package][{}]:deliver.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg
                    ),
                    DebugMsgType.NET_PKG_INFO
                )
                # record the application data that ended transmission at current timeslot
                stats_appdata_trans_beg[pkg.social_group].update(
                    list(map(
                        lambda x: x.header,
                        pkg.appdatas
                    ))
                )
                pkg_in_proc.append(pkg)
            # package transmitting
            else:
                pkg_in_proc.append(pkg)
        # Remove packages sent
        self.pkg_in_proc[LinkType.DOWNLINK] = pkg_in_proc
        # Statistic
        for sg in SocialGroup:
            # record transmission begin after recording transmission end,
            # the sequence matters!!
            if(len(stats_appdata_trans_end[sg]) > 0):
                GV.STATISTIC_RECORDER.BaseStationAppdataEndTX(
                    sg, self, stats_appdata_trans_end[sg]
                )
                GV.STATISTIC_RECORDER.BaseStationAppdataEnterTXQ(
                    sg, self, stats_appdata_trans_end[sg]
                )
            if(len(stats_appdata_trans_beg[sg]) > 0):
                GV.STATISTIC_RECORDER.BaseStationAppdataExitTXQ(
                    sg, self, stats_appdata_trans_beg[sg]
                )
                GV.STATISTIC_RECORDER.BaseStationAppdataStartTX(
                    sg, self, stats_appdata_trans_beg[sg]
                )

    # process delivered packages
    def PackageDelivered(self, package: NetworkPackage):
        for appdata in package.appdatas:
            self.app.RecvData(package.social_group, appdata)

    # Function called by VehicleRecorder to submit upload requests to this base station
    def ReceiveUploadRequest(self, sender, social_group: SocialGroup, total_bits: int):
        self.sg_upload_req[social_group.qos][social_group].append(
            UploadRequest(sender, total_bits)
        )

    # arrange uplink resource
    def ArrangeUplinkResource(self):
        # OMA resource allocator
        ra_oma = ResourceAllocatorOMA(
            BS_TOTAL_BAND[self.type]*0.9,
            NET_TS_PER_NET_STEP
        )
        # Serve requests
        for qos in range(NET_QOS_CHNLS):
            for sg in self.sg_upload_req[qos].keys():
                # Check if there exists pending requests
                if(len(self.sg_upload_req[qos][sg]) == 0):
                    continue
                # required resource block bandwidth for social group msg
                req_bw_per_rb = self.RequiredBandwidth(sg)
                # required timeslots for using this bandwidth
                req_ts_per_rb = NET_RB_BW_REQ_TS[req_bw_per_rb]
                # check if this base station has resource left
                if(ra_oma.Spare(req_bw_per_rb, req_ts_per_rb)):
                    # fetch resource block trans size for every request
                    req_rbsize_pairs = []
                    # collect the resource block size for all requests
                    for req in self.sg_upload_req[qos][sg]:
                        rbsize = GE.MATLAB_ENG.GetThroughputPerRB(
                            float(
                                GV.NET_STATUS_CACHE.GetNetStatus(
                                    (
                                        req.sender,
                                        self,
                                        sg
                                    )
                                ).max_cqi
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
                    # serve requests
                    rb_res_lack = False
                    for req_rbsize_pair in req_rbsize_pairs:
                        req = req_rbsize_pair[0]
                        rbsize = req_rbsize_pair[1]
                        # further requests are unable to serve
                        if(rbsize == 0):
                            break
                        max_rb_req = math.ceil(req.total_bits / rbsize)
                        ts_rb_req = [0 for _ in range(NET_TS_PER_NET_STEP)]
                        # allocate resource block
                        for _ in range(max_rb_req):
                            # try allocate
                            offset_ts = ra_oma.Allocate(
                                req_bw_per_rb, req_ts_per_rb
                            )
                            # allocate failed
                            if(offset_ts < 0):
                                rb_res_lack = True
                                break
                            # allocate success
                            ts_rb_req[offset_ts] += 1
                        # notify request owner for granted resources
                        for ts in range(NET_TS_PER_NET_STEP):
                            while(ts_rb_req[ts] > 0):
                                req.sender.UploadResourceGranted(
                                    self,
                                    sg,
                                    rbsize,
                                    req_ts_per_rb,
                                    ts
                                )
                                ts_rb_req[ts] -= 1
                        # break if no further resource valid
                        # for the resource blocks of this social group
                        if rb_res_lack:
                            break
                # Clear requests
                self.sg_upload_req[qos][sg].clear()

    # arrange downlink resource
    def ArrangeDownlinkResource(self):
        if (GV.NET_RES_ALLOC_TYPE == ResourceAllocatorType.OMA):
            self.ArrangeDownlinkResourceOMA()
        elif (GV.NET_RES_ALLOC_TYPE == ResourceAllocatorType.NOMA_OPT):
            self.ArrangeDownlinkResourceNOMA()

    # arrange downlink resource in OMA
    def ArrangeDownlinkResourceOMA(self):
        # OMA resource allocator
        ra_oma = ResourceAllocatorOMA(
            BS_TOTAL_BAND[self.type]*0.9,
            NET_TS_PER_NET_STEP
        )
        # TODO: Serve Resend Requests

        # Serve Broadcast Appdatas
        for qos in range(NET_QOS_CHNLS):
            for sg in self.sg_brdcst_datas[qos].keys():
                # if there's no appdata to broadcast for this social group
                if(len(self.sg_brdcst_datas[qos][sg]) == 0):
                    continue
                # the member of the social group
                members = len(self.sg_sub_vehs[sg])
                # required resource block bandwidth for this social group msg
                sg_rb_bw = self.RequiredBandwidth(sg)
                # required timeslots for using this bandwidth
                sg_rb_ts = NET_RB_BW_REQ_TS[sg_rb_bw]
                # calculate the total bits for this social group to send all its broadcast appdatas
                sg_rem_bits = sum(
                    data.bits for data in self.sg_brdcst_datas[qos][sg]
                )
                # if this base station has no subscribers or unsent data in this social group
                if(members == 0 or sg_rem_bits == 0):
                    GV.STATISTIC_RECORDER.BaseStationAppdataDrop(
                        sg,
                        self,
                        list(map(
                            lambda x: x.header,
                            self.sg_brdcst_datas[qos][sg]
                        ))
                    )
                    # clear all broadcast appdatas of this social group
                    # cause there's no receiver
                    self.sg_brdcst_datas[qos][sg].clear()
                    continue
                # if there's no resource for this social group
                if(not ra_oma.Spare(sg_rb_bw, sg_rb_ts)):
                    continue

                # fetch all the vehicle network status
                net_status = GV.NET_STATUS_CACHE.GetMultiNetStatus([
                    (veh, self, sg) for veh in self.sg_sub_vehs[sg]
                ])
                #  find the minimum cqi among all the vehicles
                cqi_min_of_all_member = min(
                    status.max_cqi for status in net_status)
                #  the minimum cqi is zero! this social group is unable to serve!
                #  or else some vehicle will not receive data.
                if(cqi_min_of_all_member == 0):
                    continue
                # calculate resource block size for minimum cqi
                sg_rb_bits = GE.MATLAB_ENG.GetThroughputPerRB(
                    float(cqi_min_of_all_member),
                    int(NET_RB_SLOT_SYMBOLS)
                )
                # total required resource blocks for this social group
                sg_max_req_rb = math.ceil(sg_rem_bits/sg_rb_bits)
                # allocate resource blocks
                sg_ts_req_rb = [0 for _ in range(NET_TS_PER_NET_STEP)]
                for _ in range(sg_max_req_rb):
                    offset_ts = ra_oma.Allocate(
                        sg_rb_bw, sg_rb_ts
                    )
                    # unable to allocate
                    if(offset_ts < 0):
                        break
                    # allocate successful
                    sg_ts_req_rb[offset_ts] += 1
                # deploy resource and create packages
                for ts in range(NET_TS_PER_NET_STEP):
                    while(sg_ts_req_rb[ts] > 0):
                        # consume resource block
                        sg_ts_req_rb[ts] -= 1
                        # collect appdatas this package is delivering
                        package_appdatas = []
                        remain_bits = sg_rb_bits
                        # the appdata index that is currently collecting
                        data_i = 0
                        data_num = len(self.sg_brdcst_datas[qos][sg])
                        # collect package appdata
                        while (data_i < data_num and remain_bits > 0):
                            appdata = self.sg_brdcst_datas[qos][sg][data_i]
                            # actual transmit bit
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
                            # appdata totally delivered, serve next appdata
                            if appdata.bits == 0:
                                data_i += 1
                                # Statistic - appdata serve timestamp
                                GV.STATISTIC_RECORDER.BaseStationAppdataServe(
                                    sg,
                                    self,
                                    [appdata.header]
                                )
                        # remove appdatas in collection
                        self.sg_brdcst_datas[qos][sg] = self.sg_brdcst_datas[qos][sg][data_i:]
                        # create package
                        package = self.CreatePackage(
                            self,
                            BroadcastObject,
                            sg,
                            sg_rb_bits-remain_bits,
                            package_appdatas,
                            sg_rb_ts,
                            ts,
                        )
                        # put package in process list
                        self.pkg_in_proc[LinkType.DOWNLINK].append(package)
                        # send package
                        for veh in self.sg_sub_vehs[sg]:
                            veh.ReceivePackage(package)

    # arrange downlink resource in NOMA
    def ArrangeDownlinkResourceNOMA(self):
        # DEBUG
        # if(self.name == "bs4" and GV.SUMO_SIM_INFO.getTime() > 272.0125):
        #     a = 0

        # TODO: Serve Resend Requests
        # Simulation config for matlab optimizer
        SIM_CONF = {
            "rbf_h": float(round(BS_TOTAL_BAND[self.type]/NET_RB_BW_UNIT*0.9)),
            "rbf_w": float(2),
            "max_pwr_dBm": float(BS_TRANS_PWR[self.type]),
        }
        # Qos group config for optimizer
        QoS_GP_CONF = []
        # Collect group configs
        for qos in range(NET_QOS_CHNLS):
            # a group config type in python
            grp_config_qos = []
            # create group config for this qos
            for sg in self.sg_brdcst_datas[qos].keys():
                # ignore if nothing in queue
                if(len(self.sg_brdcst_datas[qos][sg]) == 0):
                    continue
                # the members of the social group
                members = len(self.sg_sub_vehs[sg])
                # required resource block bandwidth for this social group msg
                sg_rb_bw = self.RequiredBandwidth(sg)
                # required timeslots for using this bandwidth
                sg_rb_ts = NET_RB_BW_REQ_TS[sg_rb_bw]
                # calculate the total bits for this social group to send all its broadcast appdatas
                sg_total_bits = sum(
                    data.bits for data in self.sg_brdcst_datas[qos][sg]
                )
                # if this base station has no subscribers or data to broadcast in this social group
                if(members == 0 or sg_total_bits == 0):
                    # Statistic
                    GV.STATISTIC_RECORDER.BaseStationAppdataDrop(
                        sg,
                        self,
                        list(map(
                            lambda x: x.header,
                            self.sg_brdcst_datas[qos][sg]
                        ))
                    )
                    # clear all broadcast appdatas of this social group
                    # cause there's no receiver
                    self.sg_brdcst_datas[qos][sg].clear()
                    continue

                # find the lowest cqi in the social group subscribers
                list_net_status = GV.NET_STATUS_CACHE.GetMultiNetStatus([
                    (veh, self, sg) for veh in self.sg_sub_vehs[sg]
                ])
                # find the minimum cqi among all members
                netstatus = min(list_net_status, key=lambda x: x.max_cqi)
                #  the minimum cqi is zero! this social group is unable to serve!
                #  or else some vehicle will not receive data.
                if(netstatus.max_cqi == 0):
                    continue
                # create group config for allocator
                grp_config_qos.append({
                    "gid": float(sg.gid),
                    "rbf_w": float(sg_rb_ts),
                    "rbf_h": float(sg_rb_bw/NET_RB_BW_UNIT),
                    "sinr_max": float(netstatus.max_sinr),
                    "pwr_req_dBm": float(netstatus.pwr_req_dBm),
                    "pwr_ext_dBm":  float(netstatus.pwr_ext_dBm),
                    "rem_bits": float(sg_total_bits),
                    "mem_num": float(members),
                })
            # if this qos has no group requires allocate, remove it.
            if(len(grp_config_qos) > 0):
                QoS_GP_CONF.append(grp_config_qos)

        # if none of the groups need resource allocation, end allocation  process.
        if(len(QoS_GP_CONF) == 0):
            return

        # create stdout receiver, save output for debug
        out = io.StringIO()
        # optimize allocation request
        gid_req_res, exitflag = GE.MATLAB_ENG.NomaPlannerV1(
            SIM_CONF, QoS_GP_CONF, nargout=2, stdout=out
        )
        #  save output for debug
        GV.DEBUG.Log(
            "[{}][alloc]:report.\n{}".format(
                self.name,
                out.getvalue()
            ),
            DebugMsgType.NET_ALLOC_INFO
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
                            sg_rb_bits = GE.MATLAB_ENG.GetThroughputPerRB(
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
                                        # Statistic - appdata serve timestamp
                                        GV.STATISTIC_RECORDER.BaseStationAppdataServe(
                                            social_group,
                                            self,
                                            [appdata.header]
                                        )
                                # collection done, remove appdatas that have been delivered
                                self.sg_brdcst_datas[qos][social_group] = self.sg_brdcst_datas[qos][social_group][deliver_index:]
                                # create package
                                package = self.CreatePackage(
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

    # Create package
    def CreatePackage(self, src, dest, social_group: SocialGroup, total_bits, appdatas, trans_ts, offset_ts):
        # create package
        package = NetworkPackage(
            src,
            dest,
            social_group,
            total_bits,
            appdatas,
            trans_ts,
            offset_ts
        )

        # log
        GV.DEBUG.Log(
            "[{}][package][{}]:create.({})".format(
                self.name,
                social_group.fname.lower(),
                package
            ),
            DebugMsgType.NET_PKG_INFO
        )

        # Create Package
        return package

    # Function called by VehicleRecorder to deliver package to this base station
    def ReceivePackage(self, package: NetworkPackage):
        self.pkg_in_proc[LinkType.UPLINK].append(package)

    # Function called by NetworkController/BaseStationApplication to propagate appdata.
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
        # Statistic
        GV.STATISTIC_RECORDER.BaseStationAppdataEnterTXQ(
            social_group, self, [header]
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
        # self.app = NetworkCoreApplication(self)

    # called by UMIs to propagate critical data to UMA.
    def ReceivePropagation(self, social_group: SocialGroup, header: AppDataHeader):
        self.StartPropagation(social_group, header)

    # def PackageDelivered(self, package: NetworkPackage):
    #     for appdata in package.appdatas:
    #         self.app.RecvData(package.social_group, appdata)

    def StartPropagation(self, social_group: SocialGroup, header: AppDataHeader):
        # Propagate all data to UMA as general data.
        for bs_ctrlr in [bs for bs in GV.NET_STATION_CONTROLLER if bs.type == BaseStationType.UMA]:
            bs_ctrlr.ReceivePropagation(SocialGroup.GENERAL, header)
