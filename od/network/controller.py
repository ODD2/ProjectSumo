from od import social
from od.social.group import SocialGroup, QoSLevel
from od.network.misc import CastObject
from od.network.application import BaseStationApplication
from od.network.appdata import AppData, AppDataHeader
from od.network.package import NetworkPackage
from od.network.types import BaseStationType, ResourceAllocatorType, LinkType
from od.vehicle.request import UploadRequest, ResendRequest
from od.network.allocator import (ResourceAllocatorNomaApprox,
                                  ResourceAllocatorOMA,
                                  ExternAllocParam)
from od.misc.types import DebugMsgType
from od.env.config import (NET_TS_PER_NET_STEP, NET_RB_BW_REQ_TS,
                           NET_RB_SLOT_SYMBOLS, NET_RB_BW_UNIT,
                           BS_UMA_RB_BW, BS_UMI_RB_BW_QoS,
                           BS_TOTAL_BAND, BS_RADIUS,
                           BS_TRANS_PWR,
                           ALLOC_TVAL_CONST)
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
        # Map(SocialGroup:List(VehicleRecorders))
        self.sg_sub_vehs = {}

        # Upload/Download packages that're currently transmitting
        self.pkg_in_proc = [[] for i in LinkType]

        # upload requests
        self.sg_upload_req = {}

        # broadcast reqeusts
        self.sg_send_req = {}

        # store allocation parameters
        self.sg_alloc_param = {}

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
                self.PackageDelivered(pkg)
            elif timeslot == pkg.offset_ts:
                # log
                GV.DEBUG.Log(
                    "[{}][package][{}]:receive.({})",
                    (
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg
                    ),
                    DebugMsgType.NET_PKG_INFO
                )
                pkg_in_proc.append(pkg)
            else:
                pkg_in_proc.append(pkg)
        # Remove packages delivered
        self.pkg_in_proc[LinkType.UPLINK] = pkg_in_proc

    # process downlink packages
    def ProcessDownlinkPackage(self, timeslot):
        if(len(self.pkg_in_proc[LinkType.DOWNLINK]) == 0):
            return
        # Define variables
        stats_appdata_trans_beg = {}  # statistic
        stats_appdata_trans_end = {}  # statistic
        pkg_in_proc = []
        # Download
        for pkg in self.pkg_in_proc[LinkType.DOWNLINK]:
            # package end transmission
            if(timeslot == pkg.end_ts):
                # record the application data that ended transmission at current timeslot
                if(pkg.social_group not in stats_appdata_trans_end):
                    stats_appdata_trans_end[pkg.social_group] = set()
                stats_appdata_trans_end[pkg.social_group].update(
                    list(map(
                        lambda x: x.header,
                        pkg.appdatas
                    ))
                )
            # package start transmission
            elif(timeslot == pkg.offset_ts):
                GV.DEBUG.Log(
                    "[{}][package][{}]:deliver.({})",
                    (
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg
                    ),
                    DebugMsgType.NET_PKG_INFO
                )
                # record the application data that started transmission at current timeslot
                if(pkg.social_group not in stats_appdata_trans_beg):
                    stats_appdata_trans_beg[pkg.social_group] = set()
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
        # record transmission begin after recording transmission end,
        # the sequence matters!!
        for sg, appdatas in stats_appdata_trans_end.items():
            if(len(appdatas) > 0):
                GV.STATISTIC_RECORDER.BaseStationAppdataEndTX(
                    sg, self, appdatas
                )
                GV.STATISTIC_RECORDER.BaseStationAppdataEnterTXQ(
                    sg, self, appdatas
                )
        for sg, appdatas in stats_appdata_trans_beg.items():
            if(len(appdatas) > 0):
                GV.STATISTIC_RECORDER.BaseStationAppdataExitTXQ(
                    sg, self, appdatas
                )
                GV.STATISTIC_RECORDER.BaseStationAppdataStartTX(
                    sg, self, appdatas
                )

    # process delivered packages
    def PackageDelivered(self, package: NetworkPackage):
        for appdata in package.appdatas:
            self.app.RecvData(package.social_group, appdata)

    # Function called by VehicleRecorder to submit upload requests to this base station
    def ReceiveUploadRequest(self, sender, social_group: SocialGroup, total_bits: int, starv_time: float):
        if(social_group not in self.sg_upload_req):
            self.sg_upload_req[social_group] = []
        self.sg_upload_req[social_group].append(
            UploadRequest(sender, total_bits, starv_time)
        )

    # Arrange uplink resource
    def ArrangeUplinkResource(self):
        # OMA resource allocator
        ra_oma = ResourceAllocatorOMA(
            BS_TOTAL_BAND[self.type] * 0.9,
            NET_TS_PER_NET_STEP
        )
        # Serve requests
        for qos in QoSLevel:
            qos_sg_prior = [sg for sg in self.sg_upload_req.keys() if sg.qos == qos]
            if(len(qos_sg_prior) == 0):
                continue
            qos_sg_prior.sort(
                key=lambda x: min(
                    [req.starv_time for req in self.sg_upload_req[x]] + [float("inf")]
                )
            )
            for sg in qos_sg_prior:
                # Check if there exists pending requests
                if(len(self.sg_upload_req[sg]) == 0):
                    continue
                # required resource block bandwidth for social group msg
                req_bw_per_rb = self.RequiredBandwidth(sg)
                # required timeslots for using this bandwidth
                req_ts_per_rb = NET_RB_BW_REQ_TS[req_bw_per_rb]
                # the maximum rb a subframe can hold
                max_frame_rb = (
                    (BS_TOTAL_BAND[self.type] * 0.9 / req_bw_per_rb) *
                    (NET_TS_PER_NET_STEP / req_ts_per_rb)
                )
                # check if this base station has resource left
                if(ra_oma.Spare(req_bw_per_rb, req_ts_per_rb)):
                    # fetch resource block trans size for every request
                    req_rbsize_pairs = []
                    # collect the resource block size for all requests
                    for req in self.sg_upload_req[sg]:
                        rbsize = GE.GetThroughputPerRB(
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
                        key=(
                            lambda req_rbsize_pair: (
                                math.floor(req_rbsize_pair[0].starv_time * 1000) * max_frame_rb +
                                min(
                                    math.ceil(
                                        req_rbsize_pair[0].total_bits / max(
                                            req_rbsize_pair[1], 1
                                        )
                                    ),
                                    max_frame_rb
                                )
                            )
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
                            if(ts_rb_req[ts] > 0):
                                req.sender.UploadResourceGranted(
                                    self,
                                    sg,
                                    rbsize * ts_rb_req[ts],
                                    req_ts_per_rb,
                                    ts
                                )
                        # break if no further resource valid
                        # for the resource blocks of this social group
                        if rb_res_lack:
                            break
                # Clear requests
                self.sg_upload_req[sg].clear()

    def ArrangeDownlinkResource(self):
        # arrange downlink resource
        # TODO: Serve Resend Requests
        if(GV.NET_RES_ALLOC_TYPE == ResourceAllocatorType.NOMA_APR):
            self.ArrangeDownlinkNomaApprox()
        else:
            self.ArrangeDownlinkNomaOptimal()

    def ArrangeDownlinkNomaApprox(self):
        # acquire resource and qos group configuration
        RES_CONF, QoS_GP_CONF = self.PreprocessDownlinkRequest()

        # if none of the groups need resource allocation, end allocation  process.
        if(len(QoS_GP_CONF) == 0):
            return

        # create approximation resource allocator
        APPRX_ALLOCATOR = ResourceAllocatorNomaApprox(RES_CONF, QoS_GP_CONF)

        # run allocation process
        alloc_report = APPRX_ALLOCATOR()
        # create packages.
        self.DeployAllocationReport(alloc_report)

    def ArrangeDownlinkNomaOptimal(self):
        # acquire resource and qos group configuration
        RES_CONF, QoS_GP_CONF = self.PreprocessDownlinkRequest()

        # if none of the groups need resource allocation, end allocation  process.
        if(len(QoS_GP_CONF) == 0):
            return

        # create stdout receiver, save output for debug
        out = io.StringIO()
        # optimize allocation request
        try:
            future = GE.MATLAB_ENG.PlannerV1(
                RES_CONF, QoS_GP_CONF, nargout=2, stdout=out, background=True
            )
            alloc_report, exitflag = future.result(timeout=300)
        except Exception as e:
            GV.ERROR.Log(
                "[{}][alloc]:Caught Matlab Exception!\nQoS_GP_CONF:{}\nRES_CONF:{}\n".format(
                    self.name,
                    QoS_GP_CONF,
                    RES_CONF
                )
            )
            return
            # raise e
        #  save output for debug
        GV.DEBUG.Log(
            "[{}][alloc]:report.\n{}",
            (
                self.name,
                out.getvalue()
            ),
            DebugMsgType.MATLAB_INFO
        )
        # create packages.
        self.DeployAllocationReport(alloc_report)

    # Organize informations for downlink allocation process
    def PreprocessDownlinkRequest(self):
        # Radio resource configuration
        RES_CONF = {
            "rbf_h": float(round(BS_TOTAL_BAND[self.type] / NET_RB_BW_UNIT * 0.9)),
            "rbf_w": float(2),
            "max_pwr_dBm": float(BS_TRANS_PWR[self.type]),
        }
        # Qos group configuration
        QoS_GP_CONF = []
        # Collect group configs
        for qos in QoSLevel:
            # a group config type in python
            grp_config_qos = []
            # create group config for this qos
            for sg in [sg for sg in self.sg_send_req.keys() if sg.qos == qos]:
                # the members of the social group
                members = len(self.sg_sub_vehs[sg]) if sg in self.sg_sub_vehs else 0
                # required resource block bandwidth for this social group msg
                sg_rb_bw = self.RequiredBandwidth(sg)
                # required timeslots for using this bandwidth
                sg_rb_ts = NET_RB_BW_REQ_TS[sg_rb_bw]
                # calculate the total bits for this social group to send all its broadcast appdatas
                sg_total_bits = sum(
                    [data.bits for data in self.sg_send_req[sg]]
                )
                # acces external allocation params
                ext_alloc_param = self.sg_alloc_param[sg]
                # accumulate time value in ExternAllocParam for the next allocation process.
                ext_alloc_param.tval = (
                    (1 - 1 / ALLOC_TVAL_CONST) * ext_alloc_param.tval +
                    (sg_total_bits / ALLOC_TVAL_CONST)
                )
                # ignore if nothing in queue
                if(len(self.sg_send_req[sg]) == 0):
                    continue
                # if this base station has no subscribers or data to broadcast in this social group
                elif(members == 0 or sg_total_bits == 0):
                    # Statistic
                    GV.STATISTIC_RECORDER.BaseStationAppdataDrop(
                        sg,
                        self,
                        list(map(
                            lambda x: x.header,
                            self.sg_send_req[sg]
                        ))
                    )
                    # clear all broadcast appdatas of this social group
                    # cause there's no receiver
                    self.sg_send_req[sg].clear()
                    # reset time value in ExterAllocParam for the next allocation process
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
                    "qos": float(sg.qos),
                    "rbf_w": float(sg_rb_ts),
                    "rbf_h": float(sg_rb_bw / NET_RB_BW_UNIT),
                    "sinr_max": float(netstatus.max_sinr),
                    "pwr_req_dBm": (
                        float(BS_TRANS_PWR[self.type])
                        if GV.NET_RES_ALLOC_TYPE == ResourceAllocatorType.OMA else
                        float(netstatus.pwr_req_dBm)
                    ),
                    "pwr_ext_dBm": (
                        float(-100)
                        if GV.NET_RES_ALLOC_TYPE == ResourceAllocatorType.OMA else
                        float(netstatus.pwr_ext_dBm)
                    ),
                    "rem_bits": float(sg_total_bits),
                    "mem_num": float(members),
                    "eager_rate": (members * ext_alloc_param.tval) / max(sg_total_bits, 1),
                })

            # if this qos has no group requires allocate, ignore it.
            if(len(grp_config_qos) > 0):
                QoS_GP_CONF.append(grp_config_qos)

        return RES_CONF, QoS_GP_CONF

    # Create packages according to the given allocation report
    def DeployAllocationReport(self, alloc_report):
        self.PrintAllocationReport(alloc_report)
        # deliver package according to optimized allocate resource
        for gid_key, gid_items in alloc_report.items():
            sg = SocialGroup(int(gid_key[1:]))
            # required resource block bandwidth for this social group msg
            sg_rb_bw = self.RequiredBandwidth(sg)
            # required timeslots for using this bandwidth
            sg_rb_ts = NET_RB_BW_REQ_TS[sg_rb_bw]
            max_frame_bits = (
                (BS_TOTAL_BAND[self.type] * 0.9 / sg_rb_bw) * 933 *
                (NET_TS_PER_NET_STEP / sg_rb_ts)
            )
            self.sg_send_req[sg].sort(
                key=lambda appdata: (
                    (math.floor(appdata.header.at * 1000) * max_frame_bits) +
                    min(appdata.bits, max_frame_bits)
                )
            )
            # create package target receiver name list for speedup.
            CastObject.name = "|".join([v.name for v in self.sg_sub_vehs[sg]])
            for ts_key, ts_items in gid_items.items():
                # the offset timeslot of the package
                offset_ts = int(ts_key[1:])
                # the total bits avialable for the current timeslot setting
                total_bits = 0
                # collect available transmit resource for the current timeslot setting.
                for cqi_key, rb_num in ts_items.items():
                    # social group resource block cqi
                    sg_rb_cqi = int(cqi_key[1:])
                    # social group rosource block size for the specified cqi
                    total_bits += round(
                        GE.GetThroughputPerRB(
                            sg_rb_cqi, NET_RB_SLOT_SYMBOLS
                        )
                    ) * rb_num
                # allocate resource to create package for current timeslot.
                # the remaining resource in bits.
                remain_bits = total_bits
                # currently delivering appdata index in group
                deliver_index = 0
                # the total number of appdatas waiting to deliver
                appdata_num = len(
                    self.sg_send_req[sg]
                )
                # ignore if no appdata allocate resource.
                if(appdata_num == 0):
                    continue
                # the appdatas this group cast package is going to deliver
                package_appdatas = []
                while(deliver_index < appdata_num and remain_bits > 0):
                    appdata = self.sg_send_req[sg][deliver_index]
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
                            sg,
                            self,
                            [appdata.header]
                        )
                # collection done, remove appdatas that have been delivered
                self.sg_send_req[sg] = self.sg_send_req[sg][deliver_index:]
                # ignore if no appdata data to package.
                if(len(package_appdatas) == 0):
                    continue
                # create package
                package = self.CreatePackage(
                    self,
                    CastObject,
                    sg,
                    total_bits - remain_bits,
                    package_appdatas,
                    sg_rb_ts,
                    offset_ts
                )
                # send package
                for veh in self.sg_sub_vehs[sg]:
                    veh.ReceivePackage(package)
                # put package in process list
                self.pkg_in_proc[LinkType.DOWNLINK].append(
                    package
                )

    # Record allocation result
    def PrintAllocationReport(self, alloc_report):
        # Construct Formatted Report
        report = "{\n"
        for gid_key, gid_items in alloc_report.items():
            sg = SocialGroup(int(gid_key[1:]))
            report += " ===== {}({}) =====\n".format(sg.fname.upper(), sg.gid)
            for ts_key, ts_items in gid_items.items():
                for cqi_key, rb_num in ts_items.items():
                    report += "  {}t/cqi:{}, num:{}\n".format(ts_key[1:], cqi_key[1:], rb_num)

        report += "}\n"
        # Log
        GV.DEBUG.Log(
            "[{}][alloc]:report.\n{}",
            (
                self.name,
                report
            ),
            DebugMsgType.NET_ALLOC_INFO
        )

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
            "[{}][package][{}]:create.({})",
            (
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
    def Propagate(self, sender, social_group: SocialGroup, header: AppDataHeader):
        if(social_group not in self.sg_send_req):
            self.sg_send_req[social_group] = []
            self.sg_alloc_param[social_group] = ExternAllocParam()

        self.sg_send_req[social_group].append(
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
        if(social_group not in self.sg_sub_vehs):
            self.sg_sub_vehs[social_group] = []
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
        if(social_group not in self.sg_sub_vehs):
            # vehicle should create social group during subscription.
            raise Exception("VehicleUnsubscribe: SocialGroup not found.")
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
            return BS_UMI_RB_BW_QoS[social_group.qos]


# The Central controller of the base station network
class NetworkCoreController:
    def __init__(self):
        self.name = "core"
        self.umi_approx_uma = {}
        # self.app = NetworkCoreApplication(self)

    # helper function for UMI to find the nearest UMA for c2g traffic propagations.
    def MapApproximityUMA(self, umi_bs):
        if(not umi_bs.type == BaseStationType.UMI):
            raise Exception("Try to Map Non-UMI to Approximate UMAs")
        approx_bs = None
        distance = float("Inf")
        for uma_bs in [bs for bs in GV.NET_STATION_CONTROLLER if bs.type == BaseStationType.UMA]:
            d = pow((uma_bs.pos[0] - umi_bs.pos[0])**2 + (uma_bs.pos[1] - umi_bs.pos[1])**2, 0.5)
            if(d < distance):
                approx_bs = uma_bs
        return approx_bs

    # called by UMIs to propagate critical data to UMA as general data.
    def Propagate(self, sender, social_group: SocialGroup, header: AppDataHeader):
        if(sender.type == BaseStationType.UMI and social_group.qos == QoSLevel.CRITICAL):
            # find the approximity uma for umi
            if(sender not in self.umi_approx_uma):
                self.umi_approx_uma[sender] = self.MapApproximityUMA(sender)
            # propagate only to the uma closest to the sender umi.
            if(GV.NET_QoS_RE_CLS):
                GV.STATISTIC_RECORDER.CoreStationConvertQoS(header, social_group, SocialGroup.RCWS)
                self.umi_approx_uma[sender].Propagate(
                    self,
                    SocialGroup.RCWS,
                    header
                )
            else:
                self.umi_approx_uma[sender].Propagate(
                    self,
                    social_group,
                    header
                )
        elif(sender.type == BaseStationType.UMA and social_group.qos == QoSLevel.GENERAL):
            for uma_bs in [bs for bs in GV.NET_STATION_CONTROLLER if bs.type == BaseStationType.UMA]:
                if(uma_bs == sender):
                    continue
                uma_bs.Propagate(self, social_group, header)
        else:
            raise Exception("Core receive propagate from Non-UMI base station")

    # def PackageDelivered(self, package: NetworkPackage):
    #     for appdata in package.appdatas:
    #         self.app.RecvData(package.social_group, appdata)

    # def StartPropagation(self, sender, social_group: SocialGroup, header: AppDataHeader):
    #     # Propagate all data to UMA as road condition warning(RCW) data.
    #     for bs_ctrlr in [bs for bs in GV.NET_STATION_CONTROLLER if bs.type == BaseStationType.UMA]:
    #         bs_ctrlr.Propagate(SocialGroup.RCWS, header)
