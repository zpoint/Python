dayrate = float(raw_input('Please enter dayInterstRate:\n'))
print 'Repay rate is %g' %((1.+ dayrate) ** 365 - 1)