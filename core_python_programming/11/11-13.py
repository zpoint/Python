#a
def mult(x,y):
    return x * y
#b
print reduce(mult,(x + 1 for x in range(int(raw_input('Enter a number to factorials\n')))))
#c
print reduce(lambda x,y:x * y,(x + 1 for x in range(int(raw_input('Enter a number to factorials\n')))))
