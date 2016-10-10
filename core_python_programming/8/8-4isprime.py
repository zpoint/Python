import math
def isprime(num):
    count = int(math.sqrt(num))
    while count > 1:
        if num % count == 0:
            return False
        count -= 1
    else:
        return True

if isprime(int(raw_input('Enter a number to determine whether it\'s prime:'))):
    print 'TRUE'
else:
    print 'False'
