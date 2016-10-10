def get_name():
    total = int(raw_input('Enter total number of names:(should be \'Last Name,First Name\') '))
    namelis = []
    wrong = 0
    times = 0
    while times < total:
        nstr = raw_input('Please enter name %d: '%times)
        if len(nstr.split(',')) == 2:
            namelis.append(nstr)
        else:
            tempstr = ''
            for i in nstr.split():
                if i == 1:
                    tempstr += ', '
                else:
                    tempstr += i
            namelis.append(tempstr)
            wrong += 1
            print 'Wrong format... should be Last, Fisrt.'
            print 'You have done this %d times(s) already. Fixing input...' %wrong
        times += 1
    return namelis
 
al = sorted(get_name())
print 'The sorted list (by last name) is:'
for i in al:
    print i
