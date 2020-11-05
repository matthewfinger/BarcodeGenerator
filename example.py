testinputs = ["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]

def listCompare(smaller, bigger):
    if bigger == None:
        return True
    if smaller == None:
        return True

    index = 0
    while index < len(smaller) or index < len(bigger):
        if index == len(smaller):
            return True
        elif index == len(bigger):
            return False
        else:
            smallerval = int(smaller[index])
            biggerval = int(bigger[index])
            if biggerval != smallerval:
                return (biggerval > smallerval)
        index += 1

    return True

def findSortedIndex(item, _list):
    if len(_list) == 0:
        return 0
    index = len(_list) // 2
    diff = index // 2
    if diff == 0:
        diff = 1
    bigger = None
    smaller = None
    if index < len(_list) and index >= 0:
        bigger = _list[index]
    if index - 1 < len(_list) and index -1 >= 0:
        smaller = _list[index - 1]
    nextItem = listCompare(item, bigger)
    prevItem = listCompare(smaller, item)
    while not (prevItem and nextItem):
        if not nextItem:
            index += diff
        else:
            index -= diff
        diff = diff // 2
        if diff == 0:
             diff = 1
        if index < len(_list) and index >= 0:
            bigger = _list[index]
        else:
            bigger = None
        if index - 1 < len(_list) and index -1 >= 0:
            smaller = _list[index - 1]
        else:
            smaller = None
        nextItem = listCompare(item, bigger)
        prevItem = listCompare(smaller, item)
        print(item, bigger, nextItem)
        print(item, smaller, prevItem)
        input()

    return index


def solution(l):
    #make all strings of version into lists
    versionlist = []
    for version in l:
        versionlist.append(version.split('.'))
    #insert versions in the correct order into the sorted list
    sortedList = []

    for version in versionlist:
        sortedList.insert(findSortedIndex(version, sortedList), version)

    #convert all sorted versions back to strings
    out = []
    for version in sortedList:
        out.append('.'.join(version))
    return out

print(solution(testinputs))
