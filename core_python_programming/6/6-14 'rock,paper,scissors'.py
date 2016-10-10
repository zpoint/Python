def showmenu():
    print '(1) Paper'
    print '(2) Rock'
    print '(3) Scissor'
def cmp(p1,p2):
    if p1 == p2:
        return 0
    else:
        if p1 - p2 == 2 or p1 - p2 == -1:
            return 1
        else:
            return -1
showmenu()
# p1 > comp : 2>1(p2 win) 3>2(comp win) 3>1(p1 win)
#p1 <comp: 1<2(p1 win) 1<3(p2 win) 2<3(p1 win)
#pq = p2 same
p1 = int(raw_input('Player 1 Enter you choice:\n')[0])
import random
computer = random.randint(1,3)
CMD = {1:'Paper',2:'Rock',3:'Scissor'}
result = cmp(p1,computer)
print 'p1:',CMD[p1]
print 'computer:',CMD[computer]
if result == 0:
    print 'They are the same'
elif result == 1:
    print 'You win'
else:
    print 'Computer win'
