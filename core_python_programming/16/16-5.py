from socket import *
import time
import os
def command(input):
    input = input.strip().upper()
    if input == 'DATA':
        return time.ctime(time.time())
    elif input == 'OS':
        return os.name
    elif input == 'LS':
        return os.getcwd()
    elif input == 'LSDIR':
        return str(os.listdir(os.getcwd()))
    else:
        return 'Sorry,Invalid Input!'
def getHostPort(Host = '',Port = 21500):
    temp = raw_input('Please enter a Host(Empty to set default: \'%s\')'%Host)
    HOST = temp
    temp = raw_input('Please enter port:(Empty to set default: %d)'%Port)
    while temp != '':
        try:
            Port = int(temp)
            break
        except BaseException as reasons:
            print 'Please enter Port such as 21500\nReason:',reasons
            temp = raw_input('Please enter port:(Empty to set default: %d)'%Port)
    return Host,Port
ADDR = getHostPort()
BUFSIZ = 1024
TcpSerSock = socket(AF_INET,SOCK_STREAM)
TcpSerSock.bind(ADDR)
TcpSerSock.listen(5)
while True:
    print 'waiting for connection...'
    TcpCliSock,addr = TcpSerSock.accept()
    print 'connected from :',addr
    while True:
        TcpCliSock.send("""
        please imput your command:
        data : I will return my current time
        os : you will get OS info
        ls : Give the list of the current directory
        lsdir : list a directory
        """)
        data = TcpCliSock.recv(BUFSIZ)
        if not data:
            print 'No data received'
            break
        TcpCliSock.send(command(data))
    TcpCliSock.close()
TcpSerSock.close()
        

