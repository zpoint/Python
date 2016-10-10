byte = raw_input('Please enter a byte value(0-255):\n')
times = int(raw_input('The number of times byte should appear in the data file\n'))
total = int(raw_input('The total number of bytes that make up the data file\n'))
f = open('1.txt','wb')
import random
ran = []
for i in range(times):
    ran.append(random.randint(0,total))
for i in range(total):
    if i in ran:
        f.write(byte)
    else:
        f.write(chr(random.randint(0,255)))
f.close()
