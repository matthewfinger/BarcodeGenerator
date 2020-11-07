# this module contains all the callbacks and other logic for the gui to work
# most of the methods are permutation methods for tk.StringVar (ie makeNumeric, makeLength, etc)

def makeNumeric(var):
    if var.get() == "":
        return var
    input = var.get()
    newinput = extractNumbers(input)
    var.set(newinput)
    return var

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
    return var

def applyRange(var, _max=None, _min=0):
    makeNumeric(var)
    if var.get() == "":
        return var
    curval = int(var.get())
    if type(_max) == int:
        curval = min(curval, _max)
    if type(_min) == int:
        curval = max(curval, _min)
    var.set("%d" % curval)
    return var


def validateUPC(upcvar):
    makeNumeric(upcvar)
    makeLength(upcvar, 11)
    return upcvar

def validateQuantity(quantityvar, quantityLength:int = 3):
    if quantityvar.get() == '':
        quantityvar.set('1')
    makeNumeric(quantityvar)
    makeLength(quantityvar, quantityLength)
    return quantityvar
