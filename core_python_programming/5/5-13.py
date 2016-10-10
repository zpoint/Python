def convertion(a,b):
    return a*60 + b
time = raw_input('Please enter a time:(i.e 2:18)\n')
t = time.split(':')
print 'The total minutes is %g' %(convertion(float(t[0]),float(t[1])))