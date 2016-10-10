def Factorial(num):
    N = 1
    for i in range(1,num+1):
        N *= i
    return N

print Factorial(int(raw_input('Please enter a number to N!:\n')))