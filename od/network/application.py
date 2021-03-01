from __future__ import annotations
from numpy import random
from od.network.types import BaseStationType
from od.network.appdata import AppData, AppDataHeader
from od.config import (NET_SG_RND_REQ_SIZE, NET_SECONDS_PER_STEP,
                       NET_SG_RND_REQ_NUM, NET_SG_RND_REQ_NUM_TIME_SCALE)
from od.social import SocialGroup
from od.misc.types import DebugMsgType
import od.vars as GV


class Application:
    def __init__(self, owner):
        self.sg_data_inbox = [{} for _ in SocialGroup]
        self.owner = owner

    # function called by application owner
    # executes DataIntact() if the whole data became "intact"
    # after receiving this appdata segment.
    def RecvData(self, social_group: SocialGroup, appdata: AppData):
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
        # sys.exit()


class VehicleApplication(Application):
    def __init__(self, vehicle):
        super().__init__(vehicle)
        # The last time when this vehicle recorder generates upload request
        self.data_stack = [0 for i in SocialGroup]
        # The social group upload data list
        self.datas = [[] for i in SocialGroup]
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
        for sg in SocialGroup:
            # TODO: Make the random poisson be social group dependent
            self.data_stack[sg] += random.poisson(NET_SG_RND_REQ_NUM[sg] * GV.NET_SG_RND_REQ_MOD[sg]) * \
                NET_SECONDS_PER_STEP / NET_SG_RND_REQ_NUM_TIME_SCALE
            # generate network app data if the stack has sufficient data.
            while(self.data_stack[sg] > 1):
                # remove data from stack.
                self.data_stack[sg] -= 1

                # get the range of random generated data size (byte)
                data_size_rnd_range = NET_SG_RND_REQ_SIZE[sg]

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
                        GV.SUMO_SIM_INFO.getTime()
                    ),
                    data_size,
                    0
                )
                self.datas[sg].append(appdata)

                # add counter
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


class NetworkCoreApplication(Application):
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
        # propagate the appdata to other base stations
        self.owner.StartPropagation(
            social_group,
            appdata.header
        )


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
        # propagate the appdata to other vehicles in range
        self.owner.ReceivePropagation(
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
        if(social_group == SocialGroup.CRITICAL):
            # propagate the appdata to other vehicles in range.
            self.owner.ReceivePropagation(
                social_group,
                appdata.header
            )
        # propagate the appdata to the network core controller.
        GV.NET_CORE_CONTROLLER.ReceivePropagation(
            social_group,
            appdata.header
        )


def BaseStationApplication(bs_ctrlr):
    if(bs_ctrlr.type == BaseStationType.UMA):
        return BaseStationApplicationUMA(bs_ctrlr)
    elif(bs_ctrlr.type == BaseStationType.UMI):
        return BaseStationApplicationUMI(bs_ctrlr)
    return None
