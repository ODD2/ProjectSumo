import traci
import numpy as np
from enum import IntEnum
from numpy import random
from queue import Queue
from net_model import GET_BS_CQI_SINR_5G, BASE_STATION_CONTROLLER, BaseStationController, CandidateBaseStationInfo
from net_pack import NetworkTransmitResponse, NetworkTransmitRequest, NetworkPackage, PackageProcessing
from globs import SocialGroup, NetObjLayer, BaseStationType, NET_SG_RND_REQ_SIZE, PackageProcessType


class BriefBaseStationInfo:
    def __init__(self, ctrlr: BaseStationController, cqi: float, sinr: float,):
        self.ctrlr = ctrlr
        self.cqi = cqi
        self.sinr = sinr


class ConnectionState(IntEnum):
    Unknown = 0
    Connect = 1,
    Deny = 2,
    Transmit = 3,
    Success = 4


class SharedConnection:
    def __init__(self, rec):
        self.share = 1
        self.rec = rec


class ConnectionRecorder:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self.state = ConnectionState.Connect
        self.name = "con_{}_{}".format(s1.name, s2.name)
        # Create line
        traci.polygon.add(
            self.name,
            [(0, 0), (0, 0)],
            (0, 0, 0, 255),
            False,
            "Line",
            NetObjLayer.CON_LINE, 0.1
        )

    def Update(self):
        traci.polygon.setShape(
            self.name,
            [self.s1.pos, self.s2.pos]
        )

    def ChangeState(self, state: ConnectionState, force=False):
        if(not force and self.state > state):
            return

        self.state = state

        if(state == ConnectionState.Transmit):
            traci.polygon.setColor(self.name, (255, 165, 0, 255))
        elif(state == ConnectionState.Success):
            traci.polygon.setColor(self.name, (0, 255, 0, 255))
        else:
            traci.polygon.setColor(self.name, (0, 0, 0, 255))

    def Clean(self):
        traci.polygon.remove(self.name)


class NetworkStatusMonitor:
    def __init__(self):
        self.total_recv_package = 0
        self.total_send_package = 0
        self.step_recv_package = 0
        self.step_send_package = 0


