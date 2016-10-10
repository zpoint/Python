time = 0
F = open(raw_input('Please enter a filename:\n'))
N = int(raw_input('And a number N:(I will print the Nth lines of the file for you):\n'))
for eachline in F:
    time += 1
    if time == N:
        print eachline,
F.close()