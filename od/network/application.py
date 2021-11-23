from __future__ import annotations
from numpy import random
from od import social
from od.network.types import BaseStationType
from od.network.appdata import AppData, AppDataHeader
from od.env.config import (NET_QoS_RND_REQ_SIZE, NET_SECONDS_PER_STEP,
                           NET_QoS_RND_REQ_NUM, NET_QoS_RND_REQ_NUM_TIME_SCALE,
                           NET_TIMEOUT_SECONDS)
from od.social.group import SocialGroup, QoSLevel
from od.misc.types import DebugMsgType
import od.vars as GV


class Application:
    def __init__(self, owner):
        self.sg_data_inbox = {}
        self.owner = owner

    # function called by application owner
    # executes DataIntact() if the whole data became "intact"
    # after receiving this appdata segment.
    def RecvData(self, social_group: SocialGroup, appdata: AppData):
        # receive the first data of the social group
        if (social_group not in self.sg_data_inbox):
            self.sg_data_inbox[social_group] = {}
        # received the first data from the data's owner
        if (appdata.header.owner.name not in self.sg_data_inbox[social_group]):
            self.sg_data_inbox[social_group][appdata.header.owner.name] = {}
        # datas, of the same owner as the received one, that have been received by this application.
        owner_datas = self.sg_data_inbox[social_group][appdata.header.owner.name]
        # the delivered data is a new one, create record
        if(appdata.header.serial not in owner_datas):
            owner_datas[appdata.header.serial] = AppData(
                appdata.header,
                0,
                0
            )

            GV.DEBUG.Log(
                "[{}][app][{}]:data intro.({})".format(
                    self.owner.name,
                    social_group.fname.lower(),
                    appdata.header
                ),
                DebugMsgType.NET_APPDATA_INFO
            )
        # the delivered data is already intact
        elif(owner_datas[appdata.header.serial].bits ==
             owner_datas[appdata.header.serial].header.total_bits):
            return

        # for deform data, process receive data
        deform_data = owner_datas[appdata.header.serial]
        # if receive data offset start before the deform data size
        # then this receive data might provide continuous bits to the deform data
        if(appdata.offset <= deform_data.bits):
            saved_bits = deform_data.bits
            income_offset = appdata.offset
            income_bits = appdata.bits
            deform_data.bits += (income_bits -
                                 (saved_bits - income_offset))
        # if receive data offset start after the deform data size
        # then this receive data provides advanced/non-continuous bits to the deform data
        else:
            self.RecvAdvanceData(social_group, appdata)
            return

        # if the appdata has became intact
        if(deform_data.bits >= deform_data.header.total_bits):
            self.DataIntact(social_group, appdata)

    def DataIntact(self, social_group: SocialGroup, appdata: AppData):
        print("Data Intact")

    def RecvAdvanceData(self, social_group: SocialGroup, appdata: AppData):
        # TODO: receive the data and save it
        header = appdata.header
        GV.ERROR.Log(
            "[{}][app][{}]receive advance appdata!(new:{}|old:{})".format(
                self.owner.name,
                social_group,
                appdata,
                self.sg_data_inbox[social_group][header.owner.name][header.serial]
            )
        )


