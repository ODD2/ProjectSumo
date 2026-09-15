"""
od/network/model.py - 5G channel estimation and network status cache.

NetStatusCache stores per-(vehicle, base-station, social-group) channel quality
results so that MATLAB is only queried once per SUMO step per unique triplet.
The cache is flushed at the start of each SUMO step after vehicle positions
have been updated.

GET_BS_CQI_SINR_5G_FUTURE() builds the MATLAB call arguments from simulation
state and issues the call asynchronously, returning a future whose result
contains CQI, SINR, and power values.
"""
from socket import timeout
from od.network.types import BaseStationType
from od.env.config import (BS_HEIGHT, BS_TRANS_PWR, BS_FREQ,
                           BS_UMA_RB_BW, BS_UMI_RB_BW_QoS,
                           BS_UMI_CP_QoS, BS_UMA_CP,
                           VEH_HEIGHT)
from od.social.group import SocialGroup
import od.engine as GE
from od.social.group.types import QoSLevel
import od.vars as GV
import matlab
import math


class NetStatus:
    """Cached channel quality result for one (vehicle, BS, social group) triplet.

    Attributes:
        cached:      True once the MATLAB result has been retrieved.
        max_cqi:     Best achievable CQI index (0–15).
        max_sinr:    Corresponding SINR in dB.
        pwr_req_dBm: Minimum transmit power (dBm) required to reach max_cqi.
        pwr_ext_dBm: Available excess power after serving the inner NOMA user.
    """
    def __init__(self):
        self.cached = False
        self.max_cqi = 0
        self.max_sinr = 0
        self.pwr_req_dBm = 0
        self.pwr_ext_dBm = 0


class NetStatusCache:
    """Three-level cache: vehicle → base station serial → social group → NetStatus.

    MATLAB channel estimation calls are expensive.  This cache ensures each
    (vehicle, BS, social group) triplet is computed at most once per SUMO step.
    Parallel futures are issued for all uncached entries in a batch query to
    maximise MATLAB engine throughput.
    """
    def __init__(self):
        self._map = {}

    def GetMultiNetStatus(self, query_tuples):
        """Return NetStatus objects for a batch of (vehicle, BS, SocialGroup) tuples.

        Uncached entries have their MATLAB futures issued in parallel; results
        are then retrieved sequentially.  Cached entries are returned directly
        without a MATLAB call.

        Args:
            query_tuples: List of (VehicleRecorder, BaseStationController,
                          SocialGroup) tuples.

        Returns:
            List of NetStatus objects in the same order as *query_tuples*.
        """
        results = []
        netstat_futures = []
        # error detection
        for query in query_tuples:
            if query[0].name not in self._map:
                raise Exception("Error! vehicle should be in the map!!")

        # fetch none cached result in parellel
        for query in query_tuples:
            # dynamically allocate NetStatus for difference vehicle social groups.
            if(query[2] not in self._map[query[0].name][query[1].serial]):
                self._map[query[0].name][query[1].serial][query[2]] = NetStatus()
            netstat = self._map[query[0].name][query[1].serial][query[2]]
            if (not netstat.cached):
                netstat_futures.append(
                    (
                        netstat,
                        GET_BS_CQI_SINR_5G_FUTURE(
                            query[0],
                            query[1],
                            query[2].qos
                        )
                    )
                )
                netstat.cached = True
        # retrieve parellel calculation result
        for pair in netstat_futures:
            netstat = pair[0]
            future = pair[1]
            try:
                (
                    netstat.max_cqi, netstat.max_sinr,
                    netstat.pwr_req_dBm,
                    _, _, _, _, _,
                    netstat.pwr_ext_dBm
                ) = future.result(60)
            except Exception as e:
                print("Simulation Failure, Channel Estimation Failure!!!")
                exit(0)

        # collect results
        for query in query_tuples:
            results.append(self._map[query[0].name][query[1].serial][query[2]])
        # return
        return results

    def GetNetStatus(self, query_tuple):
        """Return the NetStatus for a single (vehicle, BS, SocialGroup) tuple."""
        return self.GetMultiNetStatus([query_tuple])[0]

    def Flush(self):
        """Invalidate all cached results for the new SUMO step.

        Removes entries for vehicles that have left the map, adds empty
        entries for newly arrived vehicles, and resets the ``cached`` flag on
        all existing entries so MATLAB is re-queried with updated positions.
        """
        # remove ghosts
        for veh_id in GV.SUMO_SIM_INFO.ghost_veh_ids:
            self._map.pop(veh_id)
        # add new vehicles
        for veh_id in GV.SUMO_SIM_INFO.new_veh_ids:
            self._map[veh_id] = [{} for _ in GV.NET_STATION_CONTROLLER]
        # initialize
        for veh_total_status in self._map.values():
            for veh_bs_status in veh_total_status:
                for veh_bs_sg_status in veh_bs_status.values():
                    veh_bs_sg_status.cached = False


def GET_BS_CQI_SINR_5G_FUTURE(vehicle, bs_ctrlr, qos: QoSLevel):
    """Issue an async MATLAB call to compute 5G channel quality.

    Builds the parameter vectors required by SINR_Channel_Model_5G_mex,
    including interference contributions from all co-type base stations,
    and returns a MATLAB future.  Calling future.result(timeout) yields a
    9-element tuple: (max_cqi, max_sinr, pwr_req_dBm, ..., pwr_ext_dBm).

    Path loss and multipath fading follow 3GPP TR 38.901.  UMI uses a wider
    subcarrier spacing (2 × NET_RB_BW_UNIT) for CRITICAL QoS traffic.

    Args:
        vehicle:    VehicleRecorder providing the current (x, y) position.
        bs_ctrlr:   Target BaseStationController.
        qos:        QoSLevel determining subcarrier spacing for UMI cells.

    Returns:
        A MATLAB background future whose result() call blocks until the
        channel model computation completes.
    """
    # Interference vectors, seeded with a dummy far-away entry (index 0) that
    # the co-type interferer loop below appends real stations onto.
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
        bandwidth = BS_UMI_RB_BW_QoS[qos]
        # cyclic prefix
        CP = BS_UMI_CP_QoS[qos]

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
    return GE.MATLAB_ENG.SINR_Channel_Model_5G_mex(
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
        float(DS_Desired * 1000),  # us->ns
        float(CP * 1000),  # us->ns
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


# def GET_BS_CQI_SINR_5G_FUTURE(vehicle, bs_ctrlr, qos: QoSLevel):
#     class Future:
#         def __init__(self):
#             pass

#         def result(self):
#             pwr = BS_TRANS_PWR[bs_ctrlr.type] - 3.01029995664
#             return (15, 200, pwr, None, None, None, None, None, pwr)
#     return Future()
