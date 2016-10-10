A = set()
B = set()
import random
for i in range(random.randint(1,10)):
    A.add(random.randint(0,9))
len = random.randint(1,10)
for i in range(random.randint(1,10)):
    B.add(random.randint(0,9))
print 'A is',A
print 'B is',B
print 'A | B is',A | B
print 'A & B is',A & B
print 'A ^ B is',A ^ B
print 'A - B is',A - B