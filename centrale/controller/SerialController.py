from serial import Serial, SerialException


class SerialController:

    def __init__(self, devices):
        self.__devices = devices

    def check_connections(self):
        for device in self.__devices:
            connection = self.__devices[device].get_connection()
            if connection is not None:
                try:
                    connection.read()
                except SerialException:
                    connection = None

            if connection is None:
                connection = Serial(device.get_id(), 19200, stopbits=1, bytesize=8)
                connection.flushInput()
                device.set_connection(connection)

    def output_instruction(self, device, instruction):
        self.__devices[device].get_connection().write(instruction)

    def read_input(self):
        input = {}
        for device in self.__devices:
            connection = self.__devices[device].get_connection()
            input[device] = connection.read_all()
        return input
