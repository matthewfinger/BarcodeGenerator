import tkinter as tk
from . import make_barcode_list
from . import layouts
from . import barcodelist
from . import applogic
import os

CWD = os.getcwd()
ICONPHOTO_PATH = "%s\\gui\\images\\iconphoto.png" % CWD

class MakeUpcsLayout(layouts.Layout):
    #makeupcurl should take 1 parameter: upc, and makepdffun should take a list of tuples, such that (url, quantity), and a start position such that (row, col)
    def __init__(self, master, makeupcurl, makepdffun):
        super().__init__(master)
        self.upcs = []
        self.startingrow = 0
        self.startingcol = 0
        self.makeupcurl = makeupcurl
        self.makepdffun = makepdffun
        masterheight = self.master.winfo_height()
        masterwidth = self.master.winfo_width()
        self.listFrame = tk.Frame(self.widget, height=600, width=600)
        self.listFrame.pack(side=tk.LEFT, expand=True, fill='both')
        self.addLayout('barcodelist', barcodelist.FrameBox(self.listFrame, self.getupcs, self.changeupc, side=tk.TOP))
        self.loadLayout('barcodelist')


        self.rightFrame = tk.Frame(self.widget, bd=1, relief=tk.GROOVE, height=600)
        self.rightFrame.pack(side=tk.RIGHT)
        self.addLayout("rightPanel", make_barcode_list.ItemLookupBottomPanel(self.rightFrame, self.changeupc, self.setstartingpos))
        self.loadLayout("rightPanel")
        self.generatePdfButton = tk.Button(self.rightFrame, text="Make Label PDF", command=self.makePDF)
        self.generatePdfButton.pack()
        self.refreshFunctions.append(self.validateVars)
        self.once = 0


    #function that actually generates a pdf to be printed
    def makePDF(self):
        upclist = []
        for row in self.upcs:
            url = self.makeupcurl(row[0].get())
            upclist += [url] * int(row[1].get())
        self.makepdffun(upclist, startingpos=(self.startingrow, self.startingcol))

    def setstartingpos(self, row=None, col=None):
        if type(row) == int:
            self.startingrow = row

        if type(col) == int:
            self.startingcol = col

    def getupcs(self):
        return self.upcs

    def changeupc(self, upcname:str, newupcvars:dict, caller=None):
        upcindex = None
        isnew = False
        i = 0
        while i < len(self.upcs) and not upcindex:
            #if the upc is in the list
            if upcname == self.upcs[i][0].get():
                upcindex = i
            i += 1

        if upcindex == None:
            isnew = True
            upcindex = len(self.upcs)
            self.upcs.append([tk.StringVar(), tk.StringVar()])
            newupcvars['upc'] = upcname

        if "upc" in newupcvars.keys():
            self.upcs[upcindex][0].set(newupcvars['upc'])
            newupcvars['url'] = self.makeupcurl(newupcvars['upc'])

        if 'quantity' in newupcvars.keys():
            if newupcvars['quantity'] in ['', '0'] or not(newupcvars['quantity'].isnumeric()):
                newupcvars['quantity'] = '1'
            if isnew:
                self.upcs[upcindex][1].set(newupcvars['quantity'])
            else:
                applogic.validateQuantity(self.upcs[upcindex][1])
                q = int(self.upcs[upcindex][1].get())
                newquantity = q + int(newupcvars['quantity'])
                self.upcs[upcindex][1].set("%d" % newquantity)


        self.layouts['barcodelist'].pullRows()
        if self.once < 3:
            self.once += 1


    def validateVars(self):
        for upclist in self.upcs:
            applogic.validateUPC(upclist[0])
            applogic.validateQuantity(upclist[1])



class App(layouts.Layout):
    def __init__(self, makeupcurl, makepdffun):
        self.rootframe = tk.Tk()
        self.rootframe.title("Barcode Generator")
        print(ICONPHOTO_PATH)
        if os.path.exists(ICONPHOTO_PATH):
            self.iconphoto = tk.PhotoImage(file=ICONPHOTO_PATH)
            self.rootframe.iconphoto(True, self.iconphoto)
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
