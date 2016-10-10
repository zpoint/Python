pureprice = float(raw_input('Please enter your pureprice:\n'))
print 'You should pay:'
print 'subtotal %10.2f' %(pureprice)
print 'Tax: %10.2f' %(round(pureprice * 0.11,2))
print 'In total %10.2f' %(pureprice + round(pureprice * 0.11,2))