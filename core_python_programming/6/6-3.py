#a
aList = raw_input('Enter a list of number,seperated by space:\n')
bList = []
for i in aList.split(' '):
    bList.append(int(i))
bList.sort()
print bList[::-1]
#b
aList = raw_input('Enter a list of number,seperated by space:\n')
bList = []
for i in aList.split(' '):
    bList.append(i)
bList.sort()
print bList[::-1]