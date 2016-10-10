f1 = open(raw_input('Input a filename,I will make sure 80 characters a line'))
f2 = open('new','w')
for eachline in f1:
    while len(eachline) > 80:
        i = 79
        while eachline[i] != ' ':
            i -= 1
        f2.write(eachline[:i])
        f2.write('\n')
        eachline = eachline[i+1:]
    else:
        f2.write(eachline)
f1.close()
f2.close()