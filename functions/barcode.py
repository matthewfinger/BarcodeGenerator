import requests, io, random, os
from PIL import Image, ImageTk

def getbarcode(upc:str):
    upc = makeNumeric(upc)
    upc = upc[0:11]
    imgpath = os.getcwd() + "\\cache\\.%s.temp.png" % upc
    #we only want to use the url if we don't have the image cached already!
    while not os.path.exists(imgpath):
        url = "https://barcode.tec-it.com/barcode.ashx?data=%s&code=UPCA&multiplebarcodes=false&translate-esc=false&unit=Fit&dpi=96&imagetype=png&rotation=0&color=%%23000000&bgcolor=%%23ffffff&codepage=&qunit=Mm&quiet=0&dmsize=Default" % upc

        res = requests.get(url, allow_redirects=True)
        #print(res.content)
        file = open(imgpath, 'wb')
        file.write(res.content)
        file.close()
    return imgpath

def generateupc():
    randomnum = random.random()
    randomnum = randomnum * (10**11)
    randomstr = str(randomnum)
    randomstr = randomstr[0:11]
    return randomstr


def getchecksum(upc:str):
    if upc.isnumeric():
        upc = upc[0:11]
        i = 0
        oddsum = 0
        while i < len(upc):
            oddsum += int(upc[i])
            i += 2
        oddproduct = oddsum * 3

        i = 1
        evensum = 0
        while i < len(upc):
            evensum += int(upc[i])
            i += 2

        chksum = ( (evensum + oddproduct) % 10 )
        chksum = 10 - chksum
        chksum = chksum % 10

        return chksum


    return None

def makeNumeric(num:str):
    out = ""
    for char in num:
        if char.isnumeric():
            out += char

    return out
