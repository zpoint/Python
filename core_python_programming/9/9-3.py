f = open(raw_input('Please enter a filename,I will count the total lines in the file:\n'))
lines = 0
for eachline in f:
    lines += 1
f.close()
print 'There are %d lines in total!' %lines