import tkinter as tk
from . import layouts
from . import applogic
from .incrementpanel import IncrementPanel

class UpcRow(layouts.Layout):
    def __init__(self, master, upcvar, quantityvar):
        super().__init__(master)
        self.widget['height'] = 50
        #upc stuff
        self.upcframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE, padx=1, pady=1)
        self.upcframe.pack(side=tk.LEFT)
        self.upcentry = tk.Entry(self.upcframe, textvariable=upcvar, font=("px", 28, "normal"), width=12)
        self.upcentry.pack()

        #quantity stuff
        self.quantityframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE)
        self.quantityframe.pack(side=tk.RIGHT)
        self.quantityentry = tk.Entry(self.quantityframe, textvariable=quantityvar, font=("px", 28, "normal"), width=12)
        self.quantityentry.pack()


class TopRow(layouts.Layout):
    def __init__(self, master):
        super().__init__(master)
        self.widget['height'] = 50
        #upc stuff
        self.upcframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE)
        self.upcframe.pack(side=tk.LEFT)
        self.upclabel = tk.Label(self.upcframe, text="UPC", justify=tk.CENTER, font=("px", 20, "normal"), width=12)
        self.upclabel.pack()

        #quantity stuff
        self.quantityframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE)
        self.quantityframe.pack(side=tk.RIGHT)
        self.quantitylabel = tk.Label(self.quantityframe, text="quantity", justify=tk.CENTER, font=("px", 20, "normal"), width=12)
        self.quantitylabel.pack()

class FrameBox(layouts.Layout):
    #getupcs is a function that retruns a list of all upcs in the parent layout
    #changeupc is a function that changes a upc ex. changeupc("<upcname>", {<upcdetails>})
    def __init__(self, master, getupcs, changeupcs, side=None):
        super().__init__(master, side=side)
        self.getupcs = getupcs
        self.changeupcs = changeupcs
        self.incrementpanel = IncrementPanel(self.widget, self.incrementRows, self.decrementRows)
        self.incrementpanel.widget.config(relief="raised", borderwidth=2)
        self.incrementpanel.widget.pack(side=tk.LEFT, fill="y", expand=True, padx=10, pady=10)

        self.toprow = TopRow(self.widget)
        self.toprow.widget.pack(side=tk.TOP, fill="x")
        self.upcindex = 0



        #self.upcentries will be a list of tuples
        self.upcentries = []
        for index in range(11):
            upcvar = tk.StringVar()
            quantityvar = tk.StringVar()
            newentry = {
                "quantityvar": quantityvar,
                "upcvar": upcvar,
                "upcrow": UpcRow(self.widget, upcvar, quantityvar),
                "upcindex": None,
                "visible": False,
            }
            self.refreshFunctions.append(lambda: applogic.validateQuantity(quantityvar))
            self.refreshFunctions.append(lambda: applogic.validateUPC(upcvar))
            self.upcentries.append(newentry)

        self.refreshFunctions.append(self.fillRows)


    #this function syncs the rows with with the current values for the upc list
    def fillRows(self):
        upcs = self.getupcs()
        upcindex = self.upcindex
        upckeys = list(self.getupcs().keys())[upcindex : upcindex + 11]
        index = 0
        for i in range(11):
            applogic.validateQuantity(self.upcentries[index]['quantityvar'])
            applogic.validateUPC(self.upcentries[index]['upcvar'])
            if i < len(upckeys):
                upc = upckeys[i]
                changeupc = False
                newupcinfo = {}
                #if row is not visible, make it visible
                if not self.upcentries[index]['visible']:
                    self.upcentries[index]['upcrow'].widget.pack()
                    self.upcentries[index]['visible'] = True

                if self.upcentries[index]["upcindex"] == index + upcindex and not upcs[upc][2]:

                    #check whether we have to change upc
                    if upc != self.upcentries[index]['upcvar'].get():
                        changeupc = True
                        newupcinfo['upc'] = self.upcentries[index]['upcvar'].get()

                    #check wheter we have to change quantity
                    if upcs[upc][0] != int(self.upcentries[index]['quantityvar'].get()):
                        changeupc = True
                        newupcinfo['quantity'] = int(self.upcentries[index]['quantityvar'].get())

                    if changeupc:
                        self.changeupcs(upc, newupcinfo)


                else:
                    self.upcentries[index]["upcindex"] = index + upcindex
                    self.upcentries[index]['upcvar'].set(upc)
                    self.upcentries[index]['quantityvar'].set(upcs[upc][0])
                    self.changeupcs(upc, {'lastupdated': False})

                    #if row is visible, make it not so
            elif self.upcentries[index]['visible']:
                self.upcentries[index]['upcrow'].widget.pack_forget()
                self.upcentries[index]['visible'] = False


            index += 1

    # Function that increases the starting index for the rows
    def incrementRows(self, interval=1):
        numrows = len(self.getupcs().values())
        if (self.upcindex + interval) + 1 < numrows:
            self.upcindex += interval
        elif self.upcindex + 1 < numrows:
            self.upcindex = numrows - 1

    # Function that decreases the starting index for the rows
    def decrementRows(self, interval=1):
        if self.upcindex >= interval:
            self.upcindex -= interval
        elif self.upcindex > 0:
            self.upcindex = 0
