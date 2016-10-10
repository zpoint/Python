def Fibonacci(num):
    alist = []
    for i in range(num):
        if i == 0 or i == 1:
            alist.append(1)
        else:
            alist.append(alist[i-1] + alist[i-2])
    return alist 

print Fibonacci(int(raw_input('Please enter a number to Fibonacci\n')))