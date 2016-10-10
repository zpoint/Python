exp = sys.argv[1]
def verify(a):
    try:
        float(a)
        return True
    except ValueError:
        print 'You input an illegal expression. "%s" is not a number.' % (a)
        return False
if len(exp.split('+')) == 2:
    if verify(exp.split('+')[0]) and verify(exp.split('+')[1]):
        print '= %f' %((float(exp.split('+')[0])) + float(exp.split('+')[1]))
        pass
elif len(exp.split('-')) == 2:
    if verify(exp.split('-')[0]) and verify(exp.split('-')[1]):
        print '= %f' %(float(exp.split('-')[0]) - float(exp.split('-')[1]) )
        pass
elif len(exp.split('*')) == 2:
    if verify(exp.split('*')[0]) and verify(exp.split('*')[1]):
        print '= %f' %((float(exp.split('*')[0])) * float(exp.split('*')[1]))
        pass
elif len(exp.split('/')) == 2:
    if verify(exp.split('/')[0]) and verify(exp.split('/')[1]):
        print '= %f' %((float(exp.split('/')[0])) / float(exp.split('/')[1]))
        pass
elif len(exp.split('**')) == 2:
    if verify(exp.split('**')[0]) and verify(exp.split('**')[1]):
        print '= %f' %((float(exp.split('**')[0])) ** float(exp.split('**')[1]))
        pass