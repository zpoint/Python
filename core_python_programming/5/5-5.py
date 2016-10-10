 #25 cents per quarter
 # 10 cents per dime
 # 5 cents per nickel
 # 1 cents per penny
money = 100 * float(raw_input('Please enter a number less than one\n'))
q = divmod(money,25)
d = divmod(q[1],10)
n = divmod(d[1],5)
print '$',money / 100,'is',
if q[0] != 0:
    print int(q[0]),'quarters',
if (d[0] != 0):
    print int(d[0]),'cents',
if(n[0] != 0):
    print int(n[0]),'nickels',
if(n[1] != 0):
    print int(n[1]),'penny'