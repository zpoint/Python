import threading
from socket import *
def send(TcpCliSock):
    while True:
        data = raw_input('> ')
        if not data:
            print 'You input nothing!'
            break
        TcpCliSock.send(data)
        print 'you >',data
def recv(TcpCliSock):
    while True:
        data = TcpCliSock.recv(BUFSIZ)
        if not data:
            print 'No reply!'
            break
        print 'Ser >',data
nloops = [send,recv]
threads = []
HOST = 'localhost'
PORT = 20000
BUFSIZ = 1024
ADDR = (HOST,PORT)
TcpCliSock = socket(AF_INET,SOCK_STREAM)
TcpCliSock.connect(ADDR)
print 'Full Duplex chat room,enjoy it! (Client)'
for i in nloops:
    t = threading.Thread(target = i,args = (TcpCliSock,),name = i.__name__)
    threads.append(t)
for i in range(len(threads)):
    threads[i].start()
for i in range(len(threads)):
    threads[i].join()
TcpCliSock.close()