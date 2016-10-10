f = open(raw_input('Please enter a filename,I will display the text file 25 lines at a time:\n'))
lines = 0
for eachline in f:
    lines += 1
    print eachline,
    if lines % 25 == 0:
        print '25 lines,press [Enter] to continue'
        raw_input()
f.close()