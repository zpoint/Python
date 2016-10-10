balance = float(raw_input('Enter Opening balance:'))
mp = float(raw_input("Enter monthly Payment:"))
i = 0
print '\t\t%s\t\t%s' %('  Amount','    Remaining')
print '%s\t\t%s\t\t\t%s' %('  Pymt#','   Paid','     Balance')
print '%s\t%s\t\t%s' %('- ' *5,'- '*6,'- '*9)
while (balance != 0):
    if i == 0:
        tmp = 0
    elif balance < 0:
        tmp = balance + mp
        balance = 0
    else:
        tmp = mp
    print '    %d\t\t$  %.2f\t\t$    %.2f' %(i,tmp,balance)
    i+= 1
    if balance != 0:
        balance -= mp