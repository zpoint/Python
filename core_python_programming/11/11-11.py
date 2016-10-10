def choose():
    print 'Enter your choice:'
    print '(a) Creating a new file\n(b) Over writing the existing one'
    return raw_input()[0].upper

def Processline(eachline):
    lineend = 0
    linestart = 0
    while eachline[len(eachline) - 1 - lineend] == ' ' or eachline[len(eachline) - 1 - lineend] == '\n':
        lineend += 1
    while eachline[linestart] == ' ' or eachline[linestart] == '\n':
        linestart += 1
    return eachline[linestart:len(eachline) - lineend]

fn = raw_input('Please enter a filename to process')
f = open(fn)
newlines = map(Processline,f)
print newlines
f.close()


while True:
    choose = choose()
    if choose == 'A':
        f = open('newfile','w')
        break
    elif choose == 'B':
        f = open(fn,'w')
        break

for eachline in newlines:
    f.write(eachline + '\n')
f.close()