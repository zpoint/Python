year = int(raw_input('Please enter a year:\n'))
#normal year
if year < 172800:
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        print 'leap year'
#large yaer
elif year >= 172800:
    if year % 3200 == 0 and year % 172800 == 0:
        print 'leap year'
else:
    print 'normal year'