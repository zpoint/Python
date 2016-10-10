#cython: boundscheck=False
#add line above in .pyx to
#disable bounds checking 

#in command line
#python3 setup.py build_ext --inplace
#inplace argument tells Cython to build the compiled module into current directory
#rather than into a separate build directory

#cython -a cythonfn.pyx
#generate a html file to view
import time
import calculate
import numpy
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -.42193

def calc_pure_python(desired_width, max_iterations):
    x_step = (float(x2 - x1) / float(desired_width))
    y_step = (float(y1 - y2) / float(desired_width))
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))
    #numpy change
    zs = numpy.array(zs)
    cs = numpy.array(cs)
    #change done
    print ("Length of x:", len(x))
    print ("Total elemrnt", len(zs))
    start_time = time.time()
    output = calculate.calculate_z(max_iterations, zs, cs)
    end_time = time.time()
    secs = end_time - start_time
    print ("Took", secs, "seconds")
    assert sum(output) == 33219980

if __name__ == "__main__":
    calc_pure_python(desired_width = 1000, max_iterations = 300)
