date1 = (raw_input('Please input a data in MM/DD/YY (i.e. 5/25/2015)\n').split('/'))
date2 = (raw_input('Please input another data in MM/DD/YY (i.e. 5/25/2015)\n').split('/'))
for i in range(3):
    date1[i] = int(date1[i])
    date2[i] = int(date2[i])
import datetime
d1 = datetime.date(date1[2],date1[0],date1[1])
d2 = datetime.date(date2[2],date2[0],date2[1])
print (d2-d1).days

#b
birthday = raw_input('Please enter your birthday DD/MM/YY i.e.\n').split('/')
for i in range(3):
    birthday[i] = int(birthday[i])
import datetime
birthday = datetime.date(birthday[2],birthday[1],birthday[0])
print (datetime.date.today() - birthday).days

#c
birthday = raw_input('Please enter your birthday DD/MM/YY i.e.\n').split('/')
for i in range(3):
    birthday[i] = int(birthday[i])
import datetime
import time
bir = datetime.date(birthday[2],birthday[1],birthday[0])
next_year = int(time.strftime('%Y',time.localtime(time.time()))) + 1
birthday_next = datetime.date(next_year,birthday[1],birthday[0])
print 'you lived',(datetime.date.today() - bir).days,'days'
print 'Next birthday remains',(birthday_next - datetime.date.today()).days,'days'