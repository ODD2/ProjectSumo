import traci
import numpy as np
import random
from queue import Queue
from net_model import GET_BS_CQI_SINR_5G, BASE_STATION_CONTROLLER, BaseStationController
from net_pack import NetworkTransmitResponse, NetworkTransmitRequest
from globs import SociatyGroup, NetObjLayer, BaseStationType


class BriefControllerInfo():
    def __init__(self, controller: BaseStationController, sinr: float, cqi: float):
        self.controller = controller
        self.sinr = sinr
        self.cqi = cqi


class VehicleRecorder:
    def __init__(self, vid):
        # Vehicle ID
        self.vid = vid
        # Network package queue settings with social grouping
        self.queue_pref = [None] * len(SociatyGroup)
        # Queue & Base station preferences
        self.queue_pref[SociatyGroup.GENERAL] = {
            "queue": Queue(0),
            "bs_pref": (
                lambda: self.umi_info if self.umi_info != None else self.uma_info
            )
        }
        self.queue_pref[SociatyGroup.CRITICAL] = {
            "queue": Queue(0),
            "bs_pref": (
                lambda: self.umi_info if self.umi_info != None else self.uma_info
            )
        }

        # Package counter
        self.package_counter = 0
        # Controllers infos
        self.uma_info = None
        self.umi_info = None
        # The last time when this vehicle recorder updates
        self.update_time = 0
        # Connection line settings
        self.connection_line_setting = {
            self.vid + "_umi_con": {
                "info": (lambda: self.umi_info),
            },
            self.vid + "_uma_con": {
                "info": (lambda: self.uma_info),
            }
        }
        # The connetion lines currently drawn in SUMO
        self.connection_lines = []

    # General routine called by main
    def Update(self, eng):
        UMI_BS = []
        UMA_BS = []
        self.umi_info = None
        self.uma_info = None
        vehicle_pos = traci.vehicle.getPosition(self.vid)

        # Find In-Range BaseStations
        for bs_controller in BASE_STATION_CONTROLLER:
            base_station_pos = bs_controller.pos
            distance = pow((vehicle_pos[0] - base_station_pos[0])**2 +
                           (vehicle_pos[1] - base_station_pos[1])**2, 0.5)
            if distance < bs_controller.radius:
                if bs_controller.type == BaseStationType.UMA:
                    UMA_BS.append(bs_controller)
                elif bs_controller.type == BaseStationType.UMI:
                    UMI_BS.append(bs_controller)

        # UMA Base Station Selection
        if len(UMA_BS) > 0:
            uma_cqi, uma_sinr = GET_BS_CQI_SINR_5G(
                eng,
                UMA_BS,
                vehicle_pos
            )
            # Select the best uma controller according to cqi
            index = np.argmax(uma_cqi)
            self.uma_info = BriefControllerInfo(
                UMA_BS[index],
                uma_sinr[index],
                uma_cqi[index]
            )

        # UMI Base Station Selection
        if len(UMI_BS) > 0:
            umi_cqi, umi_sinr = GET_BS_CQI_SINR_5G(
                eng,
                UMI_BS,
                vehicle_pos
            )
            # Select the best umi controller according to cqi
            index = np.argmax(umi_cqi)
            self.umi_info = BriefControllerInfo(
                UMI_BS[index],
                umi_sinr[index],
                umi_cqi[index]
            )

        # Create Critical Package
        if self.umi_info != None or self.uma_info != None:
            self.CreatePackage(
                random.randrange(190, 1100, 1)*8,
                SociatyGroup.CRITICAL)
            self.CreatePackage(
                random.randrange(190, 1100, 1)*8,
                SociatyGroup.GENERAL)

        # Arrage Transmission Requests
        for combine in self.queue_pref:
            queue = combine["queue"]
            if queue.qsize() > 0:
                base_station_info = combine["bs_pref"]()
                if base_station_info == None:
                    # print("No valid base station to transfer")
                    continue
                msg = queue.queue[0]
                msg.cqi = base_station_info.cqi
                msg.sinr = base_station_info.sinr
                base_station_info.controller.Request(msg)

        # Update Connection Line
        self.UpdateConnectionLines()

        # Record
        self.update_time = traci.simulation.getTime()

    # Function called by BaseStationController to give response to requests
    def Response(self, response: NetworkTransmitResponse):
        queue = self.queue_pref[response.social_group]["queue"]
        msg = queue.queue[0]
        if msg.name != response.name:
            print("Response: Error message corrupted")
            return

        if response.status:
            msg.bits -= response.bits
            # Message Fully Transmitted. Pop!
            if(msg.bits == 0):
                queue.get()

        # Update Connection Status
        self.UpdateTransmissionStatus(response.responder, response.status)

    # Central controller that manages package creation (NetworkTransmitRequest without cqi&sinr filled)
    # size in bits
    def CreatePackage(self, size, social_group):
        queue = self.queue_pref[social_group]["queue"]
        queue.put(NetworkTransmitRequest(
            str(self.package_counter),
            self,
            size,
            0,
            0,
            social_group
        ))
        self.package_counter += 1

    # General routine called by Update. Updates connection-line position and visibility
    def UpdateConnectionLines(self):
        vehicle_pos = traci.vehicle.getPosition(self.vid)

        for line_name, tools in self.connection_line_setting.items():
            if not tools["info"]() == None:
                controller = tools["info"]().controller
                if not line_name in self.connection_lines:
                    # Create line
                    traci.polygon.add(
                        line_name,
                        [vehicle_pos, controller.pos],
                        (0, 0, 0, 255),
                        False,
                        "Line",
                        NetObjLayer.CON_LINE, 0.1
                    )
                    # Record line as currently drawn
                    self.connection_lines.append(line_name)
                else:
                    # Update line positions
                    traci.polygon.setShape(
                        line_name,
                        [vehicle_pos, controller.pos]
                    )
                    traci.polygon.setColor(
                        line_name,
                        (0, 0, 0, 255)
                    )
            elif line_name in self.connection_lines:
                # Remove connection line
                traci.polygon.remove(line_name)
                self.connection_lines.remove(line_name)

    # Update connection-line color according to message response status
    def UpdateTransmissionStatus(self, connect_bs, success):
        updated = False
        for lineid, tools in self.connection_line_setting.items():
            controller_info = tools["info"]()
            if controller_info == None:
                continue
            if controller_info.controller == connect_bs:
                if lineid in self.connection_lines:
                    updated = True
                    if success:
                        traci.polygon.setColor(lineid, (0, 255, 0, 255))
                    else:
                        traci.polygon.setColor(lineid, (255, 0, 0, 255))
                break

        if not updated:
            print("UpdateTransmissionStatus: Error!")

    def Clear(self):
        # Clear Lines
        for line_id in self.connection_lines:
            traci.polygon.remove(line_id)
        self.connection_lines = []

    def __del__(self):
        self.Clear()
