import tkinter as tk


class SharedVar:
    def __init__(self):

        self.data = ('Hoogste temperatuur', 'Laagste temperatuur',
                'Gemiddelde temperatuur', 'Hoogste lichtintensiteit',
                'Laagste lichtintensiteit', 'Gemiddelde lichtintensiteit',
                'Aantal aangesloten units','Aantal aangesloten temperatuursensoren',
                'Aantal aangesloten lichtsensoren', 'Uptime')

    def initvars(self, root):
        self.data = {'Hoogste temperatuur': tk.DoubleVar(root), 'Laagste temperatuur': tk.DoubleVar(root),
                     'Gemiddelde temperatuur': tk.DoubleVar(root), 'Hoogste lichtintensiteit': tk.DoubleVar(root),
                     'Laagste lichtintensiteit': tk.DoubleVar(root), 'Gemiddelde lichtintensiteit': tk.DoubleVar(root),
                     'Aantal aangesloten units': tk.IntVar(root),
                     'Aantal aangesloten temperatuursensoren': tk.IntVar(root),
                     'Aantal aangesloten lichtsensoren': tk.IntVar(root), 'Uptime': tk.StringVar(root)}
