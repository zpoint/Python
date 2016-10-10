import unittest
#command line:
#pip install nose
#nosetests unit_test.py

#line_profiler fix to add a no-op @profile decorator to the namespace while unit testing
if '__builtin__' not in dir() or not hasattr(__builtin__, 'profile'):
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
"""
#memory_profile fix to add no-op @profile decorator to the name space while unit testing
if 'profile' not in dir():
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
"""
@profile
def some_fn(nbr):
    return nbr * 2

class TestCase(unittest.TestCase):
    def test(self):
        result = some_fn(2)
        self.assertEqual(result, 4) 
		
a = TestCase()
a.test()