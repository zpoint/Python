d1 = {1,2,3,4}
d2 = {'abc','def','ghi','jkl'}
k = zip(d1,sorted(d2))
dic = {}
for i in range(len(k)):
    dic.update({k[i][0]:k[i][1]})
print dic