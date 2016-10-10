name = raw_input('Enter a filename,I could accsee it:\n')
f = open(name)
f2 = open('a','w')
i = 0
for eachline in f:
    i += 1
    print i,eachline.strip()
editline = int(raw_input('Please enter the lines you want to edit\n'))
f.seek(0)
i = 0
for eachline in f:
    i += 1
    if i == editline:
        eachline = raw_input('Please input:') + '\n'
    f2.write(eachline)
f.close()
f2.close()
import os
os.remove(name)
os.rename('a',name)