class VehicleRecorder:
    def __init__(self, name):
        # Vehicle ID
        self.name = name

        # Vehicle Position
        self.pos = (0, 0)

        # Best connectivity base station for each social group, categorized by base station type
        self.sbscrb_social_bs = [
            [None for j in range(len(SocialGroup))] for i in range(len(BaseStationType))
        ]

        # The Social Group Upload Request Queue
        self.social_up_queue = [Queue(0) for i in SocialGroup]

        # The last time when this vehicle recorder generates upload request
        self.up_req_gen_time = 0

        # Package counter for upload req
        self.up_req_counter = 0

        # The last time when this vehicle recorder updates
        self.sync_time = 0

        # Upload/Download packages that're currently transmitting
        self.pkg_in_proc = [[] for i in PackageProcessType]

        # The network status monitor
        self.net_status = NetworkStatusMonitor()

        # The connetion lines currently drawn in SUMO
        self.con_state = {}

    # General routine called by main
    def Update(self, eng):
        self.UpdateVehicleInfo()
        self.CheckSubscribeBSValidity()
        self.SelectBestSocialBS(eng)
        self.LinkStateUpdate()
        self.GenerateUploadRequest()
        self.ServeUploadRequest()
        self.ServePkgs()

    # Update the vehicle's basic infos
    def UpdateVehicleInfo(self):
        self.pos = traci.vehicle.getPosition(self.name)
        self.sync_time = traci.simulation.getTime()

    # Check if the latest subscribes base stations still has the validity to provide service
    def CheckSubscribeBSValidity(self):
        invalid_bs = []
        for bs_type in BaseStationType:
            for social_group in SocialGroup:
                if(self.sbscrb_social_bs[bs_type][social_group] == None):
                    continue
                else:
                    base_station_ctrlr = self.sbscrb_social_bs[bs_type][social_group].ctrlr
                    if(base_station_ctrlr not in invalid_bs):
                        distance = pow((self.pos[0] - base_station_ctrlr.pos[0])**2 +
                                       (self.pos[1] - base_station_ctrlr.pos[1])**2, 0.5)
                        if(distance > base_station_ctrlr.radius):
                            self.UnsubscribeBS(bs_type, social_group)
                            invalid_bs.append(base_station_ctrlr)
                    else:
                        self.UnsubscribeBS(bs_type, social_group)

    # Find and subscribe the base station that provides the best connectivity according to it's social group,
    # also categorized by it's base station type.
    def SelectBestSocialBS(self, eng):
        bs_in_range = [[] for i in BaseStationType]

        # Find In-Range BaseStations
        for bs_ctrlr in BASE_STATION_CONTROLLER:
            distance = pow((self.pos[0] - bs_ctrlr.pos[0])**2 +
                           (self.pos[1] - bs_ctrlr.pos[1])**2, 0.5)
            if distance < bs_ctrlr.radius:
                bs_in_range[bs_ctrlr.type].append(bs_ctrlr)

        # Find best connectivity base station for social group, filter by base station type
        for bs_type in BaseStationType:
            if(len(bs_in_range[bs_type]) == 0):
                continue
            for social_type in SocialGroup:
                # Get cqi & sinr for social type
                _cqi, _sinr = GET_BS_CQI_SINR_5G(
                    eng,
                    [
                        CandidateBaseStationInfo(bs_ctrlr, social_type)
                        for bs_ctrlr in bs_in_range[bs_type]
                    ],
                    self.pos
                )
                bs_idx = np.argmax(_cqi)
                self.SubscribeBS(
                    bs_type,
                    social_type,
                    BriefBaseStationInfo(
                        bs_in_range[bs_type][bs_idx],
                        _cqi[bs_idx],
                        _sinr[bs_idx]
                    )
                )

    # Subscribe base station
    def SubscribeBS(self, bs_type, social_group, bs_info: BriefBaseStationInfo):
        # Unsubscribe the previous base station
        if(self.sbscrb_social_bs[bs_type][social_group] != None):
            self.UnsubscribeBS(bs_type, social_group)

        # Subscribe the new one
        self.sbscrb_social_bs[bs_type][social_group] = bs_info
        # Register to base station, too.
        bs_ctrlr = bs_info.ctrlr
        bs_ctrlr.VehicleSubscribe(self.name)
        # Create connection recorder for this base station if not exists
        if(bs_ctrlr.name not in self.con_state):
            self.con_state[bs_ctrlr.name] = SharedConnection(
                ConnectionRecorder(self, bs_ctrlr)
            )
        else:
            self.con_state[bs_ctrlr.name].share += 1

    #  Unsubscribe base station
    def UnsubscribeBS(self, bs_type, social_group):
        # Unsubscribe the base station
        bs_info = self.sbscrb_social_bs[bs_type][social_group]
        self.sbscrb_social_bs[bs_type][social_group] = None
        # Unregister from base station
        bs_ctrlr = bs_info.ctrlr
        bs_ctrlr.VehicleUnsubscribe(self.name)
        # Break connection
        self.con_state[bs_ctrlr.name].share -= 1

    # Randomly generate network request for different social groups (NetworkTransmitRequest without cqi&sinr filled)
    # size in bits
    def GenerateUploadRequest(self):
        if(self.sync_time - self.up_req_gen_time > 1):
            self.up_req_gen_time = self.sync_time
            for group in SocialGroup:
                for _ in range(random.poisson(1)):
                    req_size_rnd_range = NET_SG_RND_REQ_SIZE[group]
                    self.social_up_queue[group].put(
                        NetworkTransmitRequest(
                            NetworkPackage(
                                str(self.up_req_counter),
                                self,
                                random.randint(
                                    req_size_rnd_range[0],
                                    req_size_rnd_range[1]+1
                                )*8,
                                group,
                                self.sync_time,
                            ),
                            0,
                            0
                        )
                    )
                    self.up_req_counter += 1
            return
    # Serves upload requests

    def ServeUploadRequest(self):
        for group in SocialGroup:
            if(self.social_up_queue[group].qsize() > 0):
                bs_ctrlr_info = self.SelectSocialBS(group)
                if(bs_ctrlr_info != None):
                    request = self.social_up_queue[group].queue[0]
                    request.sinr = bs_ctrlr_info.sinr
                    request.cqi = bs_ctrlr_info.cqi
                    bs_ctrlr_info.ctrlr.Upload(
                        request
                    )

    # Serves uploading/downloading packages
    def ServePkgs(self):
        for pkg_proc_type in PackageProcessType:
            for pkg_proc in self.pkg_in_proc[pkg_proc_type]:
                pkg_proc.req_time_slots -= 1
                if(pkg_proc.req_time_slots == 0):
                    self.pkg_in_proc[pkg_proc_type].remove(pkg_proc)
                    if(pkg_proc.opponent.name in self.con_state):
                        self.con_state[pkg_proc.opponent.name].rec.ChangeState(
                            ConnectionState.Success
                        )
                    # TODO: do some logging stuff.
                    print(
                        "{}: {}:{} from:{} at:{} social:{} size:{} sender:{}".format(
                            self.sync_time,
                            pkg_proc_type.name.lower(),
                            pkg_proc.package.name,
                            pkg_proc.package.owner.name,
                            pkg_proc.package.at,
                            SocialGroup(
                                pkg_proc.package.social_group
                            ).name.lower(),
                            pkg_proc.package.bits,
                            pkg_proc.opponent.name,
                        )
                    )
                else:
                    if(pkg_proc.opponent.name in self.con_state):
                        self.con_state[pkg_proc.opponent.name].rec.ChangeState(
                            ConnectionState.Transmit
                        )

    # Select the service base station according to the social type provided.
    def SelectSocialBS(self, social_type):
        if(social_type == SocialGroup.CRITICAL):
            return (self.sbscrb_social_bs[BaseStationType.UMI][social_type]
                    if self.sbscrb_social_bs[BaseStationType.UMI][social_type] != None
                    else self.sbscrb_social_bs[BaseStationType.UMA][social_type])
        elif(social_type == SocialGroup.GENERAL):
            return (self.sbscrb_social_bs[BaseStationType.UMI][social_type]
                    if self.social_up_queue[SocialGroup.CRITICAL].qsize() == 0
                    else self.sbscrb_social_bs[BaseStationType.UMA][social_type])
        else:
            return (self.sbscrb_social_bs[BaseStationType.UMA][social_type]
                    if self.sbscrb_social_bs[BaseStationType.UMA][social_type] != None
                    else self.sbscrb_social_bs[BaseStationType.UMI][social_type])

    # Function called by BaseStationController to give response to requests
    def UploadRequestResponse(self, response: NetworkTransmitResponse):
        queue = self.social_up_queue[response.social_group]
        request = queue.queue[0]
        if request.package.name != response.name:
            print("Response: Error message corrupted")
            return

        if response.status:
            request.package.bits -= response.bits
            # Add Request to transferring
            self.pkg_in_proc[PackageProcessType.UPLOAD].append(
                PackageProcessing(
                    NetworkPackage(
                        request.package.name,
                        self,
                        response.bits,
                        request.package.social_group,
                        request.package.at
                    ),
                    response.sender,
                    response.req_time_slots
                )
            )
            # Message Fully Requested. Pop!
            if(request.package.bits == 0):
                queue.get()

    # Function called by BaseStationControllers to send packages
    def ReceivePackage(self, pkg: NetworkPackage):
        self.pkg_in_proc[pkg.social_group].append(pkg)

    def LinkStateUpdate(self):
        ghost_con = []
        for name, struct in self.con_state.items():
            # if no one's sharing this connection, the recorder is redundant
            if(struct.share <= 0):
                ghost_con.append(name)
                struct.rec.Clean()
            else:
                # initialize connection state to connect
                struct.rec.Update()
                struct.rec.ChangeState(ConnectionState.Connect, True)

        # remove non-shared existing connections
        for name in ghost_con:
            self.con_state.pop(name)

    def Clear(self):
        # Clear connection recorders
        for name in self.con_state:
            self.con_state[name].rec.Clean()
        self.con_state = {}

    def __del__(self):
        self.Clear()
