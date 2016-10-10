from random import normalvariate
from numpy.random import rand
from itertools import count, ifilter, imap

def read_data(filename):
	with open(filename) as fd:
		for line in fd:
			data = line.strip().split(',')
			yield map(int, data)

def read_fake_data(filename):
	for i in count():
		print ('i', i)
		print ('count', count)
		sigma = rand() * 10
		print ('sigma', sigma)
		yield (i, normalvariate(0, sigma))

f = [i for i in range(100)]
b = read_fake_data(f)
for i in range(10):
	print (b.__next__())

import math
def check_anomaly((day, day-data)):
	n = 0
	mean = 0
	M2 = 0
	max_value = None
	for timestamp, value in day_data:
		n += 1
		delta = value = mean
		mean = mean + delta / n
		M2 += delta * (value - mean)
		max_value = max(max_value, value)
	variance = M2 / (n - 1)
	standard_deviation = math.sqrt(variance)
	if max_value > mean + 3 * standard_deviation:
		return day
	return false

data = read_data(data_filename)
data_day = day_grouper(data)
anomalous_dates = ifilter(None, imap(check_anomaly, data_day))

first_anomalous_date, first_anomalous_data = anomalous_dates.__next__()
print ("The first anomalous date is: ", first_anomalous_date)
"""
how groupby work

https://docs.python.org/3.5/library/itertools.html?highlight=groupby#itertools.groupby
class groupby:
    # [k for k, g in groupby('AAAABBBCCDAABBB')] --> A B C D A B
    # [list(g) for k, g in groupby('AAAABBBCCD')] --> AAAA BBB CC D
    def __init__(self, iterable, key=None):
        if key is None:
            key = lambda x: x
        self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()
    def __iter__(self):
        return self
    def __next__(self):
        print ('currkey', self.currkey)
        print ('tgtkey', self.tgtkey)
        print ('currkey == tgtkey', self.currkey == self.tgtkey)
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)    # Exit on StopIteration
            print ('self.currvalue == next(self.it) = ', self.currvalue)
            self.currkey = self.keyfunc(self.currvalue)
            print ('self.currkey = self.keyfunc(self.currvalue) = ', self.currkey)
        print ('self.tgtkey = ', self.tgtkey)
        print ('self.currkey = ',self.currkey)
        self.tgtkey = self.currkey
        print ('self.tgtkey = self.currkey = ', self.currkey)
        ret = (self.currkey, self._grouper(self.tgtkey))
        print ('return (self.currkey, self._grouper(self.tgtkey)) ===>', ret)
        return ret
    def _grouper(self, tgtkey):
        while self.currkey == tgtkey:
            yield self.currvalue
            try:
                self.currvalue = next(self.it)
            except StopIteration:
                return
            self.currkey = self.keyfunc(self.currvalue)

a = groupby('AAAABBBCCDAABBB')
b = groupby('AAAABBBCCD')
"""

