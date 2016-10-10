SortList = [1,2,3]
for i in range(3):
    print 'Please enter num %d\n' %(i+1)
    SortList[i] = raw_input()
print 'Before sort'
for i in range(3):
    print 'SortList [%d] is'%(i), SortList[i]
#Sort
if SortList[0] < SortList[1]:
    temp = SortList[0]
    SortList[0] = SortList[1]
    SortList[1] = temp
if SortList[0] < SortList[2]:
    temp = SortList[0]
    SortList[0] = SortList[2]
    SortList[2] = temp
if SortList[1] < SortList[2]:
    temp = SortList[1]
    SortList[1] = SortList[2]
    SortList[2] = temp
print 'After Sort'
for i in range(3):
    print 'SortList [%d] is'%(i), SortList[i]