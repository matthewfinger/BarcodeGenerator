import gui.app as gui
import functions.barcode as bcode
import functions.pdf as pdf

testapp = gui.App(bcode.getbarcode, pdf.createBarcodePDF)
testapp.run()
