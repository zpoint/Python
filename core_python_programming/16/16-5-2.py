from socket import *
ADDR = ('localhost',21500)
BUFSIZ = 1024
TcpCliSock = socket(AF_INET,SOCK_STREAM)
TcpCliSock.connect(ADDR)
while True:
    print TcpCliSock.recv(BUFSIZ)
    data = raw_input('>')
    if not data:
        break
    TcpCliSock.send(data)
    data = TcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print data
TcpCliSock.close()