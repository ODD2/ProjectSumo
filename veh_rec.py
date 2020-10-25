import traci
from enum import IntEnum
from numpy import random
from globs import SocialGroup, NetObjLayer, BaseStationType, NET_SG_RND_REQ_SIZE, LinkType
from globs import TRACI_LOCK, MATLAB_ENG, SUMO_SIM_INFO
from net_model import NET_STATUS_CACHE, BASE_STATION_CONTROLLER, BaseStationController
from net_app import AppDataHeader, AppData, VehicleApplication
from net_pack import NetworkPackage
from sim_log import DEBUG, ERROR


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
        traci.polygon.add(self.name, [(0, 0), (0, 0)], (0, 0, 0, 255), False,
                          "Line", NetObjLayer.CON_LINE, 0.1)
        TRACI_LOCK.release()

    def Update(self):
        TRACI_LOCK.acquire()
        traci.polygon.setShape(self.name, [self.s1.pos, self.s2.pos])
        TRACI_LOCK.release()

    def ChangeState(self, state: ConnectionState, force=False):
        if (not force and self.state > state):
            return

        self.state = state

        TRACI_LOCK.acquire()
        if (state == ConnectionState.Transmit):
            traci.polygon.setColor(self.name, (255, 165, 0, 255))
        elif (state == ConnectionState.Success):
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
        self.sub_sg_bs = [[None for j in SocialGroup]
                          for i in BaseStationType]

        # Create the vehicle application
        self.app = VehicleApplication(self)

        # Upload/Download packages that're currently transmitting
        self.pkg_in_proc = [[] for i in LinkType]

        # The network status monitor
        self.net_status = NetworkStatusMonitor()

        # The connetion lines currently drawn in SUMO
        self.con_state = {}

    def __del__(self):
        self.Clear()

    # Update per sumo simulation step
    def UpdateSS(self):
        self.UpdateVehicleInfo()
        self.CheckSubscribeBSValidity()
        self.SelectBestSocialBS()

    # Update per network simulation step
    def UpdateNS(self, ns):
        self.app.Run()
        self.RequestUploadResource()

    # Update per timeslot
    def UpdateT(self, ts):
        self.LinkStateUpdate()
        self.ProcessPackage(ts)

    # Update vehicle info from sumo
    def UpdateVehicleInfo(self):
        TRACI_LOCK.acquire()
        self.pos = traci.vehicle.getPosition(self.name)
        TRACI_LOCK.release()

    # Check if the latest subscription base stations still provide services
    def CheckSubscribeBSValidity(self):
        invalid_bs = []
        for bs_type in BaseStationType:
            for social_group in SocialGroup:
                if (self.sub_sg_bs[bs_type][social_group] == None):
                    continue
                else:
                    bs_ctrlr = self.sub_sg_bs[bs_type][social_group]
                    if (bs_ctrlr not in invalid_bs):
                        distance = pow((self.pos[0] - bs_ctrlr.pos[0])**2 +
                                       (self.pos[1] - bs_ctrlr.pos[1])**2, 0.5)
                        if (distance > bs_ctrlr.radius):
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
            if (len(bs_in_range[bs_type]) == 0):
                continue
            for social_type in SocialGroup:
                # Get cqi & sinr for social type
                multi_net_status = NET_STATUS_CACHE.GetMultiNetStatus([
                    (self, bs_ctrlr, social_type)
                    for bs_ctrlr in bs_in_range[bs_type]
                ])
                best_idx = 0
                best_cqi = multi_net_status[0].cqi
                for idx, net_status in enumerate(multi_net_status):
                    if net_status.cqi > best_cqi:
                        best_idx = idx
                        best_cqi = net_status.cqi

                self.SubscribeBS(bs_type, social_type,
                                 bs_in_range[bs_type][best_idx])

    # Subscribe base station
    def SubscribeBS(self, bs_type, social_group, bs_ctrlr):
        # Unsubscribe the previous base station
        if (self.sub_sg_bs[bs_type][social_group] != None):
            self.UnsubscribeBS(bs_type, social_group)

        # Subscribe the new one
        self.sub_sg_bs[bs_type][social_group] = bs_ctrlr
        # Register to base station, too.
        bs_ctrlr.VehicleSubscribe(self, social_group)
        # Update connection state
        self.ConnectionChange(True, bs_ctrlr)

    # Unsubscribe base station
    def UnsubscribeBS(self, bs_type, social_group):
        # Unsubscribe the base station
        bs_ctrlr = self.sub_sg_bs[bs_type][social_group]
        self.sub_sg_bs[bs_type][social_group] = None
        # Unregister from base station
        bs_ctrlr.VehicleUnsubscribe(self, social_group)
        # Update connection state
        self.ConnectionChange(False, bs_ctrlr)

    # Submit upload requests
    def RequestUploadResource(self):
        for social_group in SocialGroup:
            if (len(self.app.datas[social_group]) > 0):
                bs_ctrlr = self.SelectSocialBS(social_group)
                if (bs_ctrlr != None):
                    sg_total_bits = 0
                    for appdata in self.app.datas[social_group]:
                        sg_total_bits += appdata.bits
                    bs_ctrlr.ReceiveUploadRequest(
                        self,
                        social_group,
                        sg_total_bits,
                    )
                else:
                    ERROR.Log("Error: No BS to serve request.")

    # Function called by BaseStationController to give resource block to upload requests
    def UploadResourceGranted(self, bs_ctrlr, social_group, total_bits, trans_ts, offset_ts):
        self.SendPackage(
            self.CreatePackage(
                bs_ctrlr,
                social_group,
                total_bits,
                trans_ts,
                offset_ts
            )
        )

    # Create package
    def CreatePackage(self, dest, social_group, total_bits, trans_ts, offset_ts):
        # the number of appdata waiting for services
        datas_count = len(self.app.datas[social_group])
        # the serving appdata index
        data_delivering = 0
        # the appdatas collected in the package
        package_datas = []
        # while there's still space for allocation
        remain_bits = total_bits
        while(remain_bits > 0 and data_delivering < datas_count):
            appdata = self.app.datas[social_group][data_delivering]
            data_size = remain_bits if appdata.bits > remain_bits else appdata.bits
            package_datas.append(
                AppData(
                    appdata.header,
                    data_size,
                    appdata.offset
                )
            )
            # consume available bits
            remain_bits -= data_size
            # consume remaining bits
            appdata.bits -= data_size
            # add delivered bits
            appdata.offset += data_size
            # if there's no remaining bits left, work on to the next appdata
            if(appdata.bits == 0):
                data_delivering += 1

        # Remove appdata from list if it has no remaining bits to transmit
        self.app.datas[social_group] = self.app.datas[social_group][data_delivering:]
        package = NetworkPackage(
            self,
            dest,
            social_group,
            total_bits - remain_bits,
            package_datas,
            trans_ts,
            offset_ts
        )

        # log
        DEBUG.Log(
            "[{}][package][{}]:create.({})".format(
                self.name,
                social_group.fname.lower(),
                package
            )
        )

        # Create Package
        return package

    # Send package
    def SendPackage(self, package):
        self.pkg_in_proc[LinkType.UPLINK].append(
            package
        )
        package.dest.ReceivePackage(package)

    # Serves uploading/downloading packages
    def ProcessPackage(self, timeslot):
        # Download
        for pkg in self.pkg_in_proc[LinkType.DOWNLINK]:
            if timeslot == (pkg.offset_ts + pkg.trans_ts):
                # log
                DEBUG.Log(
                    "[{}][package][{}]:receive.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg,
                    )
                )
                self.PackageDelivered(pkg)
                self.con_state[pkg.src.name].rec.ChangeState(
                    ConnectionState.Success
                )
            else:
                self.con_state[pkg.src.name].rec.ChangeState(
                    ConnectionState.Transmit
                )
        # .remove delivered packages
        self.pkg_in_proc[LinkType.DOWNLINK] = [
            pkg
            for pkg in self.pkg_in_proc[LinkType.DOWNLINK]
            if (pkg.offset_ts+pkg.trans_ts) > timeslot
        ]
        # Upload
        for pkg in self.pkg_in_proc[LinkType.UPLINK]:
            if(pkg.offset_ts == timeslot):
                DEBUG.Log(
                    "[{}][package][{}]:deliver.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg,
                    )
                )
                self.con_state[pkg.dest.name].rec.ChangeState(
                    ConnectionState.Success
                )
            else:
                self.con_state[pkg.dest.name].rec.ChangeState(
                    ConnectionState.Transmit
                )
        # . remove sent packages
        self.pkg_in_proc[LinkType.UPLINK] = [
            pkg
            for pkg in self.pkg_in_proc[LinkType.UPLINK]
            if(pkg.offset_ts) > timeslot
        ]

    # Process package that're delivered
    def PackageDelivered(self, package):
        for appdata in package.appdatas:
            self.app.RecvData(package.social_group, appdata)

    # Select the service base station according to the social type provided.
    def SelectSocialBS(self, social_type):
        if (social_type == SocialGroup.CRITICAL):
            return (
                self.sub_sg_bs[BaseStationType.UMI][social_type] if
                self.sub_sg_bs[BaseStationType.UMI][social_type] != None
                else self.sub_sg_bs[BaseStationType.UMA][social_type])
        elif (social_type == SocialGroup.GENERAL):
            return (
                self.sub_sg_bs[BaseStationType.UMI][social_type] if
                (self.sub_sg_bs[BaseStationType.UMI][social_type] !=
                 None and len(self.app.datas[SocialGroup.CRITICAL]) == 0)
                else self.sub_sg_bs[BaseStationType.UMA][social_type])
        else:
            return (
                self.sub_sg_bs[BaseStationType.UMA][social_type] if
                self.sub_sg_bs[BaseStationType.UMA][social_type] != None
                else self.sub_sg_bs[BaseStationType.UMI][social_type])

    # Function called by BaseStationControllers to send packages
    def ReceivePackage(self, package,):
        self.pkg_in_proc[LinkType.DOWNLINK].append(package)

    # Update & Clean up the connection
    def LinkStateUpdate(self):
        ghost_con = []
        for name, struct in self.con_state.items():
            # if no one's sharing this connection, the recorder is redundant
            if (struct.share <= 0):
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
        if (build):
            # Create connection recorder for this base station if not exists
            if (opponent.name not in self.con_state):
                self.con_state[opponent.name] = SharedConnection(
                    ConnectionRecorder(self, opponent))
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
