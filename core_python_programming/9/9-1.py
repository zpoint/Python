f = open(r'C:\Users\zpoint\Desktop\aa.txt')
for eachline in f:
    if eachline[0] != '#':
        print eachline,
f.close()

#Extra credit:
f = open(r'C:\Users\zpoint\Desktop\aa.txt')
for eachline in f:
    switch = True
    for i in eachline:
        if i == '#':
            switch = False
    if switch:
        print eachline,
f.close()