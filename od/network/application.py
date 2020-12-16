from od.social import SocialGroup
from od.config import NET_SG_RND_REQ_SIZE
from numpy import random
import od.vars as GV


class AppDataHeader:
    def __init__(self, owner, total_bits, serial: int, at: float):
        self.owner = owner
        self.total_bits = total_bits
        self.serial = serial
        self.at = at
        self.id = "{}-{}".format(self.owner.name, self.serial)

    def __str__(self):
        return "AppDataHeader({},{}b,{}s)".format(
            self.id,
            self.total_bits,
            self.at
        )


class AppData:
    def __init__(self, header: AppDataHeader, bits: int, offset: int):
        self.header = header
        self.bits = bits
        self.offset = offset

    def __str__(self):
        return "Appdata({}-{},{}o+{}b)".format(
            self.header.owner.name,
            self.header.serial,
            self.offset,
            self.bits
        )


class Application:
    def __init__(self, owner):
        self.data_inbox = {}
        self.owner = owner

    # function called by application owner
    # executes DataIntact() if the whole data became "intact"
    # after receiving this appdata segment.
    def RecvData(self, social_group: SocialGroup, appdata: AppData):
        # received the first data from the data's owner
        if (appdata.header.owner.name not in self.data_inbox):
            self.data_inbox[appdata.header.owner.name] = {}
        # datas, of the same owner as the received one, that have been received by this application.
        owner_datas = self.data_inbox[appdata.header.owner.name]
        # the delivered data is a new one, create record
        if(appdata.header.serial not in owner_datas):
            owner_datas[appdata.header.serial] = AppData(
                appdata.header,
                0,
                0
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
                self.data_inbox[header.owner.name][header.serial]
            )
        )
        # sys.exit()


class VehicleApplication(Application):
    def __init__(self, vehicle):
        super().__init__(vehicle)
        # The last time when this vehicle recorder generates upload request
        self.prev_gen_time = 0
        # The social group upload data list
        self.datas = [[] for i in SocialGroup]
        # Package counter for upload req
        self.data_counter = 0

    def Run(self):
        self.SendData()

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
            )
        )
        GV.STATISTIC_RECORDER.VehicleReceivedIntactAppdata(
            social_group,
            self.owner,
            appdata.header
        )

    # Send application data
    def SendData(self):
        if (GV.SUMO_SIM_INFO.getTime() - self.prev_gen_time > 1):
            self.prev_gen_time = GV.SUMO_SIM_INFO.getTime()
            for group in SocialGroup:
                # TODO: Make the random poisson be social group dependent
                for _ in range(random.poisson(GV.APP_DATA_POISSON)):
                    # get the range of random generated data size (byte)
                    data_size_rnd_range = NET_SG_RND_REQ_SIZE[group]
                    # size of data (bit)
                    data_size = random.randint(
                        data_size_rnd_range[0],
                        data_size_rnd_range[1] + 1
                    ) * 8

                    # create appdata
                    self.datas[group].append(
                        AppData(
                            AppDataHeader(
                                self.owner,
                                data_size,
                                self.data_counter,
                                GV.SUMO_SIM_INFO.getTime()
                            ),
                            data_size,
                            0
                        )
                    )
                    self.data_counter += 1


class NetworkCoreApplication(Application):
    def __init__(self, owner):
        super().__init__(owner)

    def DataIntact(self, social_group: SocialGroup, appdata: AppData):
        GV.DEBUG.Log(
            "[{}][app][{}]:data intact.({})".format(
                self.owner.name,
                social_group.fname.lower(),
                appdata.header
            )
        )
        # propagate the appdata to other base stations
        self.owner.StartPropagation(
            social_group,
            appdata.header
        )
