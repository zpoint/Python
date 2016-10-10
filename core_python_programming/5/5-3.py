a = float(raw_input('Please enter a score:(0 - 100)\n'))
if a >= 90 and a <= 100:
    print 'The score is A'
elif a>= 80 and a <= 89:
    print 'The score is B'
elif a>= 70 and a <= 79:
    print 'The score is C'
elif a >= 60 and a <= 69:
    print 'The score is D'
elif a < 60 and a >= 0:
    print 'The score is E\nSorry,you failed'
else:
    print 'Not in range 0 - 100\nDone'