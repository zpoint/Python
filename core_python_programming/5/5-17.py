import random
bign = random.randint(2,100)
list = range(bign)
for i in range(bign):
    list[i] = random.randint(1,2**31 - 1)
print bign
print list
list.sort()
print list
