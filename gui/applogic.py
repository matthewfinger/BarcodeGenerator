#this file contains all the callbacks and other logic for the gui to work
def makeNumeric(var):
    input = var.get()
    newinput = extractNumbers(input)
    var.set(newinput)

def extractNumbers(var:str):
    res = ""
    for character in var:
        if character.isnumeric():
            res += character
    return res

def makeLength(var, length:int):
    input = var.get()
    if len(input) > length:
        input = input[0:length]
        var.set(input)

def validateUPC(upcvar):
    makeNumeric(upcvar)
    makeLength(upcvar, 11)

def validateQuantity(quantityvar, quantityLength:int = 3):
    if quantityvar.get() == '':
        quantityvar.set('1')
    makeNumeric(quantityvar)
    makeLength(quantityvar, quantityLength)
