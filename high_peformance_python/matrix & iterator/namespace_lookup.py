import math 
from math import sin
def test1(x):
	"""
	>>> %timeit test1(123456)
	"""
	return math.sin(x)

def test2(x):
	#same timeit usage
	return sin(x)

def test3(x, sin=math.sin):
	return sin(x)

"""
import dis
dis.dis(test1)
dis.dis(test2)
dis.dis(test3)

In [9]: dis.dis(test1)
  7           0 LOAD_GLOBAL              0 (math)
              3 LOAD_ATTR                1 (sin)
              6 LOAD_FAST                0 (x)
              9 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             12 RETURN_VALUE

In [10]: dis.dis(test2)
 11           0 LOAD_GLOBAL              0 (sin)
              3 LOAD_FAST                0 (x)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 RETURN_VALUE

In [11]: dis.dis(test3)
 14           0 LOAD_FAST                1 (sin)
              3 LOAD_FAST                0 (x)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 RETURN_VALUE

"""

def tight_loop_slow(iterations):
	#timeit tight_loop_slow(10000000)
	#1 loop, best of 3: 2.46 s per loop
	result = 0
	for i in range(iterations):
		result += sin(i) #this call to sin requires a global lookup

def tight_loop_fast(iterations):
	#timeit tight_loop_fast(10000000)
	#1 loop, best of 3: 2.4 s per loop
	result = 0
	local_sin = sin
	for i in range(iterations):
		result += local_sin(i)
