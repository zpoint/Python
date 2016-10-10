def getfactors(num):
    alist = []
    for i in range(1,num):
        if num % i == 0:
            alist.append(i)
    return alist

def isperfect(num):
    if sum(getfactors(num)) == num:
        print 1
    else:
        print 0

isperfect(int(raw_input('Please enter a number to determine whether it\'s Perfect Number')))