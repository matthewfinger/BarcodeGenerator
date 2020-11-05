import gui.app as gui
import functions.barcode as bcode
import functions.pdf as pdf

def inputupc():
    i = input('Enter a 11 digit number:\n\t')
    if len(i) == 11 and i.isnumeric():
        return i
    return inputupc()


def inputnum():
    i = input('How many do you want to print:\n\t')
    if i.isnumeric():
        return i
    return inputnum()


def makeBarcodes(upcDict):
    if not "upc" in upcDict.keys():
        return ""
    return bcode.getbarcode(upcDict['upc'])



testapp = gui.App(bcode.getbarcode, pdf.createBarcodePDF)


testapp.run()
