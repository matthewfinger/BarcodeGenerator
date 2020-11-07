import tkinter as tk
from . import applogic

class Layout:
    def __init__(self, master, side=None):
        self.widget = tk.Frame(master)
        self.master = master
        self.refreshFunctions = [self.refreshChildFunctions]
        self.layouts = {}
        self.side = side

    def refreshChildFunctions(self):
        for child in self.layouts.values():
            for function in child.refreshFunctions:
                function()

    def addLayout(self, layoutname:str, layout):
        if layoutname in self.layouts.keys():
            print("could not add layout %s because it already exists!" % layoutname)
            return

        self.layouts[layoutname] = layout

    def loadLayout(self, layoutname:str):
        if layoutname in self.layouts.keys():
            _side = self.layouts[layoutname].side
            if (_side):
                self.layouts[layoutname].widget.pack(side=_side, fill="both", expand=True)
            else:
                self.layouts[layoutname].widget.pack(fill="both", expand=True)

    def unloadLayout(self, layoutname:str):
        if layoutname in self.layouts.keys():
            self.layouts[layoutname].widget.pack_forget()
