import os
import sys
import matlab.engine
import math
import numpy as np
from enum import IntEnum
from globs import *
from net_pack import NetworkTransmitRequest, NetworkTransmitResponse

BASE_STATION_CONTROLLER = []


class BaseStationController:
    def __init__(self, name, pos, bs_type):
        self.name = name
        self.pos = pos
        self.radius = BS_UMI_RADIUS if bs_type == BaseStationType.UMI else BS_UMA_RADIUS
        self.type = bs_type
        self.social_group_pending_request = [[]]*len(SociatyGroup)
        self.valid_resource_blocks = 25

    def Request(self, pack: NetworkTransmitRequest):
        self.social_group_pending_request[pack.social_group].append(pack)

    def Update(self):
        # CRITICAL transmit requests has higher priority
        if len(self.social_group_pending_request[SociatyGroup.CRITICAL]) > 0:
            # sort width sinr
            requests = self.social_group_pending_request[SociatyGroup.CRITICAL]
            requests.sort(reverse=True, key=(lambda x: x.sinr))
            for request in requests:
                if self.valid_resource_blocks == 0:  # no resource block to allocate
                    # notify request owner
                    request.owner.Response(NetworkTransmitResponse(
                        False,
                        self,
                        request.name,
                        0,
                        request.social_group
                    ))
                else:
                    # allocate resource block for transmit request
                    trans_size = self.valid_resource_blocks if self.valid_resource_blocks < request.bytes else request.bytes
                    self.valid_resource_blocks -= trans_size
                    # notify request owner
                    request.owner.Response(NetworkTransmitResponse(
                        True,
                        self,
                        request.name,
                        trans_size,
                        request.social_group
                    ))

        # GENERAL transmit requests has lower priority
        if len(self.social_group_pending_request[SociatyGroup.GENERAL]) > 0:
            requests = self.social_group_pending_request[SociatyGroup.GENERAL]
        # Reset
        self.Reset()

    def Reset(self):
        self.social_group_pending_request = [[]]*len(SociatyGroup)
        self.valid_resource_blocks = BS_RESOURCE_BLOCK_TOTAL


# (matlab.engine,(double,double))
def GET_ALL_BS_CQI_Vector(eng, UE_POSITION):
    global BASE_STATION_CONTROLLER

    MACRO_BS_NUM = 0
    N_BS = len(BASE_STATION_CONTROLLER)
    CQI_Iter = np.zeros(N_BS, dtype=float)
    SINR_Iter = np.zeros(N_BS, dtype=float)

    for tx_BS_num, tx_BS_info in enumerate(BASE_STATION_CONTROLLER):
        Intf_dist = []
        Intf_pwr_dBm = []
        Intf_h_BS = []
        Intf_h_MS = []
        # Intf_DS_Desired = []

        # Confirm settings with 3GPP specs
        h_MS = 0.8  # height of vehicle
        if (tx_BS_num == MACRO_BS_NUM):
            h_BS = 25  # height of antenna
            CP = 4.69
            bandwidth = 180000
            tx_p_dBm = 23
        else:
            h_BS = 10  # height of antenna
            CP = 2.34
            bandwidth = 360000
            tx_p_dBm = 10

        UE_dist = pow((tx_BS_info.pos[0] - UE_POSITION[0])**2 +
                      (tx_BS_info.pos[1] - UE_POSITION[1])**2, 0.5)

        # up to 4 us
        DS_Desired = np.random.normal(0, 4)

        for intf_BS_num, intf_BS_info in enumerate(BASE_STATION_CONTROLLER):
            if (intf_BS_num == tx_BS_num):
                continue

            if (intf_BS_num == MACRO_BS_NUM):
                Intf_h_BS.append(25.0)
                Intf_h_MS.append(0.8)
                Intf_pwr_dBm.append(23)
            else:
                Intf_h_BS.append(10.0)
                Intf_h_MS.append(0.8)
                Intf_pwr_dBm.append(18)

            # GHz
            fc = 2.0

            # Locations
            Intf_dist.append(
                (pow((intf_BS_info.pos[0] - UE_POSITION[0])**2 +
                     (intf_BS_info.pos[1] - UE_POSITION[1])**2, 0.5)))

            (CQI_Iter[tx_BS_num],
             SINR_Iter[tx_BS_num]) = eng.SINR_Channel_Model_Multi_Var_BS(
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
                 nargout=2)
    return CQI_Iter


# (matlab.engine, [BaseStationController], (double,double))
def GET_BS_CQI_SINR_5G(eng, BS_INTEREST, UE_POSITION):
    CQI_Iter = np.zeros(len(BS_INTEREST), dtype=float)
    SINR_Iter = np.zeros(len(BS_INTEREST), dtype=float)

    for tx_BS_idx, tx_BS_obj in enumerate(BS_INTEREST):
        Intf_dist = []
        Intf_pwr_dBm = []
        Intf_h_BS = []
        Intf_h_MS = []

        # Confirm settings with 3GPP specs
        if (tx_BS_obj.type == BaseStationType.UMA):
            h_BS = 25  # height of antenna
            tx_p_dBm = 23  # UMA transmission power
            # bandwidth = 180000 # resource block bandwidth
            bandwidth = 360000  # for current schenario, both UMA&UMI works in bandwidth 360000
            CP = 4.69
            fc = 2.0  # GHz
        else:
            h_BS = 10  # height of antenna
            tx_p_dBm = 10  # UMI transmission power
            bandwidth = 360000  # resource block bandwidth
            CP = 2.34
            fc = 3.5  # GHz

        h_MS = 0.8  # height of vehicle

        UE_dist = pow((tx_BS_obj.pos[0] - UE_POSITION[0])**2 +
                      (tx_BS_obj.pos[1] - UE_POSITION[1])**2, 0.5)  # distance between vehicle and station

        DS_Desired = np.random.normal(0, 4)  # up to 4 us

        for intf_BS_obj in BASE_STATION_CONTROLLER:
            if (intf_BS_obj == tx_BS_obj):
                continue

            if (intf_BS_obj.type == BaseStationType.UMA):
                Intf_h_BS.append(25.0)  # intf-station antenna height
                Intf_pwr_dBm.append(23)  # intf-station transmission power
            else:
                Intf_h_BS.append(10.0)  # intf-station antenna height
                Intf_pwr_dBm.append(18)  # intf-station transmission power

            Intf_h_MS.append(0.8)  # intf-vehicle height
            Intf_dist.append((pow((intf_BS_obj.pos[0] - UE_POSITION[0])**2 +
                                  (intf_BS_obj.pos[1] - UE_POSITION[1])**2, 0.5)))  # distance between vehicle and intf-station

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
