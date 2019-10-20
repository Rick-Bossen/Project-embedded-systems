from Enums import *


class Device:

    def __init__(self):
        self.__connection = None
        self.__connection = None
        self.__control = Unit.MANUAL
        self.__control_range = {}

    def set_connection(self, connection):
        self.__connection = connection

    def get_connection(self):
        return self.__connection

    def set_control_unit(self, unit):
        self.__control = unit

    def set_control_range(self, min, max, unit=None):
        if unit is None:
            unit = self.__control

        self.__control_range[unit] = (min, max)

    def get_control_range(self, unit=None):
        if unit is None:
            unit = self.__control

        if unit in self.__control_range:
            return self.__control_range[unit]
        else:
            return None
