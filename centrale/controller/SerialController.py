from serial import Serial, SerialException, to_bytes
from serial.tools import list_ports
from model.Device import Device
from model.Response import Response


class SerialController:

    def __init__(self):
        self.__devices = {}

    def find_devices(self):
        ports = list_ports.comports()
        for port in ports:
            if port.device not in self.__devices:
                self.__devices[port.device] = Device()
        return self.__devices

    def check_connections(self):
        for device in self.__devices:
            connection = self.__devices[device].get_connection()
            if connection is None:
                connection = Serial(device, 19200, stopbits=1, bytesize=8)
                connection.flushInput()
                self.__devices[device].set_connection(connection)
            elif not connection.isOpen():
                connection.open()

    def output_instruction(self, device, instruction):
        self.__devices[device].get_connection().write(instruction)

    def read_input(self):
        input = {}
        for device in self.__devices:
            values = {}
            connection = self.__devices[device].get_connection()
            if connection.inWaiting():
                response = connection.read_until(terminator=to_bytes([13, 10]))  # End with CR LF
                values = Response(response[:-2]).decode()

            input[device] = values

        return input