class VehicleApplication(Application):
    def __init__(self, vehicle):
        super().__init__(vehicle)
        # The social groups vehicles are interest in.
        self.veh_social_groups = vehicle.social_groups
        # The last time when this vehicle recorder generates upload request
        self.data_stack = {sg: 0 for sg in self.veh_social_groups}
        # The social group upload data list
        self.sg_data_queue = {sg: [] for sg in self.veh_social_groups}
        # Package counter for upload req
        self.data_counter = 0

    def Run(self):
        self.SpawnData()

    # Receive application data
    def RecvData(self, social_group: SocialGroup, appdata: AppData):
        # if the appdata was sent by this application, don't receive it.
        if(appdata.header.owner == self.owner):
            return
        # if the appdata became intact
        Application.RecvData(self, social_group, appdata)

    def DataIntact(self, social_group: SocialGroup, appdata: AppData):
        GV.DEBUG.Log(
            "[{}][app][{}]:data intact.({})".format(
                self.owner.name,
                social_group.fname.lower(),
                appdata.header
            ),
            DebugMsgType.NET_APPDATA_INFO
        )
        GV.STATISTIC_RECORDER.VehicleReceivedIntactAppdata(
            social_group,
            self.owner,
            appdata.header
        )

    # Send application data
    def SpawnData(self):
        current_time = GV.SUMO_SIM_INFO.getTime()
        for sg in self.veh_social_groups:
            # ignore data spawn if social group has a centralized source.(no edge sources)
            if(sg.reader):
                continue
            # stack data request for data generation.
            self.data_stack[sg] += random.poisson(NET_QoS_RND_REQ_NUM[sg.qos] * GV.NET_QoS_RND_REQ_MOD[sg.qos]) * \
                NET_SECONDS_PER_STEP / NET_QoS_RND_REQ_NUM_TIME_SCALE
            # generate network app data if the stack has sufficient data.
            while(self.data_stack[sg] > 1):
                # remove data from stack.
                self.data_stack[sg] -= 1

                # get the range of random generated data size (byte)
                data_size_rnd_range = NET_QoS_RND_REQ_SIZE[sg.qos]

                # size of data (bit)
                data_size = random.randint(
                    data_size_rnd_range[0],
                    data_size_rnd_range[1] + 1
                ) * 8

                # create appdata
                appdata = AppData(
                    AppDataHeader(
                        self.owner,
                        data_size,
                        self.data_counter,
                        current_time
                    ),
                    data_size,
                    0
                )
                self.sg_data_queue[sg].append(appdata)

                # Add counter
                self.data_counter += 1

                # Log
                GV.DEBUG.Log(
                    "[{}][app][{}]:data spawn.({})".format(
                        self.owner.name,
                        sg.fname.lower(),
                        appdata.header
                    ),
                    DebugMsgType.NET_APPDATA_INFO
                )
                # Statistics
                GV.STATISTIC_RECORDER.VehicleCreateAppdata(sg, appdata.header)

    # Check for timeout application data of GENERAL QoS.
    # def CheckTimeout(self):
    #     current_time = GV.SUMO_SIM_INFO.getTime()
    #     for sg in [x for x in SocialGroup if x.qos == QoSLevel.GENERAL]:
    #         drop_index = 0
    #         for appdata in self.sg_data_queue[sg]:
    #             if appdata.header.at + NET_TIMEOUT_SECONDS <= current_time:
    #                 drop_index += 1
    #             else:
    #                 break
    #         if(drop_index > 0):
    #             # record over time.
    #             GV.STATISTIC_RECORDER.VehicleOverTimeAppdata(
    #                 sg,
    #                 map(lambda x: x.header, self.sg_data_queue[sg][:drop_index])
    #             )
    #             # drop over time datas.
    #             self.sg_data_queue[sg][drop_index:]


# class NetworkCoreApplication(Application):
#     def __init__(self, owner):
#         super().__init__(owner)

#     def DataIntact(self, social_group: SocialGroup, appdata: AppData):
#         GV.DEBUG.Log(
#             "[{}][app][{}]:data intact.({})".format(
#                 self.owner.name,
#                 social_group.fname.lower(),
#                 appdata.header
#             ),
#             DebugMsgType.NET_APPDATA_INFO
#         )
#         # propagate the appdata to other base stations
#         self.owner.StartPropagation(
#             social_group,
#             appdata.header
#         )


class BaseStationApplicationUMA(Application):
    def __init__(self, owner):
        super().__init__(owner)

    def DataIntact(self, social_group: SocialGroup, appdata: AppData):
        GV.DEBUG.Log(
            "[{}][app][{}]:data intact.({})".format(
                self.owner.name,
                social_group.fname.lower(),
                appdata.header
            ),
            DebugMsgType.NET_APPDATA_INFO
        )
        # propagate general data to the core for further process.
        if(social_group.qos == QoSLevel.GENERAL):
            GV.NET_CORE_CONTROLLER.Propagate(
                self.owner,
                social_group,
                appdata.header
            )
        # propagate the appdata to other vehicles in range.
        self.owner.Propagate(
            self.owner,
            social_group,
            appdata.header
        )


class BaseStationApplicationUMI(Application):
    def __init__(self, owner):
        super().__init__(owner)

    def DataIntact(self, social_group: SocialGroup, appdata: AppData):
        GV.DEBUG.Log(
            "[{}][app][{}]:data intact.({})".format(
                self.owner.name,
                social_group.fname.lower(),
                appdata.header
            ),
            DebugMsgType.NET_APPDATA_INFO
        )
        if(social_group.qos == QoSLevel.CRITICAL):
            # propagate the appdata to other vehicles in range.
            self.owner.Propagate(
                self.owner,
                social_group,
                appdata.header
            )
        # propagate the appdata to the network core controller.
        GV.NET_CORE_CONTROLLER.Propagate(
            self.owner,
            social_group,
            appdata.header
        )


def BaseStationApplication(bs_ctrlr):
    if(bs_ctrlr.type == BaseStationType.UMA):
        return BaseStationApplicationUMA(bs_ctrlr)
    elif(bs_ctrlr.type == BaseStationType.UMI):
        return BaseStationApplicationUMI(bs_ctrlr)
    return None
