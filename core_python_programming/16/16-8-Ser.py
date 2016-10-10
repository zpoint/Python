from socket import *
import threading
def recv(TcpCliSock,addr):
    while True:
        data = TcpCliSock.recv(BUFSIZ)
        if not data:
            print 'No reply!'
            break
        print addr,'> ',data
def send(TcpCliSock):
    while True:
        data = raw_input('> ')
        if not data:
            print 'Invalid input!'
            break
        TcpCliSock.send(data)
        print 'you >',data
threads = []
HOST = ''
PORT = 20000
BUFSIZ = 1024
ADDR = (HOST,PORT)
TcpSerSock = socket(AF_INET,SOCK_STREAM)
TcpSerSock.bind(ADDR)
TcpSerSock.listen(5)
while True:
    print 'waiting for connection...'
    TcpCliSock,addr = TcpSerSock.accept()
    print 'connected from',addr
    print 'Full Duplex chat room,enjoy it! (Services)'
    t1 = threading.Thread(target = recv,args = (TcpCliSock,addr),name = recv.__name__)
    t2 = threading.Thread(target = send,args = (TcpCliSock,),name = send.__name__)
    threads.append(t1)
    threads.append(t2)
    for i in range(2):
        threads[i].start()
    for i in range(2):
        threads[i].join()
    TcpCliSock.close()
TcpSerSock.close()
        