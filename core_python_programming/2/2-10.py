i = 0.0
i = float(raw_input('Please enter a number between 1 and 100\n'))
while i > 100 or i < 0:
    i = float(raw_input('Please make sure you enter a number between 1 and 100\n'))
print 'you enter %g\n' %(i)