def getfactors(num):
    alist = []
    for i in range(1,num+1):
        if num % i == 0:
            alist.append(i)
    return alist

print getfactors(int(raw_input('Please enter a number to get factors:')))