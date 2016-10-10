input = int(raw_input('Please enter a number:\n'))
one2ten = [None,'one','two','three','four','five','six','seven','eight','night','ten']
ten2twenty = [None,'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
tens_units = [None,'ten','twenty','thiry','forty','fifty','sixty','seventy','eighty','ninety']
hundred = input / 100
ten = (input - hundred * 100) / 10
one = input - hundred * 100 - ten * 10
if hundred > 0:
    if hundred == 10:
        print 'one thousand',
    else:
        print '%s hundred' %(one2ten[hundred]),
if one == 0:
    if ten != 0:
        print 'and',tens_units[ten]
else:
    if hundred != 0:
        print 'and',
    if ten == 0:
        print  one2ten[one]
    elif ten == 1:
        print ten2twenty[one]
    else:
        print tens_units[ten],one2ten[one]