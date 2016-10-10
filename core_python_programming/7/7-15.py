def get_set(A,B):
    a1 = raw_input('Please enter set A:(seprated by colum)\n').split(',')
    b1 = raw_input('Please enter set B:(seprated by colum)\n').split(',')
    A.update(a1)
    B.update(b1)
    print 'SET A:',A
    print 'SET B:',B

def show_menu():
    print """
    (a) A in B
    (b) A not in B
    (c) A & B
    (d) A | B
    (e) A ^ B
    (f) A < B
    (g) A <= B
    (h) A > B
    (i) A >= B
    (j) A == B
    (k) A != B
    (r) reset A and B
    (q) quit
    """

def show_result(choice,A,B):
    if choice == 'R':
        get_set(A,B)
    elif choice in 'AB':
        print choice
        print 'in AB'
        if A in B:
            print 'A in B is correct'
        else:
            print 'A not in B is correct'
    elif choice == 'C':
        print 'A & B is',A & B
    elif choice == 'D':
        print 'A | B is',A | B
    elif choice == 'E':
        print 'A ^ B is',A ^ B
    elif choice in 'FG':
        if A <= B:
            if A != B:
                print 'A < B is correct!'
            else:
                print 'A <= B is correct!'
        else:
            print 'A <= B or A < B is not correct!'    
    elif choice in 'HI':
        if A >= B:
            if A != B:
                print 'A > B is correct!'
            else:
                print 'A >= B is correct!'
        else:
            print 'A >= B or A > B is not correct!'
    elif choice in 'JK':
        if A == B:
            print 'Yes, A equals B'
        else:
            print 'A not euqals B'
def get_choice():
    choice = raw_input('Please enter your choice:\n')[0].upper()
    if choice not in 'ABCDEFGHIJKR':
        choice = "Q"
        print 'Bye!'
    return choice
#*************************************************************
A = set()
B = set()
get_set(A,B)
show_menu()
choice = get_choice()
while choice != "Q":
    show_result(choice,A,B)
    choice = get_choice()