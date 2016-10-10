from socket import *
HOST = 'localhost'
PORT = 22222
BUFSIZ = 1024
ADDR = (HOST,PORT)
TcpCliSock = socket(AF_INET,SOCK_STREAM)
TcpCliSock.connect(ADDR)
print 'connected to',ADDR
while True:
    data = raw_input('(You)>')
    if not data:
        print 'You input nothing'
        break
    TcpCliSock.send(data)
    data = TcpCliSock.recv(BUFSIZ)
    if not data:
        print 'nothing received'
        break
    print ADDR,'>',data
TcpCliSock.close()