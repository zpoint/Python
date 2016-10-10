def timeit(fun,arg = None):
    'fun can take only single argunment'
    import time
    timestart = time.clock()
    fun(arg)
    return time.clock() - timestart

def fb(N):
    if N == 1 or N == 2:
        return 1
    else:
        return fb(N-1) + fb(N-2)

print timeit(fb,50)