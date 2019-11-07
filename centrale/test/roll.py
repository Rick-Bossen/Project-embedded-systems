import time

from Enums import State, Instruction
from controller.SerialController import SerialController

controller = SerialController()
devices = controller.find_devices()
controller.check_connections()

time.sleep(6)

while True:
    input = controller.read_input()
    for device in input:
        if 'state' in input[device].keys():
            state = input[device]['state']['value']
            if state == State.ROLLED_IN.value:
                controller.output_instruction(device, Instruction.ROLL.build(State.ROLLING_OUT))
            elif state == State.ROLLED_OUT.value:
                controller.output_instruction(device, Instruction.ROLL.build(State.ROLLED_IN))

    time.sleep(6)
