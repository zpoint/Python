from cffi import FFI
grid_shape = (512, 512)
ffi = FFI()
ffi.cdef(r'''
        void evolve(
            int Nx, int Ny,
            double **in, double **out,
            double D, double dt);
        ''')
lib = ffi.dlopen("../diffusion.so")

def evolve(grid, dt, out, D = 1.0):
    X, Y = grid_shape
    pointer_grid = ffi.cast('double **', grid.ctypes.data)
    pointer_out = ffi.cast('double **', out.ctypes.data)
    lib.evolve(X, Y, pointer_grid, pointer_out)
