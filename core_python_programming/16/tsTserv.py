def getHostPort(HOST = '',PORT = 21567):
    temp = raw_input('Enter a HOST name(Empty to set default: \'%s\')'%HOST)
    if temp != '':
        HOST = temp
    temp = raw_input('Enter a PORT(Empty to set deafult: %d)'%PORT)
    while temp != '':
        try:
            int(temp)
            PORT = temp
            break
        except BaseException,reason:
            print 'Sorry,you should enter number such as 21567\nReason:',reason
            temp = raw_input('Enter a PORT(Empty to set deafult)')
    return HOST,PORT
from socket import *
from time import ctime
ADDR = getHostPort()
BUFSIZ = 1024
tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
while True:
    print 'waiting for connection...'
    tcpCliSock,addr = tcpSerSock.accept()
    print 'connected from:',addr
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        tcpCliSock.send('[%s] %s'%(ctime(),data))
        print 'received:',data
    tcpCliSock.close()
    print 'tcpCliSock.close() exceute'
tcpSerSock.close()