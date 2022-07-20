#!/usr/bin/env python3

import time
import sys
import queue
import dronecan
from dronecan import uavcan


CAN_DEVICE_TYPE = "can-slcan"


class DroneCanCommunicator:
    """
    Simple wrap on droneCan
    Based on example: https://legacy.uavcan.org/Implementations/Pyuavcan/Tutorials/
    """
    def __init__(self, can_device_type, node_id=42, node_name="uavcan communicator"):
        """
        Simply create a node without starting it.
        param can_device_type - could be 'serial' or 'can-slcan'
        """
        self.subs = []
        self.node = None

        if can_device_type == "can-slcan":
            kawrgs = {"can_device_name" : "slcan0",
                      "bustype" : "socketcan",
                      "bitrate" : 1000000}
        else:
            sys.exit()

        node_info = uavcan.protocol.GetNodeInfo.Response()
        node_info.name = node_name
        node_info.software_version.major = 0
        node_info.software_version.minor = 2
        node_info.hardware_version.unique_id = b'12345'

        self.node = dronecan.make_node(node_id=node_id, node_info=node_info, **kawrgs)
        self.subscribe(uavcan.equipment.power.CircuitStatus, self.circuit_status_callback)
        self.subscribe(uavcan.protocol.NodeStatus, self.node_status_callback)

    def __del__(self):
        if self.node is not None:
            self.node.close()

    def subscribe(self, data_type, callback):
        """
        param data_type - https://legacy.uavcan.org/Specification/7._List_of_standard_data_types/
        param callback - any function with single parameter - event
        Example:
        data_type = uavcan.protocol.NodeStatus
        callback = lambda event: print(uavcan.to_yaml(event))
        communicator.subscribe(data_type, callback)
        """
        self.subs.append(self.node.add_handler(data_type, callback))

    def publish(self, data_type):
        """
        param data_type - https://legacy.uavcan.org/Specification/7._List_of_standard_data_types/
        Example:
        fix2 = uavcan.equipment.gnss.Fix2(pdop=10)
        communicator.publish(fix2)
        """
        try:
            self.node.broadcast(data_type)
        except uavcan.driver.common.TxQueueFullError as err:
            print(f"tx uavcan.driver.common.TxQueueFullError {err}")
        except queue.Full as err:
            print(f"tx queue.Full {err}")

    def spin(self, period=0.00001):
        """
        period - blocking time, where -1 means infinity, 0 means non-blocking
        """
        try:
            if period == -1:
                self.node.spin()
            else:
                self.node.spin(period)
        except dronecan.transport.TransferError as err:
            print(f"spin uavcan.transport.TransferError {err}")
        except queue.Full as err:
            print(f"spin queue.Full {err}")
        except uavcan.driver.common.TxQueueFullError as err:
            print(f"spin uavcan.driver.common.TxQueueFullError {err}")

    def circuit_status_callback(self, event):
        print('get circuit status')

    def node_status_callback(self, event):
        print('get node status')


if __name__=="__main__":
    try:
        communicator = None
        while communicator is None:
            try:
                communicator = DroneCanCommunicator(CAN_DEVICE_TYPE)
            except OSError as e:
                print(f"{e}. Check you device. Trying to reconnect.")
                time.sleep(2)
        print("UavcanCommunicatorV0 has been successfully created")

        while True:
            communicator.spin()

    except KeyboardInterrupt:
        print("Interrupt occurs")
        sys.exit(0)