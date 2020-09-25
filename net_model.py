import os
import sys
import matlab.engine
import math
import numpy as np
import traci
from copy import copy
from net_pack import NetworkTransmitRequest, NetworkTransmitResponse, PackageProcessing, NetworkPackage
from globs import *


class NetStatus:
    def __init__(self):
        self.cached = False
        self.cqi = 0
        self.sinr = 0


class NetStatusCache:
    def __init__(self):
        self._map = {}

    # param [(vehicle,bs_ctrlr,social_group)]
    def GetMultiNetStatus(self, query_tuples):
        result = []
        for query_tuple in query_tuples:
            result.append(self.GetNetStatus(query_tuple))
        return result

    # param [(vehicle,bs_ctrlr,social_group)]
    def GetNetStatus(self, query_tuple):
        if query_tuple[0].name not in self._map:
            raise Exception("Error! vehicle should be in the map!!")

        net_stat = self._map[query_tuple[0].name][query_tuple[1].serial][query_tuple[2]]
        if (not net_stat.cached):
            (net_stat.cqi, net_stat.sinr) = GET_BS_CQI_SINR_5G(
                query_tuple[0],
                query_tuple[1],
                query_tuple[2])
            net_stat.cached = True
        return net_stat

    def Initialize(self):
        globals()
        # remove ghosts
        for veh_id in SIM_STEP_INFO.ghost_veh_ids:
            self._map.pop(veh_id)
        # add new vehicles
        for veh_id in SIM_STEP_INFO.new_veh_ids:
            self._map[veh_id] = [
                [NetStatus() for sg in SocialGroup]
                for i in range(len(BASE_STATION_CONTROLLER))
            ]
        # initialize
        for veh_status_list in self._map.values():
            for bs_idx in range(len(BASE_STATION_CONTROLLER)):
                for sg in SocialGroup:
                    veh_status_list[bs_idx][sg].cached = False


# class ReceiverState:
#     def __init__(self, recvr):
#         self.bits_sent = 0
#         self.recvr = recvr


class SocialGroupBroadcastRequest:
    def __init__(self, package, recvrs):
        self.package = package
        self.recvrs = [
            recvr
            for recvr in recvrs
            if recvr != package.owner
        ]


