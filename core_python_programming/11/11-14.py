def Fibonacci(n):
    if n == 1 or n == 2:
        return n
    else:
        return Fibonacci(n-1) + Fibonacci(n-2)
