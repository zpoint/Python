import time
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -.42193

def calc_pure_python(desired_with, max_iterations):
    x_step = (float(x2 - x1) / float(desired_with))
    y_step = (float(y1 - y2) / float(desired_with))
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
    
    print ("Length of x:", len(x))
    print ("Total elements:", len(zs))
    start_time = time.time()
    output = calculate_z_serial_purepython(max_iterations, zs, cs)
    end_tine = time.time()
    secs = end_tine - start_time
    print (calculate_z_serial_purepython.__name__ + " took", secs, "seconds")
    assert sum(output) == 33219980
    """
    print ("x_step",x_step)
    print ("y_step",y_step)
    print ("x:",x)
    print ("y", y)
    print ("ZS:",zs)
    print ("CS:",cs)
    """
@profile
def calculate_z_serial_purepython(maxiter, zs, cs):
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while True:
            not_yet_escape = abs(z) < 2
            iterations_left = n < maxiter
            if not_yet_escape and iterations_left:
                z = z * z + c
                n += 1
            else:
                break
        output[i] = n
    return output
if __name__ == "__main__":
    calc_pure_python(desired_with = 1000, max_iterations = 300)