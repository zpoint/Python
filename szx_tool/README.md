###Credit statistic tools
####Update 2.02
1. cache contents, Make user feel faster
2. more dialogs
3. help message

####Environment:
1. PyQt5 (QT5 required)
2. matplotlib, MySQL-client module
3. Chinese font in your system

#### Client follows the step:
1. Use urllib to gain plain text imformation from the school lan network.
2. Parse imformation with regular expression.
3. POST the imformation to server.
3. I use **Apache2 mode-wsgi** to support python server, server store imformation in MySQL and generate images.
4. Server POST imformation and images address to client, client display it with PyQT5.

####Run szx.py, you need to:
1. write regular expression yourself.
2. modify the server address.

- - -
####Screenshots:

![image](https://github.com/zpoint/Python/blob/master/szx_tool/Screenshots/a.png)

![image](https://github.com/zpoint/Python/blob/master/szx_tool/Screenshots/b.png)

![image](https://github.com/zpoint/Python/blob/master/szx_tool/Screenshots/c.png)



####hint

1.The string you catch from wsgi, use 
		
        str.encode('iso-8859-1').decode('utf8')

to get chinese character. You don't need a php page to store content in a txt file, and read it back in wsgi. It waste time.

