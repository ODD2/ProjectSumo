from od.network.types import BaseStationType
from od.config import (BS_HEIGHT, BS_TRANS_PWR, BS_FREQ,
                       BS_UMA_RB_BW, BS_UMI_RB_BW_SG,
                       BS_UMI_CP_SOCIAL, BS_UMA_CP)
from od.social import SocialGroup
import od.engine as GE
import od.vars as GV
import matlab

# Container to save network status


class NetStatus:
    def __init__(self):
        self.cached = False
        self.cqi = 0
        self.sinr = 0

# Container to cache status results


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
                query_tuple[2]
            )
            net_stat.cached = True
        return net_stat

    # clean
    def Flush(self):
        # remove ghosts
        for veh_id in GV.SUMO_SIM_INFO.ghost_veh_ids:
            self._map.pop(veh_id)
        # add new vehicles
        for veh_id in GV.SUMO_SIM_INFO.new_veh_ids:
            self._map[veh_id] = [[NetStatus() for sg in SocialGroup]
                                 for i in range(len(GV.NET_STATION_CONTROLLER))]
        # initialize
        for veh_status_list in self._map.values():
            for bs_idx in range(len(GV.NET_STATION_CONTROLLER)):
                for sg in SocialGroup:
                    veh_status_list[bs_idx][sg].cached = False

# (VehicleRecorder, BaseStationController, SocialGroup)


def GET_BS_CQI_SINR_5G(vehicle, bs_ctrlr, social_group: SocialGroup):
    # Vehicle's position
    Intf_dist = []
    Intf_pwr_dBm = []
    Intf_h_BS = []
    Intf_h_MS = []
    cqi = 0
    sinr = 0

    # Confirm settings with 3GPP specs
    if (bs_ctrlr.type == BaseStationType.UMA):
        # resource block bandwidth
        bandwidth = BS_UMA_RB_BW
        # cyclic prefix
        CP = BS_UMA_CP
    elif(bs_ctrlr.type == BaseStationType.UMI):
        # resource block bandwidth
        bandwidth = BS_UMI_RB_BW_SG[social_group]
        # cyclic prefix
        CP = BS_UMI_CP_SOCIAL[social_group]

    # Height of antenna
    h_BS = BS_HEIGHT[bs_ctrlr.type]
    # Transmission power
    tx_p_dBm = BS_TRANS_PWR[bs_ctrlr.type]
    # Transmission frequency.(Ghz)
    fc = BS_FREQ[bs_ctrlr.type]
    # height of vehicle
    h_MS = 0.8
    # delay spread. (up to 4 us)
    # DS_Desired = random.normal(0, 4)
    DS_Desired = 0.5
    # distance between vehicle and station
    UE_dist = pow((bs_ctrlr.pos[0] - vehicle.pos[0])**2 +
                  (bs_ctrlr.pos[1] - vehicle.pos[1])**2, 0.5)

    for intf_BS_obj in GV.NET_STATION_CONTROLLER:
        if (intf_BS_obj == bs_ctrlr):
            continue

        # intf-station antenna height
        Intf_h_BS.append(BS_HEIGHT[intf_BS_obj.type])
        # intf-station transmission power
        Intf_pwr_dBm.append(BS_TRANS_PWR[intf_BS_obj.type])
        # intf-vehicle height
        Intf_h_MS.append(0.8)
        # distance between vehicle and intf-station
        Intf_dist.append(
            pow(
                (intf_BS_obj.pos[0] - vehicle.pos[0])**2 +
                (intf_BS_obj.pos[1] - vehicle.pos[1])**2,
                0.5
            )
        )

    # result
    cqi, sinr = GE.MATLAB_ENG.SINR_Channel_Model_5G(
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
        float(DS_Desired),  # ns
        float(CP)*1000,  # ns
        True if bs_ctrlr.type == BaseStationType.UMA else False,
        nargout=2)
    return cqi, sinr
