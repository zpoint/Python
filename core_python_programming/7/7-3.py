#a
#b
my_dict = {'a':1,'b':2,'c':3,'d':4}
print my_dict.keys()
print my_dict.values()
print sorted(my_dict.keys())
#c
my_dict = {'a':4,'b':3,'c':1,'d':2}
print sorted(my_dict.iteritems(),key = lambda a:a[1])
print my_dict