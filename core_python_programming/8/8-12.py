begin = int(raw_input('Enter begin value: '))
end = int(raw_input('Enter end value: '))
print "%-8s%-10s%-10s" %('DEC','BIN','OCT',),
if end > 32:
    print '%-8s%-5s' %('HEX','ASCII')
    print '-'*41
else:
    print '%-3s'%'HEX'
    print '-'*32
for i in range(begin,end+1):
    print '%-8d%-10s%-10o%-8x' %(i,bin(i),i,i),
    if i >= 33:
        print '%3s'%chr(i)
    else:
        print ''