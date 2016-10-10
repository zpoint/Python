byte = raw_input('Please enter a byte value(0-255):\n')
f = open(raw_input('Please enter a filename:(I will search the times that byte appears in the file)'))
t = 0
for eachline in f:
    find = eachline.find(byte)
    if find >= 0:
        t += 1
f.close()
print byte,'appears %d times\n' %t