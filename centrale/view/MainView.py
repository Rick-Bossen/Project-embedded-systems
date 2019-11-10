from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style

from Enums import Instruction, State
from view.DataView import DataView

# TODO make use of settings
from view.Graph import Graph


class Root(Tk):
    def __init__(self, sharedvar, serialcontroller):
        super(Root, self).__init__()
        self.title('Besturingscentrale')
        self.minsize(900, 480)
        self.maxsize(900, 480)
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth() / 2-450), int(self.winfo_screenheight() / 2-240)))

        # Initialize data variables
        self.serialcontroller = serialcontroller
        self.sharedvar = sharedvar
        self.devices = []
        self.devicedata = {}

        # Initialize Root element grid size
        self.grid_columnconfigure(0, minsize=800, weight=1)
        self.grid_columnconfigure(1, minsize=100, weight=1)

        self.nb = ttk.Notebook(self, name='notebook', height=440)
        self.data_button = Button(self, text='Data', background='#EF5B5B', foreground='white', font='Roboto 11',
                                  width=70, command=lambda: self.data_button_pressed())
        self.dataview = DataView(self, sharedvar)

        # Styling
        self.configure(background='#2F4F4F')
        self.iconbitmap(r'resources/sun.ico')

        style = Style()
        style.theme_create('notebook', settings={
            "TNotebook": {"configure": {"background": "#2F4F4F"}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": "#AEC3B0", 'foreground': '#fff'},
                "map": {"background": [("selected", "#598392")], "foreground": [("selected", "#fff"), ("active", "#EF5B5B")]}
            }
        })
        style.theme_use('notebook')
        self.loader = Canvas(self, width=900, height=480, highlightthickness=0, background='#2F4F4F')
        self.loader.grid(column=0, row=0, columnspan=2)
        self.loading(1)

    # Remove loading
    def loading(self, stage):
        self.loader.delete('all')
        self.loader.create_text(450 - 10, 220, font='Roboto', text='Wachten op connecties' + ('.'*stage), fill='white')

        if len(self.devices) == 0:
            stage += 1
            if stage > 3:
                stage = 1
            self.after(1000, lambda: self.loading(stage))
        else:
            self.loader.destroy()
            self.nb.grid(column=0, row=0, padx=(10, 0), pady=(10, 10))
            self.data_button.grid(column=1, row=0, sticky='ne', padx=(10, 10), pady=(30, 10))

    # add a tab to the notebook
    def add_tab(self, port, device):
        self.dataview.addunit()
        frame = Frame(self, name=port.lower(), background='#598392')
        self.devices.append(device)
        self.devicedata[port] = {}
        self.create_settings_frame(frame, device.tab_settings, port)
        self.create_data_frame(frame, device.tab_data, port)
        self.updatedropdowns()

        self.nb.add(frame, text=port)

    # creates the settings frame within the tab
    def create_settings_frame(self, frame, tab_settings, port):
        settingsframe = Frame(frame, name='settings', background='#598392')
        titlelabel = Label(settingsframe, text='Instellingen', background='#598392', foreground='white', font='Roboto 14')
        titlelabel.grid(row=0, column=0, rowspan=2, sticky='nw', padx=10, pady=10)

        # Configure grid sizes
        for i in range(0, 13):
            settingsframe.grid_rowconfigure(i, minsize=34)
        for i in range(0, 2):
            settingsframe.grid_columnconfigure(i, minsize=195)

        # creates all setting labels
        row = 2
        for label in tab_settings:
            lab = Label(settingsframe, text=label + ':', background='#598392', foreground='white', font='Roboto 11')
            lab.grid(row=row, column=0, sticky='nw', padx=10)
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
        placeholder_button.grid(row=2, column=1)

        toggle_temp_var = IntVar()
        toggle_temp_var.set(20)
        toggle_temp = Entry(settingsframe, textvar=toggle_temp_var)
        self.devicedata[port]['settings']['toggle_temp'] = toggle_temp_var
        toggle_temp.grid(row=3, column=1)

        toggle_light_var = IntVar()
        toggle_light_var.set(20)
        toggle_light = Entry(settingsframe, textvar=toggle_light_var)
        self.devicedata[port]['settings']['toggle_light'] = toggle_light_var
        toggle_light.grid(row=4, column=1)

        unit_temp = OptionMenu(settingsframe, unit_temp_var, *self.devicedata)
        self.devicedata[port]['settings']['unit_temp'] = unit_temp
        unit_temp.grid(row=5, column=1)

        unit_light = OptionMenu(settingsframe, unit_light_var, *self.devicedata)
        self.devicedata[port]['settings']['unit_light'] = unit_light
        unit_light.grid(row=6, column=1)

        roll_in_button = Button(settingsframe,
            text='Inrollen', background='#EF5B5B', foreground='white', font='Roboto 11', width=20,
            command=lambda: self.serialcontroller.output_instruction(port, Instruction.ROLL.build(State.ROLLED_IN)))
        roll_in_button.grid(row=8, column=0)
        roll_out_button = Button(settingsframe,
            text='Uitrollen', background='#EF5B5B', foreground='white', font='Roboto 11', width=20,
            command=lambda: self.serialcontroller.output_instruction(port, Instruction.ROLL.build(State.ROLLED_OUT)))
        roll_out_button.grid(row=8, column=1)
        # TODO make auto button switch unit to auto
        roll_auto_button = Button(settingsframe,
            text='Auto', background='#EF5B5B', foreground='white', font='Roboto 11', width=42,
            command=lambda: self.serialcontroller.output_instruction(port, Instruction.ROLL.build(State.ROLLED_IN)))
        roll_auto_button.grid(row=9, column=0, columnspan=2)

        settingsframe.grid(row=0, column=0, sticky='nw')

    # creates the data frame within the tab
    def create_data_frame(self, frame, tab_data, port):
        dataframe = Frame(frame, name='data', width=390, background='#598392')
        titlelabel = Label(dataframe, text='Data', background='#598392', foreground='white', font='Roboto 14')
        titlelabel.grid(row=0, column=0, rowspan=2, sticky='nw', padx=10, pady=10)

        # Configure grid sizes
        for i in range(0, 13):
            dataframe.grid_rowconfigure(i, minsize=34)
        for i in range(0, 2):
            dataframe.grid_columnconfigure(i, minsize=195)

        # creates all data labels
        row = 2
        for label in tab_data:
            lab = Label(dataframe, text=label + ':', background='#598392', foreground='white', font='Roboto 11')
            lab.grid(row=row, column=0, sticky='nw', padx=10)
            row += 1

        unitvar = StringVar()
        unitvar.set('-')
        unitlab = Label(dataframe, textvar=unitvar, background='#598392', foreground='white', font='Roboto 11')
        unitlab.grid(row=2, column=1, sticky='nw')
        self.devicedata[port]['unit'] = {'name': unitvar}

        self.devicedata[port]['unit_values'] = {}

        tempvar = IntVar()
        templab = Label(dataframe, textvar=tempvar, background='#598392', foreground='white', font='Roboto 11')
        tempvar.trace('w', lambda *args: self.show_not_empty(tempvar, templab))
        self.devicedata[port]['unit_values']['temperature'] = tempvar

        lightvar = IntVar()
        lightlab = Label(dataframe, textvar=lightvar, background='#598392', foreground='white', font='Roboto 11')
        lightvar.trace('w', lambda *args: self.show_not_empty(lightvar, lightlab))

        self.devicedata[port]['unit_values']['light'] = lightvar

        # add all label variables to dictionary
        self.devicedata[port]['state'] = {}
        statevar = StringVar()
        statevar.set('-')
        statelab = Label(dataframe, textvar=statevar, background='#598392', foreground='white', font='Roboto 11')
        statelab.grid(row=4, column=1, sticky='nw')
        self.devicedata[port]['state']['name'] = statevar

        self.create_graph(dataframe, port)

        dataframe.grid(row=0, column=1, sticky='nw')

    def show_not_empty(self, var, label):
        if var.get() > 0 and not label.winfo_viewable():
            label.grid(row=3, column=1, sticky='nw')

    # creates a graph using the matplotlib package
    def create_graph(self, frame, port):
        graph = Graph(frame, (3, 2), )
        self.devicedata[port]['graph'] = graph

        canvas = graph.getCanvas()
        canvas._tkcanvas.grid(row=5, column=0, rowspan=8, columnspan=2, sticky='nw', padx=10, pady=10)

    def updategraph(self, port, data):
        self.devicedata[port]['graph'].iterate(data)

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
                    self.updategraph(device, v2['current'])
                    self.devicedata[device]['graph'].updateline('Rol in', v2['close_at'])
                    self.devicedata[device]['graph'].updateline('Rol uit', v2['open_at'])

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
