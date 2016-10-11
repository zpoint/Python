import urllib.request
import ssl
import random
import time
ssl._create_default_https_context = ssl._create_unverified_context
t1 = time.time()
for i in range(1000):
    response = urllib.request.urlopen("https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&" + str(random.random()))
    im = response.read()
    f = open("12306/i2/%d.jpg" % i, "wb")
    f.write(im)
    f.close()
    if i % 10 == 0:
        print("%d done" % i)

t2 = time.time()
print("cost " + str(t2 - t1) + " seconds")
