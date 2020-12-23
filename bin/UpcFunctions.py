SAMPLE_UPC = "85001031409" # for dev testing only


#the base encoding is left side, odd pariety
BASE_ENCODING = {
    "0": (0,0,0,1,1,0,1),
    "1": (0,0,1,1,0,0,1),
    "2": (0,0,1,0,0,1,1),
    "3": (0,1,1,1,1,0,1),
    "4": (0,1,0,0,0,1,1),
    "5": (0,1,1,0,0,0,1),
    "6": (0,1,0,1,1,1,1),
    "7": (0,1,1,1,0,1,1),
    "8": (0,1,1,0,1,1,1),
    "9": (0,0,0,1,0,1,1),
}

BASE_ENCODING_INVERSE = {}

for key in BASE_ENCODING.keys():
    inverse_key = ''.join( [ str(e) for e in BASE_ENCODING[key] ] )
    BASE_ENCODING_INVERSE[inverse_key] = key

#the pattern at the beggining and end of the sequence
END_PATTERN = (1,0,1)

# the pattern that splits the left and right halves of the sequence
MIDDLE_PATTERN = (0,1,0,1,0)

# a map of the first EAN digit to the pariety patten of the following 6 digits (even->1, odd->0)
# only matters for EAN numbers
PARIETY_PATTERN = {
    "0": (0,0,0,0,0,0),
    "1": (0,0,1,0,1,1),
    "2": (0,0,1,1,0,1),
    "3": (0,0,1,1,1,0),
    "4": (0,1,0,0,1,1),
    "5": (0,1,1,0,0,1),
    "6": (0,1,1,1,0,0),
    "7": (0,1,0,1,0,1),
    "8": (0,1,0,1,1,0),
    "9": (0,1,1,0,1,0),
}

def invert(binary_list):
    out = []
    for bit in binary_list:
        assert (bit == 1 or bit == 0)
        if bit == 0:
            out.append(1)
        else:
            out.append(0)

    return out

def get_digit_encoding(digit, left=True, even=0):
    digit = int(digit)
    assert digit <= 9 and digit >= 0
    digit = str(digit)
    out = BASE_ENCODING[digit]
    if not left:
        out = tuple(invert(list(out)))
    elif even:
        binary_list = list(out)
        binary_list.reverse()
        out = tuple(invert( binary_list ))
    return out


# returns a lsit of tuples representing the graphical representation
# of a tuple of binary values. the first element in each tuple is the width, the
# second element is the value
def get_digit_bars(binary_tuple):
    out = []
    lastval = None
    width = 0
    for bit in binary_tuple:
        assert (bit == 0 or bit == 1)
        if bit != lastval and lastval != None:
            out.append([width, lastval])
            width = 0
        width += 1
        lastval = bit

    out.append([width, lastval])

    return out


def get_checkdigit(ean):
    ean = str(ean)
    ean = ean[::-1]
    assert ean.isnumeric()
    checksum = 0
    index = 0

    while index < len(ean):
        if (not index % 2): #if index is odd
            checksum += int(ean[index]) * 3
        else:
            checksum += int(ean[index])
        index += 1

    checkdigit = -checksum
    while checkdigit < 0:
        checkdigit += 10

    return checkdigit

#converts a numeric 12-digit ean into a 13-digit binary encoding
#returns a list of binary tuples
def get_ean_encoding(ean):
    ean = str(ean)
    if len(ean) < 13:
        ean += '%d' % get_checkdigit("%s" % ean)
    assert ean.isnumeric() and len(ean) == 13

    pariety = PARIETY_PATTERN[ean[0]]
    left_half = ean[1:7]
    right_half = ean[7:]

    out = []
    out.append(END_PATTERN)

    #generate the left half
    index = 0
    for digit in left_half:
        out.append(get_digit_encoding(digit, even=pariety[index]))
        index += 1

    #add the middle pattern
    out.append(MIDDLE_PATTERN)

    #generate the right half
    for digit in right_half:
        out.append(get_digit_encoding(digit, left=False))

    #add the end pattern
    out.append(END_PATTERN)

    #return the list
    return out

def get_digit_from_tuple(binary_tuple, left=None):
    binary_str = ''.join([ str(bit) for bit in binary_tuple ])
    if binary_str in BASE_ENCODING_INVERSE.keys():


        return BASE_ENCODING_INVERSE[binary_str]

    #check for right encoding
    binary_tuple = tuple(invert(list(binary_tuple)))
    binary_str = ''.join([ str(bit) for bit in binary_tuple ])
    if not left:
        if binary_str in BASE_ENCODING_INVERSE.keys():

            return BASE_ENCODING_INVERSE[binary_str]

    #check for left even pariety encoding
    binary_list = list(binary_tuple)
    binary_list.reverse()
    binary_tuple = tuple(binary_list)
    binary_str = ''.join([ str(bit) for bit in binary_tuple ])
    if left or left == None:
        if binary_str in BASE_ENCODING_INVERSE.keys():

            return BASE_ENCODING_INVERSE[binary_str]

    return None

def get_digit_from_bars(bars:list, left=None):
    binary_list = []
    for bar in bars:
        binary_list += [int(bar[1])] * bar[0]

    binary_tuple = tuple(binary_list)
    return get_digit_from_tuple(binary_tuple, left)

def get_bars(ean_list:list):
    out = []
    for binary_tuple in ean_list:
        out.append(get_digit_bars(binary_tuple))

    return out

def get_upc_encoding(upc:str):
    ean = "0" + upc
    assert len(ean) == 13
    out = get_ean_encoding(ean)
    return out
