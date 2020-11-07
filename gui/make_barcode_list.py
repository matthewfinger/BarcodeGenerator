import tkinter as tk
from . import layouts
from . import applogic

class ItemLookupBottomPanel(layouts.Layout):
    #upcAdd function should take two params: upc and quantity
    #setstartingpos function should take a row and a col param
    def __init__(self, master, upcAdd, setstartingpos, side=None):
        super().__init__(master, side=side)
        #upc entry stuff
        self.upcLabel = tk.Label(self.widget, text="Enter a 11 digit upc:")
        self.upcLabel.pack()
        self.upcvar = tk.StringVar()
        self.upcEntry = tk.Entry(self.widget, textvariable=self.upcvar)
        self.upcEntry.bind("<Return>", lambda event: upcAdd(self.upcvar, self.quantityvar))
        self.upcEntry.pack()

        #quantity entry stuff
        self.quantityLabel = tk.Label(self.widget, text="How many of this label:")
        self.quantityLabel.pack()
        self.quantityvar = tk.StringVar()
        self.quantityEntry = tk.Entry(self.widget, textvariable=self.quantityvar)
        self.quantityEntry.pack()

        #add button stuff
        self.lookupbutton = tk.Button(self.widget, text="Add", command=lambda: upcAdd(self.upcvar, self.quantityvar))
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
        self.refreshFunctions.append(self.validateStartingPos)
        self.refreshFunctions.append(lambda: setstartingpos(row=int(self.startingrow.get()), col=int(self.startingcol.get())))


    def validateUPC(self):
        applogic.validateUPC(self.upcvar)

    def validateQuantity(self):
        applogic.validateQuantity(self.quantityvar, 3)

    def validateStartingPos(self):
        applogic.makeNumeric(self.startingrow)
        applogic.makeNumeric(self.startingcol)
        col = int(self.startingcol.get())
        row = int(self.startingrow.get())
        if row > 20:
            self.startingrow.set("20")
        elif row < 1:
            self.startingrow.set("1")

        if col > 4:
            self.startingcol.set("4")
        elif col < 1:
            self.startingcol.set("1")


class MakeBarcodeList(layouts.Layout):
    def __init__(self, master, makeupcfun, makepdffun, pdfurl:str=""):
        super().__init__(master)
        self.bottomPanel = ItemLookupBottomPanel(self.widget, self.upcAdd)
        self.bottomPanel.widget.pack()
        for function in self.bottomPanel.refreshFunctions:
            self.refreshFunctions.append(function)

        self.pdfurl = pdfurl
        self.makeupcfun = makeupcfun
        self.makepdffun = makepdffun

    def upcAdd(self):
        self.bottomPanel.validateUPC()
        self.bottomPanel.validateQuantity()

        upc = self.bottomPanel.upcvar.get()
        quantity = self.bottomPanel.quantityvar.get()

        while len(upc) < 11:
            upc += '0'
        self.bottomPanel.upcvar.set(upc)

        if quantity == "0" or quantity == '':
            quantity = "1"
        self.bottomPanel.quantityvar.set(quantity)

        self.upcs.append({"upc": upc, "quantity": quantity})

    def makeBarcodes(self):
        for upc in self.upcs:
            upc["imageURL"] = self.makeupcfun(upc)

    def getPDFImageList(self):
        res = []
        for upc in self.upcs:
            keys = upc.keys()
            if "imageURL" in keys and "quantity" in keys:
                res += ([upc['imageURL']] * upc['quantity'])
        return res

    def makePDF(self):
        images = self.getPDFImageList()
        pdfresult = None
        if self.pdfurl:
            pdfresult = self.makepdffun(images, self.pdfurl)
        else:
            pdfresult = self.makepdffun(images)

        self.pdfurl = pdfresult["file"]
