Dict = {}
lis = raw_input('Enter a list of employee name and number seperated by \',\' i.e. John:1,Adam:2\n').split(',')
for i in range(len(lis)):
    temp = lis[i].split(':')
    Dict.update({temp[0]:int(temp[1])})
print 'Output by'
print '(N)ame,n(U)mbers'
while True:
    choice = raw_input("Your choice:(other character to quit)\n").upper()[0]
    if choice == 'N':
        sorlist = sorted(Dict.iteritems())
    elif choice == 'U':
        sorlist = sorted(Dict.iteritems(),key = lambda a:a[1])
    else:
        break
    print 'name','number'
    for i in range(len(sorlist)):
        print "%-4s %-6d" %(sorlist[i][0],sorlist[i][1])