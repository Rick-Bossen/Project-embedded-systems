from tkinter import *
from tkinter import ttk

from Enums import Instruction, State
from view.DataView import DataView

import matplotlib
matplotlib.use('TkAgg')


# TODO make use of settings
class Root(Tk):
    def __init__(self, sharedvar, serialcontroller):
        super(Root, self).__init__()
        self.title('Centrale')
        self.minsize(800, 480)
        self.maxsize(900, 480)
        self.sharedvar = sharedvar
        self.devices = []
        self.devicedata = {}

        self.nb = ttk.Notebook(self, name='notebook')
        self.nb.grid(column=0, row=0)
        self.dataview = DataView(self, sharedvar)

        self.data_button = Button(self, text='Data', command=lambda: self.data_button_pressed())
        self.data_button.grid(column=1, row=0, sticky='ne')

        self.serialcontroller = serialcontroller

    # add a tab to the notebook
    def add_tab(self, port, device):
        self.dataview.addunit()
        frame = Frame(self, name=port.lower())
        self.devices.append(device)
        self.devicedata[port] = {}
        self.create_settings_frame(frame, device.tab_settings, port)
        self.create_data_frame(frame, device.tab_data, port)
        self.updatedropdowns()

        self.nb.add(frame, text=port)

    # creates the settings frame within the tab
    def create_settings_frame(self, frame, tab_settings, port):
        settingsframe = Frame(frame, name='settings')
        titlelabel = Label(settingsframe, text='Instellingen')
        titlelabel.grid(row=0, column=0, sticky='nw')

        # creates all setting labels
        row = 1
        for label in tab_settings:
            lab = Label(settingsframe, text=label + ':')
            lab.grid(row=row, column=0, sticky='nw')
            row += 1

        # creates all the setting modifiers
        # TODO create toggle button
        self.devicedata[port]['settings'] = {}
        unit_temp_var = StringVar(settingsframe)
        unit_temp_var.set(port)
        self.devicedata[port]['settings']['unit_temp_var'] = unit_temp_var
        unit_light_var = StringVar(settingsframe)
        unit_light_var.set(port)
        self.devicedata[port]['settings']['unit_light_var'] = unit_light_var

        placeholder_button = Label(settingsframe, text='placeholder')
        placeholder_button.grid(row=1, column=1)

        toggle_temp_var = IntVar()
        toggle_temp_var.set(20)
        toggle_temp = Entry(settingsframe, textvar=toggle_temp_var)
        self.devicedata[port]['settings']['toggle_temp'] = toggle_temp_var
        toggle_temp.grid(row=2, column=1)

        toggle_light_var = IntVar()
        toggle_light_var.set(20)
        toggle_light = Entry(settingsframe, textvar=toggle_light_var)
        self.devicedata[port]['settings']['toggle_light'] = toggle_light_var
        toggle_light.grid(row=3, column=1)

        unit_temp = OptionMenu(settingsframe, unit_temp_var, *self.devicedata)
        self.devicedata[port]['settings']['unit_temp'] = unit_temp
        unit_temp.grid(row=4, column=1)

        unit_light = OptionMenu(settingsframe, unit_light_var, *self.devicedata)
        self.devicedata[port]['settings']['unit_light'] = unit_light
        unit_light.grid(row=5, column=1)

        roll_in_button = Button(settingsframe, text='Inrollen',
            command=lambda: self.serialcontroller.output_instruction(port, Instruction.ROLL.build(State.ROLLED_IN)))
        roll_in_button.grid(row=6, column=0)
        roll_out_button = Button(settingsframe,text='Uitrollen',
            command=lambda: self.serialcontroller.output_instruction(port, Instruction.ROLL.build(State.ROLLED_OUT)))
        roll_out_button.grid(row=6, column=1)

        settingsframe.grid(row=0, column=0, sticky='nw')

    # creates the data frame within the tab
    def create_data_frame(self, frame, tab_data, port):
        # TODO fix spacing issues
        dataframe = Frame(frame, name='data')
        titlelabel = Label(dataframe, text='Data')
        titlelabel.grid(row=0, column=0)

        # creates all data labels
        row = 1
        for label in tab_data:
            lab = Label(dataframe, text=label + ':')
            lab.grid(row=row, column=0, sticky='nw')
            row += 1

        # add all label variables to dictionary
        self.devicedata[port]['state'] = {}
        statevar = StringVar()
        statevar.set('N/A')
        statelab = Label(dataframe, textvar=statevar)
        statelab.grid(row=3, column=1, sticky='nw')
        self.devicedata[port]['state']['name'] = statevar

        self.devicedata[port]['unit'] = {}

        self.devicedata[port]['unit_values'] = {}
        lightvar = IntVar()
        lightlab = Label(dataframe, textvar=lightvar)
        lightlab.grid(row=2, column=1, sticky='nw')
        self.devicedata[port]['unit_values']['light'] = lightvar

        tempvar = IntVar()
        templab = Label(dataframe, textvar=tempvar)
        templab.grid(row=1, column=1, sticky='nw')
        self.devicedata[port]['unit_values']['temperature'] = tempvar
        self.create_graph(dataframe)

        dataframe.grid(row=0, column=1, sticky='nw')

    # creates a graph using the matplotlib package
    def create_graph(self, frame):
        # TODO implement matplotlib graph instead of canvas
        placeholder = Canvas(frame)
        placeholder.create_line(0, 0, 500, 500)
        placeholder.grid(row=1, column=2, sticky='ne')

    # disables a tab
    def disable_tab(self, index):
        self.nb.forget(index)

    def data_button_pressed(self):
        self.dataview.toggle()

    # used to run a function in a specified interval
    def interval(self, speed, function):
        self.after(speed, lambda: [self.interval(speed, function), function()])

    # updates the specified tab with new data
    def updatetab(self, device, data):
        for k, v in data.items():
            for k2, v2 in v.items():
                if k2 in self.devicedata[device][k] and not k2 == 'light' and not k2 == 'temperature':
                    self.devicedata[device][k][k2].set(v2)
                elif k2 == 'light' or k2 == 'temperature':
                    self.devicedata[device][k][k2].set(v2['current'])

    # updates the drop down menu's of all tabs
    def updatedropdowns(self):
        for device in self.devicedata:
            print(device)
            temp = self.devicedata[device]['settings']
            temp['unit_temp']['menu'].delete(0, 'end')
            temp['unit_light']['menu'].delete(0, 'end')
            for port in self.devicedata:
                temp['unit_temp']['menu'].add_command(label=port)
                temp['unit_light']['menu'].add_command(label=port)

    # updates the data view with new data
    def updatedataview(self, data):
        self.dataview.updateData(data)
