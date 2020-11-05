from PIL import Image, ImageDraw
import fpdf
from fpdf import FPDF
import os, requests

def getupccode():
    inputnum = input("Enter a 11 digit number:\n\t")
    if (len(inputnum) == 11 and inputnum.isdecimal()):
        return inputnum
    return getupccode()

upcnum = getupccode()

PWD = os.getcwd()

#get barcode
url = "https://barcode.tec-it.com/barcode.ashx?data=%s&code=UPCA&multiplebarcodes=false&translate-esc=false&unit=Fit&dpi=96&imagetype=Gif&rotation=0&color=%%23000000&bgcolor=%%23ffffff&codepage=&qunit=Mm&quiet=0&dmsize=Default" % upcnum
r = requests.get(url, allow_redirects=True)
open('barcode.png', 'wb').write(r.content)


#create an image
im = Image.new('RGB', (500, 300), (128, 128, 128))
draw = ImageDraw.Draw(im)

draw.ellipse((100,100,150,200), fill=(255,0,0), outline=(0,0,0))

im.save('testimg.png', quality=95)


pdf = FPDF(unit="in",format="letter")
pdf.set_margins(left=0,top=0, right=0)
pdf.add_page()

pdf.set_font('Arial', size = 15)

pdf.cell(8.5, h=0.5, txt="Test Pdf", ln=1, align="C")
filelink = '%s\\testimg.png' % (PWD)

pdf.image(filelink)

pdf.output("testpdf.pdf")
