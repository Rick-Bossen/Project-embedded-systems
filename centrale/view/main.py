from tkinter import *
from tkinter import ttk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from centrale.view.label_tups import tab_settings, tab_data



class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title('Centrale')
        self.minsize(800, 480)
        self.maxsize(800, 480)

        self.nb = ttk.Notebook(self)

    # add a tab to the notebook
    def add_tab(self):
        frame = Frame(self)
        self.create_settings_frame(frame)
        self.create_data_frame(frame)

        self.nb.add(frame, text='test')
        self.nb.update()
        self.nb.grid(column=0, row=0)

    # creates the settings frame within the tab
    def create_settings_frame(self, frame):
        settingsframe = Frame(frame)
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
        # TODO fill default states using sensor input
        # TODO fill dropdown with available units
        temp = ('temp1', 'temp2', 'temp3')
        unit_temp_var = StringVar(settingsframe)
        unit_light_var = StringVar(settingsframe)

        placeholder_button = Label(settingsframe, text='placeholder')
        placeholder_button.grid(row=1, column=1)
        toggle_temp = Entry(settingsframe)
        toggle_temp.grid(row=2, column=1)
        toggle_light = Entry(settingsframe)
        toggle_light.grid(row=3, column=1)
        unit_temp = OptionMenu(settingsframe, unit_temp_var, *temp)
        unit_temp.grid(row=4, column=1)
        unit_light = OptionMenu(settingsframe, unit_light_var, *temp)
        unit_light.grid(row=5, column=1)

        settingsframe.grid(row=0, column=0, sticky='nw')

    # creates the data frame within the tab
    def create_data_frame(self, frame):
        # TODO fill in data using units
        # TODO fix spacing issues
        dataframe = Frame(frame)
        titlelabel = Label(dataframe, text='Data')
        titlelabel.grid(row=0, column=0)

        # creates all data labels
        row = 1
        for label in tab_data:
            lab = Label(dataframe, text=label + ':')
            lab.grid(row=row, column=0, sticky='nw')
            row += 1

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

# creates a new frame if this file is run, mainly for testing purposes
if __name__ == '__main__':
    root = Root()
    root.add_tab()
    root.add_tab()
    root.add_tab()
    root.add_tab()
    root.add_tab()
    root.add_tab()
    root.mainloop()
