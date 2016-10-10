#a
for i in range(0,22,2):
    print i
#b
for i in range(1,22,2):
    print i
def div(a,b):
    if a % b == 0:
        return True
    else:
        return False
a = float(raw_input('enter one number\n'))
b = float(raw_input('another\n'))
if div(a,b):
    print 'a divides b'
else:
    print 'a can\'t divide b'