def show_menu():
    print """
(a) add
(u) update
(d) delete
(e) search
(q) Store and Quit"""
def getURL():
    return raw_input('Please enter a site name, Web site URL address, a one-line description(optional)\n').split(',')
URL ={}
f = open('Website.txt','r')
for eachline in f:
    eachline=eachline.strip('\n')
    tp = eachline.split('  ')
    URL[int(tp[0])] = tp[1].split(',')
f.close()
while True:
    show_menu()
    temp = raw_input()[0].upper()
    if temp == 'Q':
        break
    elif temp == 'A':
        URL[len(URL)] = getURL()
    elif temp == 'U':
        for i in URL:
            print i+1
            print URL[i]
        i = int(raw_input('Please enter your choice(number): '))
        URL[i-1] = getURL()
    elif temp == 'D':
        for i in URL:
            print i+1
            print URL[i]
        i = int(raw_input('Please enter your choice(number): '))
        del URL[i-1]
    elif temp == 'E':
        key = raw_input('Please enter a name or URL to search\n').upper()
        times = 0
        l = len(URL)
        for i in list(URL.itervalues()):
            times += 1
            if i[0].upper().find(key) >= 0 or i[1].upper().find(key) >= 0:
                print str(i)
                break
            if times == l:
                print 'Sorry,No match!'
f = open('Website.txt','w')
count = 0
for i in URL:
    f.write(str(i))
    f.write('  ')
    ll = len(URL[i])
    for j in URL[i]:
        count += 1
        f.write(j)
        if count != ll:
            f.write(',')
            count = 0
    f.write('\n')
f.close()