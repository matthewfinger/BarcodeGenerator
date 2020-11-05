import tkinter as tk
from . import applogic

class Layout:
    def __init__(self, master):
        self.widget = tk.Frame(master)
        self.master = master
        self.refreshFunctions = [self.refreshChildFunctions]
        self.layouts = {}

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
            self.layouts[layoutname].widget.pack(expand=False)

    def unloadLayout(self, layoutname:str):
        if layoutname in self.layouts.keys():
            self.layouts[layoutname].widget.pack_forget()
