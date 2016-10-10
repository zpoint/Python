from socket import *
from time import ctime
HOST = ''
PORT = 20000
BUFSIZ = 1024
ADDR = (HOST,PORT)
UdpSerSock = socket(AF_INET,SOCK_DGRAM)
UdpSerSock.bind(ADDR)
while True:
    print 'waiting for message...'
    data,addr = UdpSerSock.recvfrom(BUFSIZ)
    UdpSerSock.sendto('[%s] %s'%(ctime(),data),addr)
    print 'receive',data,'from',addr,'and send back!'
UdpSerSock.close()