def set_pri(A,B):
    import random
    for i in range(random.randint(1,10)):
        A.add(random.randint(0,9))
        len = random.randint(1,10)
    for i in range(random.randint(1,10)):
        B.add(random.randint(0,9))
    print 'A is',A
    print 'B is',B

def get_ans(ans,str):
    ans.clear()
    answer = raw_input('Please enter your answer to %s:(seperated by comma)\nYou have three choices in total\n' %(str)).split(',')
    for i in range(len(answer)):
        answer[i] = int(answer[i])
    ans.update(answer)

def check_ans(setdef,str):
    ans = set()
    times = 1
    match = False
    while times <= 3 and not match:
        print 'the %d times' %(times)
        get_ans(ans,str)
        times += 1
        if ans == setdef:
            print 'Wow , correct answer!'
            match = True
            break
        else:
            if times < 4:
                print 'Sorry try again!'
    if times == 4 and not match:
        print 'Sorry, you tried three times'
        print 'No more chances'
        print 'The correct answer is',setdef
#**************************************************************#
A = set()
B = set()
set_pri(A,B)
check_ans(A | B,'A | B')
check_ans(A & B,'A & B')