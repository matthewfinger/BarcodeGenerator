import tkinter as tk
from . import make_barcode_list
from . import layouts
from . import barcodelist

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


    #function that actually generates a pdf to be printed
    def makePDF(self):
        upclist = []
        for row in self.upcs:
            upclist += [row[2]] * row[1]
        self.makepdffun(upclist, startingpos=(self.startingrow, self.startingcol))

    def setstartingpos(self, row=None, col=None):
        if type(row) == int:
            self.startingrow = row

        if type(col) == int:
            self.startingcol = col

    def getupcs(self):
        return self.upcs

    def changeupc(self, upcname:str, newupcvars:dict):
        upcindex = None
        updatedrow = []
        i = 0
        while i < len(self.upcs) and not upcindex:
            #if the upc is in the list
            if upcname == self.upcs[i][0]:
                upcindex = i
                updatedrow = list(self.upcs[upcindex])
            i += 1

        #if the upc is not in the list
        if not upcindex:
            print('hi')
            upcindex = len(self.upcs)
            quantity = 1
            newkeys = newupcvars.keys()
            if 'quantity' in newkeys:
                if type(newupcvars['quantity']) == str and newupcvars['quantity'].isnumeric():
                    quantity = int(newupcvars['quantity'])
            lastupdated = False
            if 'lastupdated' in newkeys:
                bool(newupcvars['lastupdated'])
            self.upcs.append([upcname, quantity, "", lastupdated])
            return
            newupcvars['upc'] = upcname
            newupcvars['lastupdated'] = False

        currentrow = self.upcs[upcindex]
        changedfields = newupcvars.keys()

        #if we're getting a new upc
        if not currentrow[2]:
            newupc = upcname
            if 'upc' in changedfields:
                newupc = newupcvars['upc']
            newupcvars['url'] = self.makeupcurl(newupc)
            changedfields = newupcvars.keys()

        i = 0
        for property in ['upc', 'quantity', 'url', 'lastupdated']:
            if property in changedfields and self.upcs[upcindex][i] != newupcvars[property]:

                print(self.upcs[upcindex][i])
                self.upcs[upcindex][i] = newupcvars[property]
            i += 1
        return
        #make sure quantity is a var
        if type(updatedrow[1]) != int:
            if type(updatedrow[1]) == str and updatedrow[1].isnumeric():
                updatedrow[1] = int(updatedrow[1])
            else:
                updatedrow[1] = 1
        print(upcindex)
        self.upcs[upcindex] = updatedrow



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
