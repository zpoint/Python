def GCD(a,b):
    if a < b:
        temp = a
        a = b
        b = temp
    r = a % b
    a = b
    b = r
    while r != 0:
        r = a % b
        a = b
        b = r
    return a
def LCM(a,b):
    return a * b / GCD(a,b)
a = int(raw_input('enter an interger\n'))
b = int(raw_input('Enter another:\n'))
print 'GCD is %g' %(GCD(a,b))
print 'LCM is %g' %(LCM(a,b))