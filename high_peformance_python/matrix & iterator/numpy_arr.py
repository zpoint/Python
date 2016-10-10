from array import array
import numpy

vector = [i for i in range(1000000)]
vector_arr = array('l', vector)
vector_numpy = numpy.arange(1000000)
print (vector_numpy)

def norm_square_list(vector):
    norm = 0
    for v in vector:
        norm += v * v
    return norm

def norm_square_list_comprehension(vector):
    return sum([v * v for v in vector])

def norm_squared_generator_comperhension(vector):
    return sum(v * v for v in vector)

def norm_square_array(vector_arr):
    norm = 0
    for v in vector:
        norm += v * v
    return norm

def norm_square_numpy(vector_numpy):
    return numpy.sum(vector_numpy * vector_numpy)

def norm_square_numpy_dot(vector_numpy):
    return numpy.dot(vector_numpy, vector_numpy)

"""
In [2]: %timeit norm_square_list(vector)
10 loops, best of 3: 83.9 ms per loop

In [3]: %timeit norm_square_list_comprehension(vector)
10 loops, best of 3: 74.4 ms per loop

In [4]: %timeit norm_squared_generator_comperhension(vector)
10 loops, best of 3: 83.5 ms per loop #suppose to be faster than [3]

In [5]: %timeit norm_square_array(vector_arr)
10 loops, best of 3: 75.8 ms per loop

In [6]: %timeit norm_square_numpy(vector_numpy)
100 loops, best of 3: 3.11 ms per loop

In [7]: %timeit norm_square_numpy_dot(vector_numpy)
1000 loops, best of 3: 862 µs per loop

In [8]: %timeit norm_squared_generator_comperhension(vector)
10 loops, best of 3: 83.4 ms per loop
"""
