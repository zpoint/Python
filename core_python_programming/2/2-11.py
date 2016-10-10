def sumfive():
    total = 0
    for i in range(5):
        total += float(raw_input('Please enter a number\n'))
    print 'The sum is',total

def average_5():
    total = 0
    for i in range(5):
        total += float(raw_input('Please enter a number\n'))
    print 'The average is',total / 5

print 'Please select ... \n'
print '(1) To get the total of 5 numbers, please input letter "a" ... '
print '(2) To get the average of 5 numbers, please input letter "b" ... '
print '(x) To quit, please input letter "x" ... \n'
T = 1
choice = raw_input('Your choice is\n')
while T:
    if choice == 'a':
         sumfive()
    elif choice == 'b':
        average_5()
    elif choice == 'x':
        T = 1
        break
    else:
        print 'Please enter a,b,or c'
    print 'Please select ... \n'
    print '(1) To get the total of 5 numbers, please input letter "a" ... '
    print '(2) To get the average of 5 numbers, please input letter "b" ... '
    print '(x) To quit, please input letter "x" ... \n'
    choice = raw_input('Your choice is\n')