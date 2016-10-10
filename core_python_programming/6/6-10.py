str = raw_input('Please input a string, I will \'case inverted\' it\n')
str2 = ''
for i in str:
    if i.isupper():
        str2 += i.lower()
    elif i.islower():
        str2 += i.upper()
    else:
        str2 += i
print str2