"""
from ctype import Structure
class cPoint(Structure):
    _fields_ = ("x", c_int), ("y", c_int)
"""
import ctypes

grid_shape = (512, 512)
_diffusion = ctypes.CDLL("../diffusion.so")

#Create references to the C types that we will need to simplify future code
TYPE_INT = ctypes.c_int
TYPE_DOUBLE = ctypes.c_double
TYPE_DOUBLE_SS = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

#Initialize the signature of the evolve function to:
#void evolve(int, int, double **, double **, double, double)
_diffusion.evolve.argtypes = [
    TYPE_INT,
    TYPE_INT,
    TYPE_DOUBLE_SS,
    TYPE_DOUBLE_SS,
    TYPE_DOUBLE,
    TYPE_DOUBLE
]
_diffusion.evolve.restype = None

def evolve(grid, out, dt, D = 1.0):
    #First we convert the Python types into the relevant C types
    cX = TYPE_INT(grid_shape[0])
    cY = TYPE_INT(grid_shape[1])
    cdt = TYPE_DOUBLE(dt)
    cD = TYPE_DOUBLE(D)
    pointer_grid = grid.ctypes.data_as(TYPE_DOUBLE_SS)
    pointer_out = out.ctypes.data_as(TYPE_DOUBLE_SS)

    #Now, we can call the function
    _diffusion.evolve(cX, cY, pointer_grid, pointer_out, cD, cdt)
