from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style

from Enums import Instruction, State, Unit
from view.Theme import *
from view.DataView import DataView
from view.Graph import Graph
from controller.ViewController import *


# class that represents the main window
class Root(Tk):

    tab_settings = ('Uitrol waarde ', 'Inrol waarde ',)
    tab_data = ('Eenheid', 'Waarde', 'Status')
    unit_names = {Unit.MANUAL.name: 'Handmatig', Unit.LIGHT.value: 'Licht', Unit.TEMPERATURE.name: 'Temperatuur'}
    state_names = {State.ROLLED_IN.name: 'Ingerold', State.ROLLING_OUT.name: 'Uitrollen',
                   State.ROLLED_OUT.name: 'Uitgerold', State.ROLLING_IN.name: 'Inrollen'}

    def __init__(self, view_controller):
        super(Root, self).__init__()
        self.devices = []
        self.devicedata = {}
        self.view_controller = view_controller

        self.title('Besturingscentrale')
        self.minsize(*Theme.SIZE)
        self.maxsize(*Theme.SIZE)
        self.geometry("+{}+{}".format(
            int(self.winfo_screenwidth() / 2 - Theme.WIDTH / 2),
            int(self.winfo_screenheight() / 2 - Theme.HEIGHT / 2))
        )

        # Initialize Root element grid size
        self.grid_columnconfigure(0, minsize=Theme.TK_NB_WIDTH, weight=1)
        self.grid_columnconfigure(1, minsize=Theme.TK_DATA_BUTTON_WIDTH, weight=1)

        self.nb = ttk.Notebook(self, name='notebook', height=Theme.HEIGHT - Theme.PADDING * 4)
        self.data_button = Button(self, text='Data', width=70, command=self.view_controller.data_button_pressed,
                                  **Theme.BUTTON)
        self.roll_auto_button = None
        self.dataview = DataView(self)

        # Styling
        self.configure(background=Theme.BACKGROUND_COLOR)
        self.iconbitmap(Theme.R_ICO)
        Theme.init()
        # Initialize loading animation
        self.loading_text()

    # used to run a function in a specified interval
    def interval(self, speed, function):
        self.after(speed, lambda: [self.interval(speed, function), function()])

    # Remove loading
    def loading_text(self, stage=1, loader=None):
        if loader is None:
            loader = Canvas(self, width=Theme.WIDTH, height=Theme.HEIGHT, highlightthickness=0,
                            background=Theme.BACKGROUND_COLOR)
            loader.grid(column=0, row=0, columnspan=2)

        loader.delete('all')
        loader.create_text(450 - 10, 220, font=Theme.FONT_FAMILY, text='Wachten op connecties' + ('.'*stage),
                           fill=Theme.FONT_COLOR)

        if len(self.devices) == 0:
            stage += 1
            if stage > 3:
                stage = 1
            self.after(1000, lambda: self.loading_text(stage, loader))
        else:
            loader.destroy()
            self.nb.grid(column=0, row=0, padx=(Theme.PADDING, 0), pady=Theme.PADDING)
            self.data_button.grid(column=1, row=0, sticky='ne', padx=Theme.PADDING,
                                  pady=(Theme.PADDING * 3, Theme.PADDING))

    # add a tab to the notebook
    def add_tab(self, port, device):
        self.dataview.addunit()
        frame = Frame(self, name=port.lower(), background='#598392')
        self.devices.append(device)
        self.devicedata[port] = {}
        self.create_settings_frame(frame, port)
        self.create_data_frame(frame, port)

        self.nb.add(frame, text=port)

    # creates the settings frame within the tab
    def create_settings_frame(self, frame, port):
        settingsframe = Frame(frame, name='settings', background=Theme.FRAME_COLOR)
        titlelabel = Label(settingsframe, text='Instellingen', **Theme.LABEL_HEADER)
        titlelabel.grid(row=0, column=0, rowspan=2, sticky='nw', padx=Theme.PADDING, pady=Theme.PADDING)

        # Configure grid sizes
        for i in range(0, 13):
            settingsframe.grid_rowconfigure(i, minsize=Theme.ROW_HEIGHT)
        for i in range(0, 2):
            settingsframe.grid_columnconfigure(i, minsize=Theme.COLUMN_WIDTH)

        # creates all setting labels
        row = 2
        for label in self.tab_settings:
            lab = Label(settingsframe, text=label + ':', **Theme.LABEL)
            lab.grid(row=row, column=0, sticky='nw', padx=Theme.PADDING)
            row += 1

        # creates all the setting modifiers
        self.devicedata[port]['settings'] = {}

        roll_out_var = IntVar(settingsframe)
        roll_out = Entry(settingsframe, textvar=roll_out_var, font=Theme.FONT)
        self.devicedata[port]['settings']['roll_out'] = roll_out_var
        roll_out.grid(row=2, column=1)

        roll_in_var = IntVar(settingsframe)
        roll_in = Entry(settingsframe, textvar=roll_in_var, font=Theme.FONT)
        self.devicedata[port]['settings']['roll_in'] = roll_in_var
        roll_in.grid(row=3, column=1)

        save_settings_button = Button(settingsframe, text='Opslaan', width=20, **Theme.BUTTON,
                                      command=lambda: self.view_controller.save_settings_button_pressed(port))
        save_settings_button.grid(row=4, column=1)

        roll_in_button = Button(settingsframe, text='Inrollen',  width=20, **Theme.BUTTON,
                                command=lambda: self.view_controller.roll_in_button_pressed(port))
        roll_in_button.grid(row=6, column=0)
        roll_out_button = Button(settingsframe, text='Uitrollen', width=20, **Theme.BUTTON,
                                 command=lambda: self.view_controller.roll_out_button_pressed(port))
        roll_out_button.grid(row=6, column=1)

        self.roll_auto_button = Button(settingsframe, text='Auto', width=45, **Theme.BUTTON)
        self.devicedata[port]['settings']['auto'] = self.roll_auto_button

        settingsframe.grid(row=0, column=0, sticky='nw')

    # creates the data frame within the tab
    def create_data_frame(self, frame, port):
        dataframe = Frame(frame, name='data', width=390, background=Theme.FRAME_COLOR)
        titlelabel = Label(dataframe, text='Data', **Theme.LABEL_HEADER)
        titlelabel.grid(row=0, column=0, rowspan=2, sticky='nw', padx=Theme.PADDING, pady=Theme.PADDING)

        # Configure grid sizes
        for i in range(0, 13):
            dataframe.grid_rowconfigure(i, minsize=Theme.ROW_HEIGHT)
        for i in range(0, 2):
            dataframe.grid_columnconfigure(i, minsize=Theme.COLUMN_WIDTH)

        # creates all data labels
        row = 2
        for label in self.tab_data:
            lab = Label(dataframe, text=label + ':', **Theme.LABEL)
            lab.grid(row=row, column=0, sticky='nw', padx=10)
            row += 1

        unitvar = StringVar()
        unitvar.set('-')
        unitlab = Label(dataframe, textvar=unitvar, **Theme.LABEL)
        unitlab.grid(row=2, column=1, sticky='nw')
        self.devicedata[port]['unit'] = {'name': unitvar}

        self.devicedata[port]['unit_values'] = {}

        tempvar = IntVar()
        templab = Label(dataframe, textvar=tempvar, **Theme.LABEL)
        tempvar.trace('w', lambda *args: self.show_not_empty(tempvar, templab))
        self.devicedata[port]['unit_values']['temperature'] = tempvar

        lightvar = IntVar()
        lightlab = Label(dataframe, textvar=lightvar, **Theme.LABEL)
        lightvar.trace('w', lambda *args: self.show_not_empty(lightvar, lightlab))

        self.devicedata[port]['unit_values']['light'] = lightvar

        # add all label variables to dictionary
        self.devicedata[port]['state'] = {}
        statevar = StringVar()
        statevar.set('-')
        statelab = Label(dataframe, textvar=statevar, **Theme.LABEL)
        statelab.grid(row=4, column=1, sticky='nw')
        self.devicedata[port]['state']['name'] = statevar

        self.create_graph(dataframe, port)

        dataframe.grid(row=0, column=1, sticky='nw')

    # creates a graph using the Graph class
    def create_graph(self, frame, port):
        graph = Graph(frame, (4, 3))
        self.devicedata[port]['graph'] = graph

        canvas = graph.get_canvas()
        canvas._tkcanvas.grid(row=5, column=0, rowspan=8, columnspan=2, sticky='nw', padx=10, pady=10)

    # updates a graph with new data
    def updategraph(self, port, data):
        self.devicedata[port]['graph'].iterate(data)

    # updates the specified tab with new data
    def updatetab(self, device, data):
        for k, v in data.items():
            for k2, v2 in v.items():
                if k2 in self.devicedata[device][k] and not k2 == 'light' and not k2 == 'temperature':
                    if k == 'unit' and k2 == 'name':
                        if v2 == Unit.MANUAL.name:
                            v2 = self.unit_names[v2]
                            if not self.roll_auto_button.winfo_viewable():
                                self.roll_auto_button.grid(row=7, column=0, columnspan=2)
                        else:
                            if v2 == Unit.LIGHT.name:
                                v2 = 'Licht'
                            elif v2 == Unit.TEMPERATURE.name:
                                v2 = 'Temperatuur'
                            if self.roll_auto_button.winfo_viewable():
                                self.roll_auto_button.grid_forget()
                    elif k == 'state' and k2 == 'name':
                        v2 = self.state_names[v2]

                    self.devicedata[device][k][k2].set(v2)
                elif k2 == 'light' or k2 == 'temperature':
                    if 'type' not in self.devicedata[device]:
                        self.devicedata[device]['settings']['roll_in'].set(v2['close_at'])
                        self.devicedata[device]['settings']['roll_out'].set(v2['open_at'])

                    self.devicedata[device]['type'] = k2

                    # set action of auto button
                    if k2 == 'light':
                        self.devicedata[device]['settings']['auto']['command'] = \
                            lambda: self.view_controller.roll_auto_button_pressed(device, Unit.LIGHT)
                    else:
                        self.devicedata[device]['settings']['auto']['command'] = \
                            lambda: self.view_controller.roll_auto_button_pressed(device, Unit.TEMPERATURE)

                    # check if temperature is a normal reading
                    if v2['current'] < 100 or k2 == 'light':
                        self.devicedata[device][k][k2].set(v2['current'])
                        self.updategraph(device, v2['current'])
                        self.devicedata[device]['graph'].updateline('Rol in', v2['close_at'])
                        self.devicedata[device]['graph'].updateline('Rol uit', v2['open_at'])

    def show_not_empty(self, var, label):
        if var.get() > 0 and not label.winfo_viewable():
            label.grid(row=3, column=1, sticky='nw')
