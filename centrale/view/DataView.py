from tkinter import *
import time
import datetime


# TODO add live data and graphs to view
class DataView:
    def __init__(self, parent, sharedvars):
        self.sharedvars = sharedvars
        self.data = {}
        self.starttime = time.time()
        self.top = Toplevel(parent)
        self.create_main_frame(self.top)

        self.top.withdraw()
        self.visible = 0

        self.top.protocol("WM_DELETE_WINDOW", lambda: self.toggle())

    # creates the main frame in which all the data will be displayed
    def create_main_frame(self, frame):
        frame = Frame(frame)
        titlelabel = Label(frame, text='Data')
        titlelabel.grid(row=0, column=0)
        self.create_statistics_frame(frame)

        frame.grid(row=0, column=0)

    # creates the frame within the main frame that contains all the numeric data
    def create_statistics_frame(self, frame):
        data_frame = Frame(frame)

        # creates all the labels
        row = 1
        for label in self.sharedvars.data:
            lab = Label(data_frame, text=label + ':')
            lab.grid(row=row, column=0, sticky='nw')
            row += 1

        # creates all the variable labels and variables
        maxtempvar = IntVar()
        maxtemplab = Label(data_frame, textvar=maxtempvar)
        maxtemplab.grid(row=1, column=1, sticky='nw')
        self.data['maxtemp'] = maxtempvar

        mintempvar = IntVar()
        mintemplab = Label(data_frame, textvar=mintempvar)
        mintemplab.grid(row=2, column=1, sticky='nw')
        self.data['mintemp'] = mintempvar

        avgtempvar = IntVar()
        avgtemplab = Label(data_frame, textvar=avgtempvar)
        avgtemplab.grid(row=3, column=1, sticky='nw')
        self.data['avgtemp'] = avgtempvar

        maxlightvar = IntVar()
        maxlightlab = Label(data_frame, textvar=maxlightvar)
        maxlightlab.grid(row=4, column=1, sticky='nw')
        self.data['maxlight'] = maxlightvar

        minlightvar = IntVar()
        minlightlab = Label(data_frame, textvar=minlightvar)
        minlightlab.grid(row=5, column=1, sticky='nw')
        self.data['minlight'] = minlightvar

        avglightvar = IntVar()
        avglightlab = Label(data_frame, textvar=avglightvar)
        avglightlab.grid(row=6, column=1, sticky='nw')
        self.data['avglight'] = avglightvar

        unitsvar = IntVar()
        unitslab = Label(data_frame, textvar=unitsvar)
        unitslab.grid(row=7, column=1, sticky='nw')
        self.data['units'] = unitsvar

        tempunitsvar = IntVar()
        tempunitslab = Label(data_frame, textvar=tempunitsvar)
        tempunitslab.grid(row=8, column=1, sticky='nw')
        self.data['tempunits'] = tempunitsvar

        lightunitsvar = IntVar()
        lightunitslab = Label(data_frame, textvar=lightunitsvar)
        lightunitslab.grid(row=9, column=1, sticky='nw')
        self.data['lightunits'] = lightunitsvar

        uptimevar = StringVar()
        uptimelab = Label(data_frame, textvar=uptimevar)
        uptimelab.grid(row=10, column=1, sticky='nw')
        self.data['uptime']= uptimevar

        data_frame.grid(row=1, column=0, rowspan=2)

    # TODO add graphs to frame
    def create_graph_frame(self):
        pass

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
        for device in data:
            if data[device]:
                units += 1
                temp = data[device]
                if 'unit' in temp:
                    unit = temp['unit']
                    if not unit['name'] == 'MANUAL':
                        unit_values = temp['unit_values'][unit['name'].lower()]
                        if unit['name'] == 'LIGHT':
                            lightunits += 1
                            if self.data['maxlight'].get() < unit_values['current']:
                                self.data['maxlight'].set(unit_values['current'])
                            if self.data['minlight'].get() > unit_values['current']:
                                self.data['minlight'].set(unit_values['current'])
                        elif unit['name'] == 'TEMPERATURE':
                            tempunits += 1
                            if self.data['maxtemp'].get() < unit_values['current']:
                                self.data['maxtemp'].set(unit_values['current'])
                            if self.data['mintemp'].get() > unit_values['current']:
                                self.data['mintemp'].set(unit_values['current'])

        uptime = datetime.timedelta(seconds=time.time() - self.starttime)
        uptime = uptime - datetime.timedelta(microseconds=uptime.microseconds)
        self.data['uptime'].set(str(uptime))

        self.data['units'].set(units)
        self.data['lightunits'].set(lightunits)
        self.data['tempunits'].set(tempunits)
