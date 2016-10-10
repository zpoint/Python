from socket import *
BUFSIZ = 1024
ADDR = ('localhost',20000)
UdpCliSock = socket(AF_INET,SOCK_DGRAM)
while True:
    data = raw_input('>')
    UdpCliSock.sendto(data,ADDR)
    data,addr = UdpCliSock.recvfrom(1024)
    if not data:
        break
    print 'ADDR:',ADDR,addr
    print data
UdpCliSock.close()