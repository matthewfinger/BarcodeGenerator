import gui.app as gui
import bin.barcode as bcode
import bin.pdf as pdf
from bin.DrawFunctions import make_barcode_path

testapp = gui.App(make_barcode_path, pdf.createBarcodePDF)
testapp.run()
