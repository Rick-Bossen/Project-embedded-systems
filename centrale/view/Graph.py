from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from itertools import count

from view.Theme import *


class Graph:
    def __init__(self, master, size, title=""):
        self.title = title
        plt.style.use('seaborn')
        ax = plt.figure().gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        self.fig = plt.Figure(figsize=size, dpi=80)
        self.fig.set_facecolor(Theme.FRAME_COLOR)
        self.plot = self.fig.add_subplot(111)
        self.plot.set_title(title, color=Theme.FONT_COLOR)
        self.plot.tick_params(colors=Theme.FONT_COLOR)
        self.x_values = []
        self.y_values = []
        self.lines = {}

        self.index = count()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

    # adds new value to graph
    def iterate(self, data):
        self.x_values.append(next(self.index))
        self.y_values.append(data)
        if len(self.x_values) > 10:
            self.x_values.pop(0)
            self.y_values.pop(0)

        self.plot.cla()
        self.plot.set_title(self.title, color=Theme.FONT_COLOR)
        self.plot.plot(self.x_values, self.y_values, marker='o', color=Theme.HIGHLIGHT_COLOR)

        # adds static lines with different colors
        if self.lines:
            colors = ('rgcmykb')
            i = 0
            for k, v in self.lines.items():
                self.plot.axhline(y=v, linestyle='--', label=k, color=colors[i])
                self.plot.legend()
                i += 1

        self.canvas.draw()

    # returns the canvas
    def getCanvas(self):
        return self.canvas

    # updates or adds a static line, supports up to 7 lines
    def updateline(self, name, value):
        if len(self.lines) < 7:
            self.lines[name] = value
