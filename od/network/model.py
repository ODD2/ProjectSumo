from od.network.types import BaseStationType
from od.config import (BS_HEIGHT, BS_TRANS_PWR, BS_FREQ,
                       BS_UMA_RB_BW, BS_UMI_RB_BW_SG,
                       BS_UMI_CP_SOCIAL, BS_UMA_CP,
                       VEH_HEIGHT)
from od.social import SocialGroup
import od.engine as GE
import od.vars as GV
import matlab
import math

# Container to save network status


class NetStatus:
    def __init__(self):
        self.cached = False
        self.max_cqi = 0
        self.max_sinr = 0
        self.pwr_req_dBm = 0
        self.pwr_ext_dBm = 0


# Container to cache status results
class NetStatusCache:
    def __init__(self):
        self._map = {}

    # param [(vehicle,bs_ctrlr,social_group)]
    def GetMultiNetStatus(self, query_tuples):
        results = []
        netstat_futures = []
        # error detection
        for query in query_tuples:
            if query[0].name not in self._map:
                raise Exception("Error! vehicle should be in the map!!")
        # fetch none cached result in parellel
        for query in query_tuples:
            netstat = self._map[query[0].name][query[1].serial][query[2]]
            if (not netstat.cached):
                netstat_futures.append(
                    (
                        netstat,
                        GET_BS_CQI_SINR_5G_FUTURE(
                            query[0],
                            query[1],
                            query[2]
                        )
                    )
                )
                netstat.cached = True
        # retrieve parellel calculation result
        for pair in netstat_futures:
            netstat = pair[0]
            future = pair[1]
            (
                netstat.max_cqi, netstat.max_sinr,
                netstat.pwr_req_dBm,
                _, _, _, _, _,
                netstat.pwr_ext_dBm
            ) = future.result()
        # collect results
        for query in query_tuples:
            results.append(self._map[query[0].name][query[1].serial][query[2]])
        # return
        return results

    # param [(vehicle,bs_ctrlr,social_group)]
    def GetNetStatus(self, query_tuple):
        return self.GetMultiNetStatus([query_tuple])[0]

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
        for veh_status in self._map.values():
            for bs in GV.NET_STATION_CONTROLLER:
                for sg in SocialGroup:
                    veh_status[bs][sg].cached = False


# (VehicleRecorder, BaseStationController, SocialGroup)
def GET_BS_CQI_SINR_5G_FUTURE(vehicle, bs_ctrlr, social_group: SocialGroup):
    # Vehicle's position
    Intf_dist = [5000]  # dummy base station for work around
    Intf_pwr_dBm = [BS_TRANS_PWR[bs_ctrlr.type]]
    Intf_h_BS = [BS_HEIGHT[bs_ctrlr.type]]
    Intf_h_MS = [VEH_HEIGHT]

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
    h_MS = VEH_HEIGHT
    # delay spread.
    DS_Desired = 0.1
    # distance between vehicle and station
    UE_dist = max(
        pow((bs_ctrlr.pos[0] - vehicle.pos[0])**2 +
            (bs_ctrlr.pos[1] - vehicle.pos[1])**2, 0.5),
        10
    )

    for intf_BS_obj in [x for x in GV.NET_STATION_CONTROLLER if x.type == bs_ctrlr.type and x != bs_ctrlr]:
        # intf-station antenna height
        Intf_h_BS.append(BS_HEIGHT[intf_BS_obj.type])
        # intf-station transmission power
        Intf_pwr_dBm.append(BS_TRANS_PWR[intf_BS_obj.type])
        # intf-vehicle height
        Intf_h_MS.append(VEH_HEIGHT)
        # distance between vehicle and intf-station
        Intf_dist.append(
            max(
                pow(
                    (intf_BS_obj.pos[0] - vehicle.pos[0])**2 +
                    (intf_BS_obj.pos[1] - vehicle.pos[1])**2,
                    0.5
                ),
                10
            )
        )

    # result
    return GE.MATLAB_ENG.SINR_Channel_Model_5G(
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
        float(DS_Desired*1000),  # us->ns
        float(CP*1000),  # us->ns
        True if bs_ctrlr.type == BaseStationType.UMA else False,
        float(0.001),
        float(tx_p_dBm - 3.01029995664),
        # 10*log10(pwr_mw/2) = 10*log10(pwr_mw) - 10*log10(2)
        #                    = pwr_dBm - 3.01029995664
        False,
        True,
        nargout=9,
        background=True
    )
