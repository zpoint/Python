def show_getF():
    print """
    Your option:
    (S)manage savings
    (C)checking
    (M)money market
    (D)certificate of deposit
    (Q)quit
    """
    return raw_input()[0].upper()
def show_get():
    print """
    Your option:
    (1)Deposits
    (2)Withdrawals
    (3)Debits
    (4)Credits
    """
    return int(raw_input()[0])
S =[0,0,0,0]
C = [0,0,0,0]
M = [0,0,0,0]
D = [0,0,0,0]
Finances = {'S':S,'C':C,'M':M,'D':D}
while True:
    temp = show_getF()
    if temp == 'Q':
        break
    elif temp in 'SCMD':
        t = show_get() - 1
        if temp == 'S':
            S[t] = int(raw_input('Please enter a num:\n'))
        elif temp == 'C':
            C[t] = int(raw_input('Please enter a num:\n'))
        elif temp == 'M':
            M[t] = int(raw_input('Please enter a num:\n'))
        elif temp == 'D':
            D[t] = int(raw_input('Please enter a num:\n'))
    else:
        print 'Invalid input,try again'

f = open('Finance','w+')
for i in Finances:
    f.write(i)
    f.write(str(Finances[i]))
    f.write('\n')
f.close()