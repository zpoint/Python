dic1 = {}
dic2 = {}
k = raw_input('Enter dictionary seperate by ,[Empty to terminate]\n').split(',')
for i in range(len(k)):
    temp = k[i].split(':')
    dic1.update({temp[0]:temp[1]})
    dic2.update({temp[1]:temp[0]})
print "you input dic:",dic1
print 'I converse it to:',dic2
