import os
import sys
import matlab.engine
import math
import numpy as np
import traci
from copy import copy
from net_pack import NetworkTransmitRequest, NetworkTransmitResponse, PackageProcessing, NetworkPackage
from globs import *

BASE_STATION_CONTROLLER = []


class ReceiverState:
    def __init__(self, recvr):
        self.bits_sent = 0
        self.recvr = recvr


class SocialGroupBroadcastRequest:
    def __init__(self, package, recvrs):
        self.package = package
        self.recvr_stats = [
            ReceiverState(recvr)
            for recvr in recvrs
            if recvr != package.owner
        ]


class BaseStationController:
    def __init__(self, name, pos, bs_type):
        # Base station paremeters
        self.name = name
        self.pos = pos
        self.radius = BS_UMI_RADIUS if bs_type == BaseStationType.UMI else BS_UMA_RADIUS
        self.type = bs_type

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
                pkg_proc.req_time_slots -= 1
                # consume bandwidth
                self.valid_bandwidth[link_type] -= self.RequiredBandwidth(
                    pkg_proc.package.social_group
                )
                if(pkg_proc.req_time_slots == 0):
                    # package that has done transmitting are collected
                    pkg_procs_done.append(pkg_proc)
                    # if the package is uploaded
                    if(link_type == LinkType.UPLOAD):
                        # Save to local
                        self.recv_package.append(pkg_proc.package)

                    TRACI_LOCK.acquire()
                    # log
                    print(
                        "{}-{}: type:{} target:{} origin:{}-{}*-{}b-{}-{}s ".format(
                            traci.simulation.getTime(),
                            self.name,
                            link_type.name.lower(),
                            pkg_proc.opponent.name,
                            pkg_proc.package.owner.name,
                            pkg_proc.package.name,
                            pkg_proc.package.bits,
                            SocialGroup(
                                pkg_proc.package.social_group
                            ).name.lower(),
                            pkg_proc.package.at,
                        )
                    )
                    TRACI_LOCK.release()

            # remove transmitted packages
            for pkg_proc in pkg_procs_done:
                # remove packages that has done transmitting
                self.pkg_in_proc[link_type].remove(pkg_proc)

    # Function called by VehicleRecorder to submit upload requests to this base station
    def Upload(self, req: NetworkTransmitRequest):
        self.sg_upload_req[req.package.social_group].append(req)

    # Serve submitted upload requests
    def ServeUploadRequest(self):
        for social_group in SocialGroup:
            # Check if there exists pending requests
            if len(self.sg_upload_req[social_group.value]) > 0:
                # sort with cqi
                requests = self.sg_upload_req[social_group.value]
                requests.sort(reverse=True, key=(lambda x: x.cqi))
                # required resource block bandwidth for social group msg
                req_bandwidth_per_rb = self.RequiredBandwidth(social_group)
                # required timeslot for using this bandwidth
                req_time_slots = NET_RB_BANDWIDTH_TS[req_bandwidth_per_rb]
                # serve requests
                for req in requests:
                    package = req.package
                    if self.valid_bandwidth[LinkType.UPLOAD] < req_bandwidth_per_rb:
                        package = copy(package)
                        # no resource block to allocate
                        package.bits = 0
                        # notify request owner
                        package.owner.UploadRequestResponse(
                            NetworkTransmitResponse(
                                False,
                                self,
                                package
                            )
                        )
                    else:
                        # allocate resource block for transmit request
                        # get the maximum transmission size per resource-block according to cqi
                        rb_trans_size = MATLAB_ENG.GetThroughputPerRB(
                            float(req.cqi),
                            int(NET_RB_SLOT_SYMBOLS)
                        )
                        valid_resource_blocks = math.floor(
                            self.valid_bandwidth[LinkType.UPLOAD] /
                            req_bandwidth_per_rb
                        )
                        # available total transmission size
                        valid_trans_size = rb_trans_size * valid_resource_blocks
                        # get the actual transmission size
                        trans_size = valid_trans_size if valid_trans_size < package.bits else package.bits
                        total_required_bandwidth = (req_bandwidth_per_rb *
                                                    math.ceil(trans_size/rb_trans_size))
                        # consume required bandwidth
                        self.valid_bandwidth[LinkType.UPLOAD] -= total_required_bandwidth
                        package = copy(package)
                        package.bits = trans_size
                        # notify request owner
                        package.owner.UploadRequestResponse(
                            NetworkTransmitResponse(
                                True,
                                self,
                                package,
                                req_time_slots
                            )
                        )
                        # create package to process
                        self.pkg_in_proc[LinkType.UPLOAD].append(
                            PackageProcessing(
                                package,
                                package.owner,
                                req_time_slots
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
        for social_group in SocialGroup:
            reqs_brdcst_done = []
            # required resource block bandwidth for social group msg
            req_bandwidth_per_rb = self.RequiredBandwidth(social_group)
            # required timeslot for using this bandwidth
            req_time_slots = NET_RB_BANDWIDTH_TS[req_bandwidth_per_rb]
            for req_brdcst in self.sg_broadcast_req[social_group]:
                package = req_brdcst.package
                recvrs_done = []
                # Not enought bandwidth for this type of social group request
                if self.valid_bandwidth[LinkType.DOWNLOAD] < req_bandwidth_per_rb:
                    break
                for recvr_state in req_brdcst.recvr_stats:
                    # Not enought bandwidth for this social group receiver
                    if self.valid_bandwidth[LinkType.DOWNLOAD] < req_bandwidth_per_rb:
                        break
                    else:
                        # allocate resource block for transmit request

                        # the receiver of this package
                        recvr = recvr_state.recvr
                        # remaining bits to transmit to complete the package
                        remain_bits = package.bits - recvr_state.bits_sent
                        # get sinr/cqi for receiver
                        _cqi, _sinr = GET_BS_CQI_SINR_5G(
                            [CandidateBaseStationInfo(self, social_group)],
                            recvr.pos
                        )
                        # get the maximum transmission size per resource-block according to cqi
                        rb_trans_size = MATLAB_ENG.GetThroughputPerRB(
                            float(_cqi),
                            int(NET_RB_SLOT_SYMBOLS)
                        )
                        valid_resource_blocks = math.floor(
                            self.valid_bandwidth[LinkType.UPLOAD] /
                            req_bandwidth_per_rb
                        )
                        # available total transmission size
                        valid_trans_size = rb_trans_size * valid_resource_blocks
                        # get the actual transmission size
                        trans_size = valid_trans_size if valid_trans_size < remain_bits else remain_bits
                        # get the total required bandwidth
                        total_required_bandwidth = (req_bandwidth_per_rb *
                                                    math.ceil(trans_size/rb_trans_size))
                        # consume required bandwidth
                        self.valid_bandwidth[LinkType.DOWNLOAD] -= total_required_bandwidth
                        # set package
                        package = copy(package)
                        package.bits = trans_size
                        # notify receiver
                        recvr.ReceivePackage(
                            self,
                            package,
                            req_time_slots
                        )
                        # create package to process
                        self.pkg_in_proc[LinkType.DOWNLOAD].append(
                            PackageProcessing(
                                package,
                                recvr,
                                req_time_slots
                            )
                        )
                        # record recvr if package completely transmitted
                        if(trans_size >= remain_bits):
                            recvrs_done.append(recvr_state)
                # remove receivers that has received the complete package
                for recvr_state in recvrs_done:
                    req_brdcst.recvr_stats.remove(recvr_state)
                # record broadcast request if all reciever recieves package.
                if len(req_brdcst.recvr_stats) == 0:
                    reqs_brdcst_done.append(req_brdcst)
            # remove completed broadcast requests
            for req_brdcst in reqs_brdcst_done:
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
    def __init__(self, base_station, social_group):
        self.transmitter = base_station
        self.transmit_social_group = social_group

# (matlab.engine, [CandidateBaseStationInfo], (double,double))


def GET_BS_CQI_SINR_5G(BS_INTEREST_INFO, UE_POSITION):
    CQI_Iter = np.zeros(len(BS_INTEREST_INFO), dtype=float)
    SINR_Iter = np.zeros(len(BS_INTEREST_INFO), dtype=float)

    for tx_BS_idx, tx_BS_info_obj in enumerate(BS_INTEREST_INFO):
        tx_BS_obj = tx_BS_info_obj.transmitter
        tx_social_group = tx_BS_info_obj.transmit_social_group
        Intf_dist = []
        Intf_pwr_dBm = []
        Intf_h_BS = []
        Intf_h_MS = []

        # Confirm settings with 3GPP specs
        if (tx_BS_obj.type == BaseStationType.UMA):
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
            bandwidth = BS_UMI_RB_BANDWIDTH_SOCIAL[tx_social_group]
            # cyclic prefix
            CP = BS_UMI_CP_SOCIAL[tx_social_group]
            # GHz
            fc = BS_UMI_FREQ

        # height of vehicle
        h_MS = 0.8

        # distance between vehicle and station
        UE_dist = pow((tx_BS_obj.pos[0] - UE_POSITION[0])**2 +
                      (tx_BS_obj.pos[1] - UE_POSITION[1])**2, 0.5)

        # up to 4 us
        DS_Desired = np.random.normal(0, 4)

        for intf_BS_obj in BASE_STATION_CONTROLLER:
            if (intf_BS_obj == tx_BS_obj):
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
            Intf_dist.append((pow((intf_BS_obj.pos[0] - UE_POSITION[0])**2 +
                                  (intf_BS_obj.pos[1] - UE_POSITION[1])**2, 0.5)))

        (CQI_Iter[tx_BS_idx], SINR_Iter[tx_BS_idx]) = MATLAB_ENG.SINR_Channel_Model_5G(
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
            True if tx_BS_obj.type == BaseStationType.UMA else False,
            nargout=2)

    return CQI_Iter, SINR_Iter
