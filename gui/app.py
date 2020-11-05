import tkinter as tk
from . import make_barcode_list
from . import layouts
from . import barcodelist

class MakeUpcsLayout(layouts.Layout):
    #makeupcurl should take 1 parameter: upc, and makepdffun should take a list of tuples, such that (url, quantity), and a start position such that (row, col)
    def __init__(self, master, makeupcurl, makepdffun):
        super().__init__(master)
        self.upcs = {}
        self.startingrow = 0
        self.startingcol = 0
        self.makeupcurl = makeupcurl
        self.makepdffun = makepdffun
        masterheight = self.master.winfo_height()
        masterwidth = self.master.winfo_width()
        self.listFrame = tk.Frame(self.widget, height=600, width=600)
        self.listFrame.pack(side=tk.LEFT)
        self.addLayout('barcodelist', barcodelist.FrameBox(self.listFrame, self.getupcs, self.changeupc))
        self.loadLayout('barcodelist')


        self.bottomFrame = tk.Frame(self.widget, bd=1, relief=tk.GROOVE, height=600)
        self.bottomFrame.pack(expand=False)
        self.addLayout("bottomPanel", make_barcode_list.ItemLookupBottomPanel(self.bottomFrame, self.upcAdd, self.setstartingpos))
        self.loadLayout("bottomPanel")
        self.generatePdfButton = tk.Button(self.bottomFrame, text="Make Label Pdf", command=self.makePDF)
        self.generatePdfButton.pack()


    #function that actually generates a pdf to be printed
    def makePDF(self):
        upclist = []
        for pair in self.upcs.values():
            upclist += [pair[1]] * pair[0]
        self.makepdffun(upclist)#, (self.startingrow, self.startingcol))

    def setstartingpos(self, row=None, col=None):
        if type(row) == int:
            self.startingrow = row

        if type(col) == int:
            self.startingcol = col

    #function that either generates a new upc image and gets the url, or increments the value of the upc
    def upcAdd(self, upcvar, quantityvar):

        upc = upcvar.get()
        quantity = quantityvar.get()

        while len(upc) < 11:
            upc += '0'
        upcvar.set(upc)

        if quantity == "0" or quantity == '':
            quantity = "1"
        quantityvar.set(quantity)

        #if the upc has already been generated, only increment the quantity
        if upc in self.upcs.keys():
            print("Adding %s to the quantity of upc %s" % (quantity, upc))
            self.upcs[upc][0] += int(quantity)
            self.upcs[upc][2] = True
            return

        upcurl = self.makeupcurl(upc)
        self.upcs[upc] = [int(quantity), upcurl, True,]

    def getupcs(self):
        return self.upcs

    def changeupc(self, upcname:str, newupcvars:dict):
        if not upcname in self.upcs.keys():
            print("Upc %s does not exist!" % upcname)
            return
        #if we're changing the upc, we'll have to change the key and record itself
        if "upc" in newupcvars.keys():
            newupc = newupcvars["upc"]
            self.upcs[newupc] = [self.upcs[upcname][0], self.upcs[upcname][1], False]
            del self.upcs[upcname]
            upcname = newupc

        #chnage other params where applicable
        if "quantity" in newupcvars.keys():
            if type(newupcvars['quantity']) == int and newupcvars['quantity'] > 0:
                self.upcs[upcname][0] = newupcvars['quantity']

        self.upcs[upcname][2] = False




class App(layouts.Layout):
    def __init__(self, makeupcurl, makepdffun):
        self.rootframe = tk.Tk()
        self.rootframe.geometry("800x600")
        self.layouts = {}
        self.refreshFunctions = [self.refreshChildFunctions]
        self.addLayout("makeBarcodes", MakeUpcsLayout(self.rootframe, makeupcurl, makepdffun))
        self.loadLayout("makeBarcodes")


    def run(self):
        self.rootframe.after(1, self.rootframeLoop)
        self.rootframe.mainloop()

    def rootframeLoop(self):
        #logic
        callback = self.rootframeLoop
        for function in self.refreshFunctions:
            function()
        #recursion
        self.rootframe.after(10, callback)