class BaseStationController:
    def __init__(self, name, pos, bs_type, serial):
        # Base station paremeters
        self.name = name
        self.pos = pos
        self.radius = BS_UMI_RADIUS if bs_type == BaseStationType.UMI else BS_UMA_RADIUS
        self.type = bs_type
        self.serial = serial

        # vehicles that've subscribed to specific social groups
        self.sbscrb_social_vehs = [[] for i in SocialGroup]

        # Upload/Download packages that're currently transmitting
        self.pkg_in_proc = [[] for i in LinkType]

        # request for sending to other objects
        self.sg_broadcast_req = (
            [[] for x in range(len(SocialGroup))]
        )

        self.Reset()

    def Update(self):
        self.ServePackage()
        self.CreateBroadcastRequest()
        # TODO: Propagate
        self.ServeBroadcastRequest()
        self.ServeUploadRequest()
        # Reset
        self.Reset()

    # Serves uploading/downloading packages
    def ServePackage(self):
        for link_type in LinkType:
            pkg_procs_done = []
            for pkg_proc in self.pkg_in_proc[link_type]:
                # consume time slot
                pkg_proc.time_slots -= 1
                package = pkg_proc.package
                # consume bandwidth
                self.valid_bandwidth[link_type] -= self.RequiredBandwidth(
                    package.social_group
                )
                if(pkg_proc.time_slots == 0):
                    # package that has done transmitting are collected
                    pkg_procs_done.append(pkg_proc)
                    # if the package is uploaded
                    if(link_type == LinkType.UPLOAD):
                        local_pckg = copy(package)
                        local_pckg.bits = pkg_proc.proc_bits
                        # Save to local
                        self.recv_package.append(local_pckg)

                    # log
                    print(
                        "{}-{}: type:{} target:{} origin:{}-{}*-{}b-{}-{}s ".format(
                            SIM_STEP_INFO.time,
                            self.name,
                            link_type.name.lower(),
                            pkg_proc.opponent.name,
                            package.owner.name,
                            package.name,
                            pkg_proc.proc_bits,
                            SocialGroup(package.social_group).name.lower(),
                            package.at,
                        )
                    )

            # remove transmitted packages
            for pkg_proc in pkg_procs_done:
                # remove packages that has done transmitting
                self.pkg_in_proc[link_type].remove(pkg_proc)

    # Function called by VehicleRecorder to submit upload requests to this base station
    def Upload(self, package):
        self.sg_upload_req[package.social_group].append(package)

    # Serve submitted upload requests
    def ServeUploadRequest(self):
        globals()
        for social_group in SocialGroup:
            # Check if there exists pending requests
            if len(self.sg_upload_req[social_group]) > 0:
                # required resource block bandwidth for social group msg
                req_bandwidth_per_rb = self.RequiredBandwidth(social_group)
                # required timeslot for using this bandwidth
                time_slots = NET_RB_BANDWIDTH_TS[req_bandwidth_per_rb]

                # fetch transmission size for each request
                req_txs_list = []
                for package in self.sg_upload_req[social_group]:
                    trans_rate = MATLAB_ENG.GetThroughputPerRB(
                        float(NET_STATUS_CACHE.GetNetStatus(
                            (
                                package.owner,
                                self,
                                social_group
                            )
                        ).cqi),
                        int(NET_RB_SLOT_SYMBOLS)
                    )
                    req_txs_list.append((package, trans_rate))

                # sort with trans size
                req_txs_list.sort(
                    reverse=True,
                    key=(
                        lambda req_txr: req_txr[1]
                    )
                )

                # serve requests
                for req_txs in req_txs_list:
                    package = req_txs[0]
                    rb_trans_size = req_txs[1]
                    if self.valid_bandwidth[LinkType.UPLOAD] < req_bandwidth_per_rb:
                        # notify request owner
                        package.owner.UploadRequestResponse(
                            self,
                            package,
                            0,
                            0
                        )
                    else:
                        # allocate resource block for transmit request

                        # the useable resource blocks
                        valid_resource_blocks = math.floor(
                            self.valid_bandwidth[LinkType.UPLOAD] /
                            req_bandwidth_per_rb
                        )

                        # available total transmission size
                        valid_trans_size = rb_trans_size * valid_resource_blocks

                        # the actual transmission size
                        trans_size = valid_trans_size if valid_trans_size < package.bits else package.bits
                        total_required_bandwidth = (req_bandwidth_per_rb *
                                                    math.ceil(trans_size/rb_trans_size))
                        # consume required bandwidth
                        self.valid_bandwidth[LinkType.UPLOAD] -= total_required_bandwidth

                        # reply request owner
                        package.owner.UploadRequestResponse(
                            self,
                            package,
                            trans_size,
                            time_slots
                        )
                        # create package to process
                        self.pkg_in_proc[LinkType.UPLOAD].append(
                            PackageProcessing(
                                package,
                                package.owner,
                                trans_size,
                                time_slots
                            )
                        )

    def CreateBroadcastRequest(self):
        for package in self.recv_package:
            social_group = package.social_group
            self.sg_broadcast_req[social_group].append(
                SocialGroupBroadcastRequest(
                    package,
                    self.sbscrb_social_vehs[social_group]
                )
            )

    def ServeBroadcastRequest(self):
        globals()
        for social_group in SocialGroup:
            # record broadcast requests that're done
            brdcst_reqs_done = []
            # required resource block bandwidth for social group msg
            req_bandwidth_per_rb = self.RequiredBandwidth(social_group)
            # required timeslot for using this bandwidth
            time_slots = NET_RB_BANDWIDTH_TS[req_bandwidth_per_rb]
            for req_brdcst in self.sg_broadcast_req[social_group]:
                # Not enought bandwidth for this type of social group request
                if self.valid_bandwidth[LinkType.DOWNLOAD] < req_bandwidth_per_rb:
                    break

                package = req_brdcst.package

                # Record receivers that're out of service
                out_of_service_recvrs = []

                # Find the lowest cqi in receiver lists
                lowest_cqi_in_recvrs = 30
                for recvr in req_brdcst.recvrs:
                    # Check if this receiver is still in service
                    if recvr.name not in SIM_STEP_INFO.veh_ids:
                        out_of_service_recvrs.append(recvr)
                        continue
                    # Get net status of the recvr
                    net_status = NET_STATUS_CACHE.GetNetStatus(
                        (recvr, self, social_group)
                    )
                    # Check if net status cqi is lower
                    if(net_status.cqi < lowest_cqi_in_recvrs):
                        lowest_cqi_in_recvrs = net_status.cqi

                # remove out of service receivers
                for recvr in out_of_service_recvrs:
                    req_brdcst.recvrs.remove(recvr)

                # broadcast request done if theirs no one to serve
                if(len(req_brdcst.recvrs) == 0):
                    brdcst_reqs_done.append(req_brdcst)
                    continue

                # The maximum transmission size per resource-block according to cqi
                rb_trans_size = MATLAB_ENG.GetThroughputPerRB(
                    float(lowest_cqi_in_recvrs),
                    int(NET_RB_SLOT_SYMBOLS)
                )

                # total resource blocks valid for this type of social message
                valid_resource_blocks = math.floor(
                    self.valid_bandwidth[LinkType.UPLOAD] /
                    req_bandwidth_per_rb
                )

                # available total transmission size
                valid_trans_size = rb_trans_size * valid_resource_blocks

                # the actual transmission size
                trans_size = valid_trans_size if valid_trans_size < package.bits else package.bits

                # the total required bandwidth
                total_required_bandwidth = (req_bandwidth_per_rb *
                                            math.ceil(trans_size/rb_trans_size))

                # consume required bandwidth
                self.valid_bandwidth[LinkType.DOWNLOAD] -= total_required_bandwidth

                # remove transmitted size
                package.bits -= trans_size

                for recvr in req_brdcst.recvrs:
                    # notify receiver
                    recvr.ReceivePackage(
                        self,
                        package,
                        trans_size,
                        time_slots
                    )

                    # package in process
                    self.pkg_in_proc[LinkType.DOWNLOAD].append(
                        PackageProcessing(
                            package,
                            recvr,
                            trans_size,
                            time_slots
                        )
                    )

                # broadcast request done if all data have been transmitted
                if package.bits == 0:
                    brdcst_reqs_done.append(req_brdcst)
                    continue
            # remove completed broadcast requests
            for req_brdcst in brdcst_reqs_done:
                self.sg_broadcast_req[social_group].remove(req_brdcst)

    def PropagateSocialPackage(self, cloud):
        a = 0

    def ReceivePropagation(self):
        a = 0

    # The reset function
    def Reset(self):
        # request for uploading to this base station
        self.sg_upload_req = (
            [[] for x in SocialGroup]
        )
        # valid bandwidth for next timeslot (0.5ms per timeslot)
        self.valid_bandwidth = [BS_ALL_BANDWIDTH *
                                0.9 for i in LinkType]
        self.recv_package = []

    # Function called by VehicleRecorder to subscribe to a specific social group on this base station
    def VehicleSubscribe(self, vehicle, social_group):
        if(vehicle not in self.sbscrb_social_vehs[social_group]):
            self.sbscrb_social_vehs[social_group].append(vehicle)
        else:
            print(
                "veh:{} subscription to bs:{} duplicated.".format(
                    vehicle.name,
                    self.name
                )
            )

    # Function called by VehicleRecorder to unsubscribe to a specific social group on this base station
    def VehicleUnsubscribe(self, vehicle, social_group):
        if(vehicle in self.sbscrb_social_vehs[social_group]):
            self.sbscrb_social_vehs[social_group].remove(vehicle)
        else:
            print(
                "veh:{} try to unsubscribe from bs:{}, but not yet subscribed.".format(
                    vehicle.name,
                    self.name
                )
            )

    # Helper functions
    def RequiredBandwidth(self, social_group):
        if(self.type == BaseStationType.UMA):
            return BS_UMA_RB_BANDWIDTH
        elif(self.type == BaseStationType.UMI):
            return BS_UMI_RB_BANDWIDTH_SOCIAL[social_group]


