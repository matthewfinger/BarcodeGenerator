from fpdf import FPDF
import time, math

def createLetterPdf(marginTop=1, marginLeft=0.75, marginRight=0.75):
    pdf = FPDF(unit="in",format="letter")
    pdf.set_margins(left=marginLeft,top=marginTop, right=marginRight)
    pdf.set_font('Arial', size = 15)
    pdf.add_page()

    return pdf

def createBarcodePDF(imageList, outputfile="testbarcode.pdf"):
    success = True
    try:
        pdf = createLetterPdf(0,0,0)

        #for an Avery #8167
        marginTop = 0.5
        marginLeft = 0.3
        lblHSpacing = 0.3
        lblVSpacing = 0
        lblHPadding = 0.5
        lblVPadding = 0.05
        lblWidth = 1.75 - lblHPadding*2
        lblHeight = 0.5 - lblVPadding*2
        columnsperrow = 4
        rowsperpage = 20

        #assemble a list of lists to represent pages->rows->labels
        pages = []
        rows = []
        index = 0
        while index < len(imageList):
            rows.append(imageList[index:index + columnsperrow]) # for four columns
            index += columnsperrow

        index = 0
        while index < len(rows):
            pages.append(rows[index:index + rowsperpage]) #for 20 rows per page
            index += rowsperpage
        #make a page for each page array
        pagenum = 1
        for page in pages:
            #remember page is a list of lists
            yoffset = marginTop
            rownum = 1
            for row in page:
                pdf.text(x=0,y=yoffset + lblVPadding +0.25,txt= str(rownum))
                xoffset = marginLeft
                for img in row:
                    pdf.rect(w=lblWidth + lblHPadding*2, h=lblHeight+lblVPadding*2, x=xoffset, y=yoffset)
                    print(img)
                    pdf.image(img, x=xoffset + lblHPadding, y=yoffset + lblVPadding, w=lblWidth, h=lblHeight)
                    print(1)
                    xoffset += lblWidth + (lblHPadding * 2) + lblHSpacing
                yoffset += lblHeight + (lblVPadding * 2) + lblVSpacing
                rownum += 1

            if pagenum < len(pages):
                pdf.add_page(orientation="P")
            pagenum += 1

        pdf.output(outputfile)
    except Exception as inst:
        print('something went wrong!', inst)

    return {"success": success, "file":outputfile}
