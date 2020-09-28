import sys
from globs import SUMO_STEP_INFO, SocialGroup, NET_SG_RND_REQ_SIZE
from sim_log import DEBUG, ERROR
from numpy import random


class AppDataHeader:
    def __init__(self, owner, total_bits, serial: int, at: float):
        self.owner = owner
        self.total_bits = total_bits
        self.serial = serial
        self.at = at


class AppData:
    def __init__(self, header: AppDataHeader, bits: int, offset: int):
        self.header = header
        self.bits = bits
        self.offset = offset


class Application:
    def __init__(self):
        self.data_inbox = {}

    # function called by it's owner
    # returns true if this appdata became "intact" after receive
    # any other cases, e.g. appdata is already intact , will return false
    def ReceiveData(self, social_group: SocialGroup, appdata: AppData):
        # receive the first data from the data's owner
        if (appdata.header.owner.name not in self.data_inbox):
            self.data_inbox[appdata.header.owner.name] = {}
        # data, of the same owner as the received on, that've been received by this application.
        owner_datas = self.data_inbox[appdata.header.owner.name]
        # the receive data is a new one, create record
        if(appdata.header.serial not in owner_datas):
            if(appdata.offset != 0):
                ERROR.Log("Error! first arrived appdata offset should be 0")
                sys.exit()
            owner_datas[appdata.header.serial] = AppData(
                appdata.header,
                appdata.bits,
                0
            )
            return False
        # the receive data is already intact
        elif(owner_datas[appdata.header.serial].bits ==
             owner_datas[appdata.header.serial].header.total_bits):
            return False
        # for deform data, process receive data
        deform_data = owner_datas[appdata.header.serial]
        # if receive data offset start before the deform data size
        # then this receive data might provide continuous bits to the deform data
        if(appdata.offset <= deform_data.bits):
            saved_bits = deform_data.bits
            income_offset = appdata.offset
            income_bits = appdata.bits
            deform_data.bits += (income_bits -
                                 (saved_bits-income_offset))
        # if receive data offset start after the deform data size
        # then this receive data provides advanced/non-continuous bits to the deform data
        else:
            # TODO: receive the data and save it
            ERROR.Log("ERROR!Received Advanced Appdata!!!")
        # if the appdata has became intact
        if(deform_data.bits == deform_data.header.total_bits):
            return True


class VehicleApplication(Application):
    def __init__(self, vehicle):
        super().__init__()
        self.vehicle = vehicle
        # The last time when this vehicle recorder generates upload request
        self.prev_gen_time = 0
        # The social group upload data list
        self.sg_appdatas = [[] for i in SocialGroup]
        # Package counter for upload req
        self.appdata_counter = 0

    def Run(self):
        self.GenerateSocialGroupAppData()

    def ReceiveData(self, social_group: SocialGroup, appdata: AppData):
        # if the appdata was sent by this application, don't receive it.
        if(appdata.header.owner == self.vehicle):
            return
        # if the appdata became intact
        if(Application.ReceiveData(self, social_group, appdata)):
            header = appdata.header
            DEBUG.Log(
                "[{}-app]:app data received.(origin:{}-{} bits:{}b at:{}s)".format(
                    self.vehicle.name,
                    header.owner.name,
                    header.serial,
                    header.total_bits,
                    header.at,
                )
            )

    # Randomly generate application data for different social groups
    def GenerateSocialGroupAppData(self):
        if (SUMO_STEP_INFO.time - self.prev_gen_time > 1):
            self.prev_gen_time = SUMO_STEP_INFO.time
            for group in SocialGroup:
                # TODO: Make the random poisson be social group dependent
                for _ in range(random.poisson(1)):
                    # get the range of random generated data size (byte)
                    data_size_rnd_range = NET_SG_RND_REQ_SIZE[group]
                    # size of data (bit)
                    data_size = random.randint(
                        data_size_rnd_range[0],
                        data_size_rnd_range[1] + 1
                    ) * 8

                    # create appdata
                    self.sg_appdatas[group].append(
                        AppData(
                            AppDataHeader(
                                self.vehicle,
                                data_size,
                                self.appdata_counter,
                                SUMO_STEP_INFO.time
                            ),
                            data_size,
                            0
                        )
                    )
                    self.appdata_counter += 1


class NetworkCoreApplication(Application):
    def __init__(self, core_ctrlr):
        super().__init__()
        self.core_ctrlr = core_ctrlr

    def ReceiveData(self, social_group: SocialGroup, appdata: AppData):
        if(Application.ReceiveData(self, social_group, appdata)):
            header = appdata.header
            DEBUG.Log(
                "[{}-app]:app data received.(origin:{}-{} bits:{}b at:{}s)".format(
                    self.core_ctrlr.name,
                    header.owner.name,
                    header.serial,
                    header.total_bits,
                    header.at,
                )
            )
            # propagate the appdata to other base stations
            self.core_ctrlr.StartPropagation(
                social_group,
                header
            )
