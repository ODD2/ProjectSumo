import os
import sys
import matlab.engine
import math
import numpy as np
import traci
from globs import *
from net_pack import NetworkTransmitRequest, NetworkTransmitResponse

BASE_STATION_CONTROLLER = []


class BaseStationController:
    def __init__(self, name, pos, bs_type):
        self.name = name
        self.pos = pos
        self.radius = BS_UMI_RADIUS if bs_type == BaseStationType.UMI else BS_UMA_RADIUS
        self.type = bs_type
        self.Reset()

    def Request(self, pack: NetworkTransmitRequest):
        self.social_group_pending_request[pack.social_group].append(pack)

    def Update(self, eng):
        for group in SociatyGroup:
            # Check if there exists pending requests
            if len(self.social_group_pending_request[group.value]) > 0:
                # sort with cqi
                requests = self.social_group_pending_request[group.value]
                requests.sort(reverse=True, key=(lambda x: x.cqi))
                # required resource block bandwidth for social group msg
                req_bandwidth_per_rb = self.RequiredBandwidth(group)
                # serve requests
                for req in requests:
                    if self.valid_bandwidth < req_bandwidth_per_rb:
                        # no resource block to allocate

                        # notify request owner
                        req.owner.Response(NetworkTransmitResponse(
                            False,
                            self,
                            req.name,
                            0,
                            req.social_group
                        ))
                    else:
                        # allocate resource block for transmit request

                        # get the cqi and sinr of tranmission
                        # cqi, sinr = GET_BS_CQI_SINR_5G(
                        #     eng,
                        #     [CandidateBaseStationInfo(self, req.social_group)],
                        #     traci.vehicle.getPosition(request.owner.vid)
                        # )

                        # get the maximum transmission size per resource-block according to cqi
                        rb_trans_size = eng.GetThroughputPerRB(
                            float(req.cqi),
                            int(NET_RB_SLOT_SYMBOLS)
                        )
                        valid_resource_blocks = math.floor(
                            self.valid_bandwidth/req_bandwidth_per_rb
                        )
                        # available total transmission size
                        valid_trans_size = rb_trans_size * valid_resource_blocks

                        # get the actual transmission size
                        trans_size = valid_trans_size if valid_trans_size < req.bits else req.bits

                        total_required_bandwidth = (req_bandwidth_per_rb *
                                                    math.ceil(trans_size/rb_trans_size))
                        # consume required bandwidth
                        self.valid_bandwidth -= total_required_bandwidth

                        # if resource block bandwidth requires two timeslots
                        if(NET_RB_BANDWIDTH_TS[req_bandwidth_per_rb] == 2):
                            # consume required bandwidth for the next timeslot
                            self.valid_bandwidth_next_ts -= total_required_bandwidth

                        # notify request owner
                        req.owner.Response(NetworkTransmitResponse(
                            True,
                            self,
                            req.name,
                            trans_size,
                            req.social_group
                        ))
        # Reset
        self.Reset()

    def Reset(self):
        self.social_group_pending_request = (
            [[] for x in range(len(SociatyGroup))]
        )
        # valid bandwidth for next timeslot (0.5ms per timeslot)
        self.valid_bandwidth_next_ts = BS_ALL_BANDWIDTH*0.9
        self.valid_bandwidth = self.valid_bandwidth_next_ts

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
def GET_BS_CQI_SINR_5G(eng, BS_INTEREST_INFO, UE_POSITION):
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
            CP = 4.69
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

        (CQI_Iter[tx_BS_idx], SINR_Iter[tx_BS_idx]) = eng.SINR_Channel_Model_5G(
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
