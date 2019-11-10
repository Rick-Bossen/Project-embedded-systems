from enum import IntEnum, unique


@unique
class Unit(IntEnum):
    MANUAL = 0
    LIGHT = 1
    TEMPERATURE = 2


@unique
class State(IntEnum):
    ROLLED_IN = 0
    ROLLED_OUT = 1
    ROLLING_OUT = 2
    ROLLING_IN = 3

@unique
class ResponseType(IntEnum):
    STATE_INFO = 1
    UNIT_INFO = 2
    UNIT_VALUE_INFO = 3


@unique
class Instruction(IntEnum):
    SET_UNIT = 1
    ROLL = 2
    SET_UNIT_RANGE = 3

    def build(self, *args):
        output = bytearray()
        output.append(self.value << 4)  # First nibble is the Instruction

        if self is Instruction.SET_UNIT:
            if len(args) is not 1:
                raise ValueError('SET_UNIT can only have 1 argument')

            if args[0] not in Unit:
                raise ValueError('Argument 1 should be instance of Unit')

            output[0] += args[0]

        elif self is Instruction.ROLL:
            if len(args) is not 1:
                raise ValueError('ROLL can only have 1 argument')

            if args[0] not in State:
                raise ValueError('Argument 1 should be instance of State')

            output[0] += args[0]

        elif self is Instruction.SET_UNIT_RANGE:
            if len(args) is not 3:
                raise ValueError('SET_UNIT_RANGE can only have 3 arguments')

            if args[0] not in Unit:
                raise ValueError('Argument 1 should be instance of Unit')
            output[0] += args[0]

            if (args[1] < 0) | (args[1] > 0xFF):
                raise ValueError('Argument 2 Should be between 0 and 255')

            if (args[2] < 0) | (args[2] > 0xFF):
                raise ValueError('Argument 3 Should be between 0 and 255')

            output.append(args[1])
            output.append(args[2])

        return output
