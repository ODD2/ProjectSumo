import traci
import numpy as np
import profile
import net_model
from enum import IntEnum
from numpy import random
from queue import Queue
from net_model import NET_STATUS_CACHE, BASE_STATION_CONTROLLER, BaseStationController, CandidateBaseStationInfo
from net_pack import NetworkPackage, PackageProcessing
from globs import SocialGroup, NetObjLayer, BaseStationType, NET_SG_RND_REQ_SIZE, LinkType
from globs import TRACI_LOCK, MATLAB_ENG, SIM_STEP_INFO


class ConnectionState(IntEnum):
    Unknown = 0
    Connect = 1,
    Deny = 2,
    Transmit = 3,
    Success = 4


class SharedConnection:
    def __init__(self, rec):
        self.share = 0
        self.rec = rec


class ConnectionRecorder:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self.state = ConnectionState.Connect
        self.name = "con_{}_{}".format(s1.name, s2.name)
        TRACI_LOCK.acquire()
        # Create line
        traci.polygon.add(
            self.name,
            [(0, 0), (0, 0)],
            (0, 0, 0, 255),
            False,
            "Line",
            NetObjLayer.CON_LINE, 0.1
        )
        TRACI_LOCK.release()

    def Update(self):
        TRACI_LOCK.acquire()
        traci.polygon.setShape(
            self.name,
            [self.s1.pos, self.s2.pos]
        )
        TRACI_LOCK.release()

    def ChangeState(self, state: ConnectionState, force=False):
        if(not force and self.state > state):
            return

        self.state = state

        TRACI_LOCK.acquire()
        if(state == ConnectionState.Transmit):
            traci.polygon.setColor(self.name, (255, 165, 0, 255))
        elif(state == ConnectionState.Success):
            traci.polygon.setColor(self.name, (0, 255, 0, 255))
        else:
            traci.polygon.setColor(self.name, (0, 0, 0, 255))
        TRACI_LOCK.release()

    def Clean(self):
        TRACI_LOCK.acquire()
        traci.polygon.remove(self.name)
        TRACI_LOCK.release()


class NetworkStatusMonitor:
    def __init__(self):
        self.total_recv_package = 0
        self.total_send_package = 0
        self.step_recv_package = 0
        self.step_send_package = 0


