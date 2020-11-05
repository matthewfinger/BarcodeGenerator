import tkinter as tk
from . import layouts
from . import applogic

class UpcRow(layouts.Layout):
    def __init__(self, master, upcvar, quantityvar):
        super().__init__(master)
        self.widget['height'] = 50
        #upc stuff
        self.upcframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE)
        self.upcframe.pack(side=tk.LEFT)
        self.upcentry = tk.Entry(self.upcframe, textvariable=upcvar)
        self.upcentry.pack()

        #quantity stuff
        self.quantityframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE)
        self.quantityframe.pack(side=tk.RIGHT)
        self.quantityentry = tk.Entry(self.quantityframe, textvariable=quantityvar)
        self.quantityentry.pack()


class TopRow(layouts.Layout):
    def __init__(self, master):
        super().__init__(master)
        self.widget['height'] = 50
        #upc stuff
        self.upcframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE)
        self.upcframe.pack(side=tk.LEFT)
        self.upclabel = tk.Label(self.upcframe, text="UPC", justify=tk.LEFT)
        self.upclabel.pack()

        #quantity stuff
        self.quantityframe = tk.Frame(self.widget, width=275, relief=tk.GROOVE)
        self.quantityframe.pack(side=tk.RIGHT)
        self.quantitylabel = tk.Label(self.quantityframe, text="quantity", anchor="w")
        self.quantitylabel.pack()

class FrameBox(layouts.Layout):
    #getupcs is a function that retruns a list of all upcs in the parent layout
    #changeupc is a function that changes a upc ex. changeupc("<upcname>", {<upcdetails>})
    def __init__(self, master, getupcs, changeupcs):
        super().__init__(master)
        self.getupcs = getupcs
        self.changeupcs = changeupcs
        self.toprow = TopRow(self.widget)
        self.toprow.widget.pack()
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
            }
            self.upcentries.append(newentry)
            newentry['upcrow'].widget.pack()
            self.refreshFunctions.append(lambda: applogic.validateQuantity(quantityvar))
            self.refreshFunctions.append(lambda: applogic.validateUPC(upcvar))
        self.refreshFunctions.append(self.fillRows)


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
                    print("updating upcrow")
                    self.upcentries[index]["upcindex"] = index + upcindex
                    self.upcentries[index]['upcvar'].set(upc)
                    self.upcentries[index]['quantityvar'].set(upcs[upc][0])
                    self.changeupcs(upc, {'lastupdated': False})

            index += 1
