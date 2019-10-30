from tkinter import *


# TODO add live data and graphs to view
class DataView:
    def __init__(self, parent, sharedvars):
        self.sharedvars = sharedvars
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
        row = 1
        for label in self.sharedvars.data:
            lab = Label(data_frame, text=label + ':')
            lab.grid(row=row, column=0, sticky='nw')
            row += 1

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