class VehicleRecorder():
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
        self.sg_upload_list = [[] for i in SocialGroup]

        # The last time when this vehicle recorder generates upload request
        self.up_last_pkg_gen_time = 0

        # Package counter for upload req
        self.up_pkg_counter = 0

        # The last time when this vehicle recorder updates
        self.sync_time = 0

        # Upload/Download packages that're currently transmitting
        self.pkg_in_proc = [[] for i in LinkType]

        # The network status monitor
        self.net_status = NetworkStatusMonitor()

        # The connetion lines currently drawn in SUMO
        self.con_state = {}

    def __del__(self):
        self.Clear()

    # General routine called by main

    def Update(self):
        self.UpdateVehicleInfo()
        self.CheckSubscribeBSValidity()
        self.SelectBestSocialBS()
        self.LinkStateUpdate()
        self.GenerateUploadRequest()
        self.ServeUploadRequest()
        self.ServePackage()

    # Update the vehicle's basic infos
    def UpdateVehicleInfo(self):
        TRACI_LOCK.acquire()
        self.pos = traci.vehicle.getPosition(self.name)
        TRACI_LOCK.release()
        self.sync_time = SIM_STEP_INFO.time

    # Check if the latest subscribes base stations still has the validity to provide service
    def CheckSubscribeBSValidity(self):
        invalid_bs = []
        for bs_type in BaseStationType:
            for social_group in SocialGroup:
                if(self.sbscrb_social_bs[bs_type][social_group] == None):
                    continue
                else:
                    bs_ctrlr = self.sbscrb_social_bs[bs_type][social_group]
                    if(bs_ctrlr not in invalid_bs):
                        distance = pow((self.pos[0] - bs_ctrlr.pos[0])**2 +
                                       (self.pos[1] - bs_ctrlr.pos[1])**2, 0.5)
                        if(distance > bs_ctrlr.radius):
                            self.UnsubscribeBS(bs_type, social_group)
                            invalid_bs.append(bs_ctrlr)
                    else:
                        self.UnsubscribeBS(bs_type, social_group)

    # Find and subscribe the base station that provides the best connectivity according to it's social group,
    # also categorized by it's base station type.
    def SelectBestSocialBS(self):
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
                multi_net_status = NET_STATUS_CACHE.GetMultiNetStatus(
                    [
                        (self, bs_ctrlr, social_type)
                        for bs_ctrlr in bs_in_range[bs_type]
                    ]
                )
                best_idx = 0
                best_cqi = multi_net_status[0].cqi
                for idx, net_status in enumerate(multi_net_status):
                    if net_status.cqi > best_cqi:
                        best_idx = idx
                        best_cqi = net_status.cqi

                self.SubscribeBS(
                    bs_type,
                    social_type,
                    bs_in_range[bs_type][best_idx]
                )

    # Subscribe base station
    def SubscribeBS(self, bs_type, social_group, bs_ctrlr):
        # Unsubscribe the previous base station
        if(self.sbscrb_social_bs[bs_type][social_group] != None):
            self.UnsubscribeBS(bs_type, social_group)

        # Subscribe the new one
        self.sbscrb_social_bs[bs_type][social_group] = bs_ctrlr
        # Register to base station, too.
        bs_ctrlr.VehicleSubscribe(self, social_group)
        # Update connection state
        self.ConnectionChange(True, bs_ctrlr)

    #  Unsubscribe base station
    def UnsubscribeBS(self, bs_type, social_group):
        # Unsubscribe the base station
        bs_ctrlr = self.sbscrb_social_bs[bs_type][social_group]
        self.sbscrb_social_bs[bs_type][social_group] = None
        # Unregister from base station
        bs_ctrlr.VehicleUnsubscribe(self, social_group)
        # Update connection state
        self.ConnectionChange(False, bs_ctrlr)

    # Randomly generate network request for different social groups (NetworkTransmitRequest without cqi&sinr filled)
    # size in bits
    def GenerateUploadRequest(self):
        if(self.sync_time - self.up_last_pkg_gen_time > 1):
            self.up_last_pkg_gen_time = self.sync_time
            for group in SocialGroup:
                for _ in range(random.poisson(1)):
                    req_size_rnd_range = NET_SG_RND_REQ_SIZE[group]
                    self.sg_upload_list[group].append(
                        NetworkPackage(
                            str(self.up_pkg_counter),
                            self,
                            random.randint(
                                req_size_rnd_range[0],
                                req_size_rnd_range[1]+1
                            )*8,
                            group,
                            self.sync_time,
                        ),
                    )
                    self.up_pkg_counter += 1

    # Serves upload requests
    def ServeUploadRequest(self):
        for social_group in SocialGroup:
            if(len(self.sg_upload_list[social_group]) > 0):
                bs_ctrlr = self.SelectSocialBS(social_group)
                if(bs_ctrlr != None):
                    for pkg in self.sg_upload_list[social_group]:
                        bs_ctrlr.Upload(pkg)
                else:
                    print("Error: No BS to serve request.")

    # Serves uploading/downloading packages
    def ServePackage(self):
        for link_type in LinkType:
            pkg_procs_done = []
            for pkg_proc in self.pkg_in_proc[link_type]:
                pkg_proc.time_slots -= 1
                pkg = pkg_proc.package
                if(pkg_proc.time_slots == 0):
                    # collect packages that were transmitted
                    pkg_procs_done.append(pkg_proc)
                    # TODO: do some logging stuff.
                    print(
                        "{}-{}: type:{} target:{} origin:{}-{}*-{}b-{}-{}s ".format(
                            self.sync_time,
                            self.name,
                            link_type.name.lower(),
                            pkg_proc.opponent.name,
                            pkg.owner.name,
                            pkg.name,
                            pkg_proc.proc_bits,
                            SocialGroup(pkg.social_group).name.lower(),
                            pkg.at,
                        )
                    )
                    if(pkg_proc.opponent.name in self.con_state):
                        self.con_state[pkg_proc.opponent.name].rec.ChangeState(
                            ConnectionState.Success
                        )
                else:
                    if(pkg_proc.opponent.name in self.con_state):
                        self.con_state[pkg_proc.opponent.name].rec.ChangeState(
                            ConnectionState.Transmit
                        )
            # remove transmitted packages
            for pkg_proc in pkg_procs_done:
                self.pkg_in_proc[link_type].remove(pkg_proc)

    # Select the service base station according to the social type provided.
    def SelectSocialBS(self, social_type):
        if(social_type == SocialGroup.CRITICAL):
            return (self.sbscrb_social_bs[BaseStationType.UMI][social_type]
                    if self.sbscrb_social_bs[BaseStationType.UMI][social_type] != None
                    else self.sbscrb_social_bs[BaseStationType.UMA][social_type])
        elif(social_type == SocialGroup.GENERAL):
            return (self.sbscrb_social_bs[BaseStationType.UMI][social_type]
                    if (self.sbscrb_social_bs[BaseStationType.UMI][social_type] != None
                        and
                        len(self.sg_upload_list[SocialGroup.CRITICAL]) == 0)
                    else self.sbscrb_social_bs[BaseStationType.UMA][social_type])
        else:
            return (self.sbscrb_social_bs[BaseStationType.UMA][social_type]
                    if self.sbscrb_social_bs[BaseStationType.UMA][social_type] != None
                    else self.sbscrb_social_bs[BaseStationType.UMI][social_type])

    # Function called by BaseStationController to give response to requests
    def UploadRequestResponse(self, sender, package, bits, time_slots):
        #  no bits to transfer, request denied
        if(not bits > 0):
            return

        # make package in process state
        self.pkg_in_proc[LinkType.UPLOAD].append(
            PackageProcessing(
                package,
                sender,
                bits,
                time_slots
            )
        )

        if(package.bits <= bits):
            self.sg_upload_list[package.social_group].remove(package)

    # Function called by BaseStationControllers to send packages
    def ReceivePackage(self, sender, package, bits, time_slots):
        self.pkg_in_proc[LinkType.DOWNLOAD].append(
            PackageProcessing(
                package,
                sender,
                bits,
                time_slots
            )
        )

    # Update & Clean up the connection
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

    # The Connection manager to manage connection between self and others
    def ConnectionChange(self, build, opponent):
        if(build):
            # Create connection recorder for this base station if not exists
            if(opponent.name not in self.con_state):
                self.con_state[opponent.name] = SharedConnection(
                    ConnectionRecorder(self, opponent)
                )
            self.con_state[opponent.name].share += 1
        else:
            # Break connection
            self.con_state[opponent.name].share -= 1

    # Clean up
    def Clear(self):
        # Clear connection recorders
        for name in self.con_state:
            self.con_state[name].rec.Clean()
        self.con_state = {}
