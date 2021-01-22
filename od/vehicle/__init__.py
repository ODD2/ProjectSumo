from .connection import ConnectionState, ConnectionRecorder, SharedConnection
from .monitor import NetworkStatusMonitor
from od.network.types import BaseStationType, LinkType
from od.network.package import NetworkPackage
from od.network.application import VehicleApplication
from od.network.appdata import AppData
from od.social import SocialGroup
from od.config import VEH_MOVE_BS_CHECK, SUMO_SIM_GUI
from od.misc.types import DebugMsgType
from traci import vehicle
import od.vars as GV
import traci.constants as tc


class VehicleRecorder():
    # Constructor
    def __init__(self, name):
        # Vehicle ID
        self.name = name

        # Traci Subscribe
        vehicle.subscribe(self.name, [tc.VAR_POSITION])

        # Vehicle Position
        self.pos = (0, 0)

        # Vehicle Position of Latest Base Station Subscribe Process
        self.chk_pos = (0, 0)

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
        self.Leave()

    # Update per sumo simulation step
    def UpdateSS(self):
        self.UpdateVehicleInfo()
        self.SelectBestSocialBS()
        self.LinkStateUpdate()

    # Update per network simulation step
    def UpdateNS(self, ns):
        self.app.Run()
        self.RequestUploadResource()

    # Update per timeslot
    def UpdateT(self, ts):
        self.ProcessPackage(ts)

    # Update vehicle info from sumo
    def UpdateVehicleInfo(self):
        self.pos = vehicle.getSubscriptionResults(self.name)[tc.VAR_POSITION]

    # Check if the latest subscription base stations still provide services
    def CheckSubscribeBSValidity(self):
        invalid_bs = []
        for bs_type in BaseStationType:
            for social_group in SocialGroup:
                if (self.sub_sg_bs[bs_type][social_group] == None):
                    continue
                else:
                    bs_ctrl = self.sub_sg_bs[bs_type][social_group]
                    if (bs_ctrl not in invalid_bs):
                        distance = pow((self.pos[0] - bs_ctrl.pos[0])**2 +
                                       (self.pos[1] - bs_ctrl.pos[1])**2, 0.5)
                        if (distance > bs_ctrl.radius):
                            self.UnsubscribeBS(bs_type, social_group)
                            invalid_bs.append(bs_ctrl)
                    else:
                        self.UnsubscribeBS(bs_type, social_group)
        if(len(invalid_bs) > 0):
            return False
        else:
            return True

    # Find and subscribe the base station that provides the best connectivity according to it's social group,
    # if the vehicle has move away for a specific amount of distance,
    # or if the connected base station became out of service.
    def SelectBestSocialBS(self):
        # the distance between latest base station check position.
        d = pow((self.pos[0] - self.chk_pos[0])**2 +
                (self.pos[1] - self.chk_pos[1])**2,
                0.5)

        # verify check conditions
        if(d < VEH_MOVE_BS_CHECK and self.CheckSubscribeBSValidity()):
            return

        # update the check position
        self.chk_pos = self.pos
        # define container
        bs_near = [[None, float("inf")] for i in BaseStationType]
        # find closest in range base station
        for bs_ctrl in GV.NET_STATION_CONTROLLER:
            x = (self.pos[0] - bs_ctrl.pos[0])
            if(x > bs_ctrl.radius):
                continue
            y = (self.pos[1] - bs_ctrl.pos[1])
            if(y > bs_ctrl.radius):
                continue
            d = pow(x**2 + y**2, 0.5)
            if d > bs_ctrl.radius:
                continue
            ctrl_range = bs_near[bs_ctrl.type]
            if d > ctrl_range[1]:
                continue
            ctrl_range[0] = bs_ctrl
            ctrl_range[1] = d
        # cache net status
        GV.NET_STATUS_CACHE.GetMultiNetStatus([
            (self, ctrl_range[0], sg)
            for sg in SocialGroup
            for ctrl_range in bs_near
            if ctrl_range[0] != None
        ])

        # subscribe base station
        for bs_type in BaseStationType:
            for sg in SocialGroup:
                # get the base station controller
                bs_ctrl = bs_near[bs_type][0]
                # there's no base station of this type
                if(bs_ctrl == None):
                    continue
                # subscribe to base station
                self.SubscribeBS(
                    bs_type,
                    sg,
                    bs_ctrl
                )

    # Subscribe base station
    def SubscribeBS(self, bs_type, social_group: SocialGroup, bs_ctrl):
        # if the desire base station was already subscribed
        if self.sub_sg_bs[bs_type][social_group] == bs_ctrl:
            return
        else:
            self.UnsubscribeBS(bs_type, social_group)

        # Subscribe the new one
        self.sub_sg_bs[bs_type][social_group] = bs_ctrl
        # Register to base station, too.
        bs_ctrl.VehicleSubscribe(self, social_group)
        # Update connection state
        self.ConnectionChange(True, bs_ctrl)

    # Unsubscribe base station
    def UnsubscribeBS(self, bs_type, social_group: SocialGroup):
        # There is no subscription, nothing to do.
        if (self.sub_sg_bs[bs_type][social_group] == None):
            return
        # Unsubscribe the base station
        bs_ctrl = self.sub_sg_bs[bs_type][social_group]
        self.sub_sg_bs[bs_type][social_group] = None
        # Unregister from base station
        bs_ctrl.VehicleUnsubscribe(self, social_group)
        # Update connection state
        self.ConnectionChange(False, bs_ctrl)

    # Submit upload requests
    def RequestUploadResource(self):
        for social_group in SocialGroup:
            if (len(self.app.datas[social_group]) > 0):
                bs_ctrl = self.SelectSocialBS(social_group)
                if (bs_ctrl != None):
                    sg_total_bits = 0
                    for appdata in self.app.datas[social_group]:
                        sg_total_bits += appdata.bits
                    bs_ctrl.ReceiveUploadRequest(
                        self,
                        social_group,
                        sg_total_bits,
                    )
                else:
                    GV.ERROR.Log("Error: No BS to serve request.")

    # Function called by BaseStationController to give resource block to upload requests
    def UploadResourceGranted(self, bs_ctrl, social_group: SocialGroup, total_bits, trans_ts, offset_ts):
        self.SendPackage(
            self.CreatePackage(
                bs_ctrl,
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
            ),
            DebugMsgType.NET_PKG_INFO
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
        self.ProcessUplinkPackage(timeslot)
        self.ProcessDownlinkPackage(timeslot)

    def ProcessDownlinkPackage(self, timeslot):
        # exit if no package to process
        if(len(self.pkg_in_proc[LinkType.DOWNLINK]) == 0):
            return

        # Download
        pkg_in_proc = []
        for pkg in self.pkg_in_proc[LinkType.DOWNLINK]:
            if timeslot == pkg.end_ts:
                # log
                GV.DEBUG.Log(
                    "[{}][package][{}]:receive.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg,
                    ),
                    DebugMsgType.NET_PKG_INFO
                )
                # process received package
                self.PackageDelivered(pkg)
                # Connection display are required for gui only.
                if(SUMO_SIM_GUI):
                    # change connection state
                    self.con_state[pkg.src.name].rec.ChangeState(
                        ConnectionState.Success
                    )
            else:
                # update connection state
                pkg_in_proc.append(pkg)
                # Connection display are required for gui only.
                if(SUMO_SIM_GUI):
                    self.con_state[pkg.src.name].rec.ChangeState(
                        ConnectionState.Transmit
                    )
        # .remove delivered packages
        self.pkg_in_proc[LinkType.DOWNLINK] = pkg_in_proc

    def ProcessUplinkPackage(self, timeslot):
        # exit if no package to process
        if(len(self.pkg_in_proc[LinkType.UPLINK]) == 0):
            return
        # Upload
        pkg_in_proc = []
        for pkg in self.pkg_in_proc[LinkType.UPLINK]:
            if(timeslot == pkg.offset_ts):
                GV.DEBUG.Log(
                    "[{}][package][{}]:deliver.({})".format(
                        self.name,
                        pkg.social_group.fname.lower(),
                        pkg,
                    ),
                    DebugMsgType.NET_PKG_INFO
                )
                # Connection display are required for gui only.
                if(SUMO_SIM_GUI):
                    # update connection state
                    self.con_state[pkg.dest.name].rec.ChangeState(
                        ConnectionState.Success
                    )
            else:
                pkg_in_proc.append(pkg)
                # Connection display are required for gui only.
                if(SUMO_SIM_GUI):
                    # update connection state
                    self.con_state[pkg.dest.name].rec.ChangeState(
                        ConnectionState.Transmit
                    )
        # . remove sent packages
        self.pkg_in_proc[LinkType.UPLINK] = pkg_in_proc

    # Process package that're delivered
    def PackageDelivered(self, package: NetworkPackage):
        for appdata in package.appdatas:
            self.app.RecvData(package.social_group, appdata)

    # Select the service base station according to the social type provided.
    def SelectSocialBS(self, social_group: SocialGroup):
        # 2021/1/11 Scenario:
        # UMIs are spcificly for critical data, only Critical datas select UMI
        # as a type of upload destination. Any other social datas never select a UMI.
        if (social_group == SocialGroup.CRITICAL):
            return (
                self.sub_sg_bs[BaseStationType.UMI][social_group] if
                self.sub_sg_bs[BaseStationType.UMI][social_group] != None
                else self.sub_sg_bs[BaseStationType.UMA][social_group]
            )
        # elif (social_group == SocialGroup.GENERAL):
        #     return (
        #         self.sub_sg_bs[BaseStationType.UMI][social_group] if
        #         (self.sub_sg_bs[BaseStationType.UMI][social_group] !=
        #          None and len(self.app.datas[SocialGroup.CRITICAL]) == 0)
        #         else self.sub_sg_bs[BaseStationType.UMA][social_group]
        #     )
        else:
            return self.sub_sg_bs[BaseStationType.UMA][social_group]

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

        # remove non-shared existing connections
        for name in ghost_con:
            self.con_state.pop(name)

    # The Connection manager to manage connection between self and others
    def ConnectionChange(self, build, opponent):
        # Connection display are required for gui only.
        if(not SUMO_SIM_GUI):
            return

        if (build):
            # Create connection recorder for this base station if not exists
            if (opponent.name not in self.con_state):
                self.con_state[opponent.name] = SharedConnection(
                    ConnectionRecorder(self, opponent)
                )
            self.con_state[opponent.name].share += 1
        else:
            if(opponent.name in self.con_state):
                # Break connection
                self.con_state[opponent.name].share -= 1

    # Leave Simulation
    def Leave(self):
        # UnSubscribe Any Base Station
        for i in BaseStationType:
            for j in SocialGroup:
                self.UnsubscribeBS(i, j)
        # Clear connection recorders
        for name in self.con_state:
            self.con_state[name].rec.Clean()
        self.con_state = {}
