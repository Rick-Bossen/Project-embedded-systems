from tkinter import *
import time
import datetime

from view.Theme import *
from view.Graph import Graph


class DataView:
    labels = ('Hoogste temperatuur', 'Laagste temperatuur', 'Gemiddelde temperatuur', 'Hoogste lichtintensiteit',
                 'Laagste lichtintensiteit', 'Gemiddelde lichtintensiteit', 'Aantal units',
              'Aantal temperatuursensoren', 'Aantal lichtsensoren', 'Uptime')

    def __init__(self, parent):
        self.data = {}
        self.starttime = time.time()
        self.top = Toplevel(parent, background=Theme.FRAME_COLOR)
        self.top.minsize(600, 480)
        self.top.maxsize(600, 480)
        self.create_main_frame(self.top)
        self.firsttimelight = 1
        self.firsttimetemp = 1

        self.top.withdraw()
        self.visible = 0

        self.top.protocol("WM_DELETE_WINDOW", lambda: self.toggle())

    # creates the main frame in which all the data will be displayed
    def create_main_frame(self, frame):
        frame = Frame(frame, background=Theme.FRAME_COLOR)
        titlelabel = Label(frame, text='Data', **Theme.LABEL_HEADER)
        titlelabel.grid(row=0, column=0)
        self.create_statistics_frame(frame)
        self.create_graph_frame(frame)

        frame.grid(row=0, column=0)

    # creates the frame within the main frame that contains all the numeric data
    def create_statistics_frame(self, frame):
        data_frame = Frame(frame, background=Theme.FRAME_COLOR)
        data_frame.grid_columnconfigure(1, minsize=50)

        # creates all the labels
        row = 1
        for label in self.labels:
            lab = Label(data_frame, text=label + ':', **Theme.LABEL)
            lab.grid(row=row, column=0, sticky='nw')
            row += 1

        # creates all the variable labels and variables
        maxtempvar = IntVar()
        maxtemplab = Label(data_frame, textvar=maxtempvar, **Theme.LABEL)
        maxtemplab.grid(row=1, column=1, sticky='nw')
        self.data['maxtemp'] = maxtempvar

        mintempvar = IntVar()
        mintemplab = Label(data_frame, textvar=mintempvar, **Theme.LABEL)
        mintemplab.grid(row=2, column=1, sticky='nw')
        self.data['mintemp'] = mintempvar

        avgtempvar = IntVar()
        avgtemplab = Label(data_frame, textvar=avgtempvar, **Theme.LABEL)
        avgtemplab.grid(row=3, column=1, sticky='nw')
        self.data['avgtemp'] = avgtempvar

        maxlightvar = IntVar()
        maxlightlab = Label(data_frame, textvar=maxlightvar, **Theme.LABEL)
        maxlightlab.grid(row=4, column=1, sticky='nw')
        self.data['maxlight'] = maxlightvar

        minlightvar = IntVar()
        minlightlab = Label(data_frame, textvar=minlightvar, **Theme.LABEL)
        minlightlab.grid(row=5, column=1, sticky='nw')
        self.data['minlight'] = minlightvar

        avglightvar = IntVar()
        avglightlab = Label(data_frame, textvar=avglightvar, **Theme.LABEL)
        avglightlab.grid(row=6, column=1, sticky='nw')
        self.data['avglight'] = avglightvar

        unitsvar = IntVar()
        unitslab = Label(data_frame, textvar=unitsvar, **Theme.LABEL)
        unitslab.grid(row=7, column=1, sticky='nw')
        self.data['units'] = unitsvar

        tempunitsvar = IntVar()
        tempunitslab = Label(data_frame, textvar=tempunitsvar, **Theme.LABEL)
        tempunitslab.grid(row=8, column=1, sticky='nw')
        self.data['tempunits'] = tempunitsvar

        lightunitsvar = IntVar()
        lightunitslab = Label(data_frame, textvar=lightunitsvar, **Theme.LABEL)
        lightunitslab.grid(row=9, column=1, sticky='nw')
        self.data['lightunits'] = lightunitsvar

        uptimevar = StringVar()
        uptimelab = Label(data_frame, textvar=uptimevar, **Theme.LABEL)
        uptimelab.grid(row=10, column=1, sticky='nw')
        self.data['uptime']= uptimevar

        data_frame.grid(row=1, column=0, rowspan=2)

    def create_graph_frame(self, frame):
        graph_frame = Frame(frame)

        tempgraph = Graph(graph_frame, (4, 3), 'Gemiddelde temperatuur')
        self.data['tempgraph'] = tempgraph
        tempcanvas = tempgraph.getCanvas()
        tempcanvas._tkcanvas.grid(row=0, column=0)

        lightgraph = Graph(graph_frame, (4, 3), 'Gemiddelde lichtintensiteit')
        self.data['lightgraph'] = lightgraph
        lightcanvas = lightgraph.getCanvas()
        lightcanvas._tkcanvas.grid(row=1, column=0)

        graph_frame.grid(row=1, column=3)

    # toggles the visibility of the data window
    def toggle(self):
        if self.visible == 1:
            self.top.withdraw()
            self.visible = 0
        else:
            self.top.deiconify()
            self.visible = 1

    # increments the total connected units
    def addunit(self):
        self.data['units'].set(self.data['units'].get() + 1)

    # updates the data
    def updateData(self, data):
        units = 0
        lightunits = 0
        tempunits = 0
        lightvals = []
        tempvals = []
        for device in data:
            if data[device]:
                units += 1
                temp = data[device]
                if 'unit' in temp:
                    unit = temp['unit']
                    if not unit['name'] == 'MANUAL':
                        unit_values = temp['unit_values'][unit['name'].lower()]
                        current = unit_values['current']
                        if unit['name'] == 'LIGHT':
                            lightunits += 1
                            if self.data['maxlight'].get() < current:
                                self.data['maxlight'].set(current)
                                self.data['lightgraph'].updateline('Hoogste lichtintensiteit', current)
                            if self.data['minlight'].get() > current:
                                self.data['minlight'].set(current)
                                self.data['lightgraph'].updateline('Laagste lichtintensiteit', current)
                            lightvals.append(current)
                            self.firsttimeset('light', current)
                        elif unit['name'] == 'TEMPERATURE':
                            tempunits += 1
                            if self.data['maxtemp'].get() < current < 100:
                                self.data['maxtemp'].set(current)
                                self.data['tempgraph'].updateline('Hoogste temperatuur', current)
                            if self.data['mintemp'].get() > current:
                                self.data['mintemp'].set(current)
                                self.data['tempgraph'].updateline('Laagste temperatuur', current)
                            tempvals.append(current)
                            self.firsttimeset('temperature', current)
        if tempvals:
            avgtemp = round(sum(tempvals) / len(tempvals), 2)
            if avgtemp < 100:
                self.data['avgtemp'].set(avgtemp)
                self.data['tempgraph'].iterate(avgtemp)

        if lightvals:
            avglight = round(sum(lightvals) / len(lightvals), 2)
            self.data['avglight'].set(avglight)
            self.data['lightgraph'].iterate(avglight)
        uptime = datetime.timedelta(seconds=time.time() - self.starttime)
        uptime = uptime - datetime.timedelta(microseconds=uptime.microseconds)
        self.data['uptime'].set(str(uptime))

        self.data['units'].set(units)
        self.data['lightunits'].set(lightunits)
        self.data['tempunits'].set(tempunits)

    def updategraphs(self):
        pass

    # sets the min values with the first given values instead of 0
    def firsttimeset(self, type, value):
        if type == 'light':
            if self.firsttimelight:
                self.firsttimelight = 0
                self.data['minlight'].set(value)
        elif type == 'temperature':
            if self.firsttimetemp:
                self.firsttimetemp = 0
                self.data['mintemp'].set(value)
