from _tkinter import TclError

from Enums import Instruction, Unit, State

# class that represents the controller for the main and data view
class ViewController:

    def __init__(self, serial_controller):
        self.window = None
        self.serial_controller = serial_controller

    # checks for new devices
    def check_devices(self):
        devices = self.serial_controller.find_devices()
        for device in devices:
            try:
                self.window.nametowidget(device.lower())
            except KeyError:
                self.window.add_tab(device, devices[device])
        self.serial_controller.check_connections()

    # updates the view with new data
    def update_view(self):
        self.serial_controller.check_connections()
        input = self.serial_controller.read_input()
        for device in input:
            if input[device]:
                print(input[device])
                self.window.updatetab(device, input[device])
        self.window.dataview.updateData(input)

    # toggles the visibility of the data view
    def data_button_pressed(self):
        self.window.dataview.toggle()

    # saves the settings in the entry fields to the device
    def save_settings_button_pressed(self, device):
        try:
            roll_in = self.window.devicedata[device]['settings']['roll_in'].get()
            roll_out = self.window.devicedata[device]['settings']['roll_out'].get()
        except TclError:
            return

        if self.window.devicedata[device]['type'] == 'light':
            instruction = Instruction.SET_UNIT_RANGE.build(Unit.LIGHT, roll_out, roll_in)
            self.serial_controller.output_instruction(device, instruction)
        elif self.window.devicedata[device]['type'] == 'temperature':
            instruction = Instruction.SET_UNIT_RANGE.build(Unit.TEMPERATURE, roll_out, roll_in)
            self.serial_controller.output_instruction(device, instruction)

    # makes the specified device roll in
    def roll_in_button_pressed(self, device):
        self.serial_controller.output_instruction(device, Instruction.ROLL.build(State.ROLLED_IN))

    # makes the specified device roll out
    def roll_out_button_pressed(self, device):
        self.serial_controller.output_instruction(device, Instruction.ROLL.build(State.ROLLED_OUT))

    # makes the specified device roll in or out automatically
    def roll_auto_button_pressed(self, device, unit):
        self.serial_controller.output_instruction(device, Instruction.SET_UNIT.build(unit))
