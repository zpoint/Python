from math import sqrt
def safe_sqrt():
    num = int(raw_input('Please enter a number I will tell you it\'s square root:'))
    try:
        return sqrt(num)
    except ValueError:
        return '+-' + str(sqrt(abs(num))) + 'j'
print safe_sqrt()