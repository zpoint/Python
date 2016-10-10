def myPop(alist):
    del alist[len(alist) - 1]
    return alist
alist = list(raw_input('Enter a list seperate by \',\'\n').split(','))
print myPop(alist)