class CandidateBaseStationInfo:
    def __init__(self, station, social_group):
        self.station = station
        self.social_group = social_group


BASE_STATION_CONTROLLER = []
NET_STATUS_CACHE = NetStatusCache()


# (matlab.engine, [CandidateBaseStationInfo], (double,double))
def GET_BS_CQI_SINR_5G(vehicle, bs_ctrlr, social_group):
    # Vehicle's position
    Intf_dist = []
    Intf_pwr_dBm = []
    Intf_h_BS = []
    Intf_h_MS = []
    cqi = 0
    sinr = 0

    # Confirm settings with 3GPP specs
    if (bs_ctrlr.type == BaseStationType.UMA):
        # height of antenna
        h_BS = BS_UMA_HEIGHT
        # UMA transmission power
        tx_p_dBm = BS_UMA_TRANS_PWR
        # resource block bandwidth
        bandwidth = BS_UMA_RB_BANDWIDTH
        # cyclic prefix
        CP = BS_UMA_CP
        # GHz
        fc = BS_UMA_FREQ
    else:
        # height of antenna
        h_BS = BS_UMI_HEIGHT
        # UMI transmission power
        tx_p_dBm = BS_UMI_TRANS_PWR
        # resource block bandwidth
        bandwidth = BS_UMI_RB_BANDWIDTH_SOCIAL[social_group]
        # cyclic prefix
        CP = BS_UMI_CP_SOCIAL[social_group]
        # GHz
        fc = BS_UMI_FREQ
    # height of vehicle
    h_MS = 0.8
    # delay spread. (up to 4 us)
    DS_Desired = np.random.normal(0, 4)
    # distance between vehicle and station
    UE_dist = pow((bs_ctrlr.pos[0] - vehicle.pos[0])**2 +
                  (bs_ctrlr.pos[1] - vehicle.pos[1])**2, 0.5)

    for intf_BS_obj in BASE_STATION_CONTROLLER:
        if (intf_BS_obj == bs_ctrlr):
            continue
        if (intf_BS_obj.type == BaseStationType.UMA):
            # intf-station antenna height
            Intf_h_BS.append(BS_UMA_HEIGHT)
            # intf-station transmission power
            Intf_pwr_dBm.append(BS_UMA_TRANS_PWR)
        else:
            # intf-station antenna height
            Intf_h_BS.append(BS_UMI_HEIGHT)
            # intf-station transmission power
            Intf_pwr_dBm.append(BS_UMI_TRANS_PWR)
        # intf-vehicle height
        Intf_h_MS.append(0.8)
        # distance between vehicle and intf-station
        Intf_dist.append(pow((intf_BS_obj.pos[0] - vehicle.pos[0])**2 +
                             (intf_BS_obj.pos[1] - vehicle.pos[1])**2, 0.5))

    # result
    cqi, sinr = MATLAB_ENG.SINR_Channel_Model_5G(
        float(UE_dist),
        float(h_BS),
        float(h_MS),
        float(fc),
        float(tx_p_dBm),
        float(bandwidth),
        matlab.double(Intf_h_BS),
        matlab.double(Intf_h_MS),
        matlab.double(Intf_dist),
        matlab.double(Intf_pwr_dBm),
        float(DS_Desired),
        float(CP),
        True if bs_ctrlr.type == BaseStationType.UMA else False,
        nargout=2)
    return cqi, sinr
