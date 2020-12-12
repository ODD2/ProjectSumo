from .connection import ConnectionState, ConnectionRecorder, SharedConnection
from .monitor import NetworkStatusMonitor
from od.network.types import BaseStationType, LinkType
from od.network.package import NetworkPackage
from od.network.application import AppData, VehicleApplication
from od.social import SocialGroup
import od.vars as GV
import traci


class VehicleRecorder():
    # Constructor
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

    # Destructor
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
        GV.TRACI_LOCK.acquire()
        self.pos = traci.vehicle.getPosition(self.name)
        GV.TRACI_LOCK.release()

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
        for bs_ctrlr in GV.NET_STATION_CONTROLLER:
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
                multi_net_status = GV.NET_STATUS_CACHE.GetMultiNetStatus([
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
    def SubscribeBS(self, bs_type, social_group: SocialGroup, bs_ctrlr):
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
    def UnsubscribeBS(self, bs_type, social_group: SocialGroup):
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
                    GV.ERROR.Log("Error: No BS to serve request.")

    # Function called by BaseStationController to give resource block to upload requests
    def UploadResourceGranted(self, bs_ctrlr, social_group: SocialGroup, total_bits, trans_ts, offset_ts):
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
    def CreatePackage(self, dest, social_group: SocialGroup, total_bits, trans_ts, offset_ts):
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
        GV.DEBUG.Log(
            "[{}][package][{}]:create.({})".format(
                self.name,
                social_group.fname.lower(),
                package
            )
        )

        # Create Package
        return package

    # Send package
    def SendPackage(self, package: NetworkPackage):
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
                GV.DEBUG.Log(
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
                GV.DEBUG.Log(
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
    def PackageDelivered(self, package: NetworkPackage):
        for appdata in package.appdatas:
            self.app.RecvData(package.social_group, appdata)

    # Select the service base station according to the social type provided.
    def SelectSocialBS(self, social_group: SocialGroup):
        if (social_group == SocialGroup.CRITICAL):
            return (
                self.sub_sg_bs[BaseStationType.UMI][social_group] if
                self.sub_sg_bs[BaseStationType.UMI][social_group] != None
                else self.sub_sg_bs[BaseStationType.UMA][social_group])
        elif (social_group == SocialGroup.GENERAL):
            return (
                self.sub_sg_bs[BaseStationType.UMI][social_group] if
                (self.sub_sg_bs[BaseStationType.UMI][social_group] !=
                 None and len(self.app.datas[SocialGroup.CRITICAL]) == 0)
                else self.sub_sg_bs[BaseStationType.UMA][social_group])
        else:
            return (
                self.sub_sg_bs[BaseStationType.UMA][social_group] if
                self.sub_sg_bs[BaseStationType.UMA][social_group] != None
                else self.sub_sg_bs[BaseStationType.UMI][social_group])

    # Function called by BaseStationControllers to send packages
    def ReceivePackage(self, package: NetworkPackage):
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
