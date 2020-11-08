import tkinter as tk
from . import layouts
from . import applogic

class ItemLookupBottomPanel(layouts.Layout):
    #upcAdd function should take two params: upc and quantity
    #setstartingpos function should take a row and a col param
    def __init__(self, master, changeupc, setstartingpos, side=None):
        super().__init__(master, side=side)
        self.setstartingpos = setstartingpos
        self.changeupc = changeupc
        #upc entry stuff
        self.upcLabel = tk.Label(self.widget, text="Enter a 11 digit upc:")
        self.upcLabel.pack()
        self.upcvar = tk.StringVar()
        self.upcEntry = tk.Entry(self.widget, textvariable=self.upcvar)
        self.upcEntry.bind("<Return>", self.addupc)
        self.upcEntry.pack()

        #quantity entry stuff
        self.quantityLabel = tk.Label(self.widget, text="How many of this label:")
        self.quantityLabel.pack()
        self.quantityvar = tk.StringVar()
        self.quantityEntry = tk.Entry(self.widget, textvariable=self.quantityvar)
        self.quantityEntry.pack()
        self.quantityEntry.bind("<Return>", self.addupc)

        #add button stuff
        self.lookupbutton = tk.Button(self.widget, text="Add", command=self.addupc)
        self.lookupbutton.pack()

        #starting pos stuff
        self.startingcol = tk.StringVar()
        self.startingcol.set("1")
        self.startingrow = tk.StringVar()
        self.startingrow.set("1")
        self.startingrowlabel = tk.Label(self.widget, text="Enter the starting row")
        self.startingrowentry = tk.Entry(self.widget, textvariable=self.startingrow)
        self.startingrowlabel.pack()
        self.startingrowentry.pack()
        self.startingcollabel = tk.Label(self.widget, text="Enter the starting column")
        self.startingcolentry = tk.Entry(self.widget, textvariable=self.startingcol)
        self.startingcollabel.pack()
        self.startingcolentry.pack()

        self.refreshFunctions.append(self.validateUPC)
        self.refreshFunctions.append(self.validateQuantity)

        self.refreshFunctions.append(lambda: setstartingpos(**self.getstartingpos()))


    def addupc(self, event=None):
        self.validateUPC()
        self.validateQuantity()
        self.changeupc(self.upcvar.get(), {
            'quantity': self.quantityvar.get(),
        }, caller="addupc")

    def validateUPC(self):
        applogic.validateUPC(self.upcvar)

    def validateQuantity(self):
        applogic.validateQuantity(self.quantityvar, 3)

    def validateStartingPos(self):
        applogic.applyRange(self.startingrow, _max=20, _min=1)
        applogic.applyRange(self.startingcol, _max=4, _min=1)


    def getstartingpos(self):
        self.validateStartingPos()
        row = self.startingrow.get()
        if row == "":
            row = "1"
        col = self.startingcol.get()
        if col == "":
            col = "1"

        return {
            'row' : int(row) - 1,
            'col' : int(col) - 1,
            }
