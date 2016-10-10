def listdisplay(List,N,F):
    hang = len(List) / N
    if F == 1:
        for i in range(len(List)):
            print List[i],
            if (i + 1) % hang == 0 and i / hang != N:
                print ''
    else:
        rest = List % N
        bList = []
        for i in range(N):
            for j in range(lang):
                bList.append(aList[i + j*N])
        for i in range(len(bList)):
            print bList[i]
            if (i + 1) % hang == 0:
                print ''
        for i in range(rest):
            print ''*N*2,List[len(List) - rest + i]
alist = list(raw_input('Please enter a list:\n'))
N = int(raw_input('How many rows/columns in display:\n'))
F = int(raw_input('(1)Horizontal or (2)Vertical:\n'))
listdisplay(alist,N,F)