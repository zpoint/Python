###Credit statistic tools

- - -


* [Update](#update-2.02)
* [Installation](#installation)
	* [Environment](#----environment)
	* [run](#----run-szx.py,-you-need-to)
    * [hint](#----hint)
* [How it works?](#how-it-works)
* [Screenshots](#screenshots)

- - -




### Screenshots

![image](https://github.com/zpoint/Python/blob/master/szx_tool/Screenshots/a.png)

![image](https://github.com/zpoint/Python/blob/master/szx_tool/Screenshots/b.png)

![image](https://github.com/zpoint/Python/blob/master/szx_tool/Screenshots/c.png)

- - -


### Update 2.02
1. cache contents, Make user feel faster
2. more dialogs
3. help message

- - -


### Installation

- - -

#### ----Environment
1. PyQt5 (QT5 required)
2. matplotlib, MySQL-client module
3. Chinese font in your system

- - -

#### ----Run szx.py, you need to
1. write regular expression yourself.
2. modify the server address.

		Python3 szx.py

- - -

#### ----hint

1.The string you catch from wsgi, use

        str.encode('iso-8859-1').decode('utf8')

to get chinese character. You don't need a php page to store content in a txt file, and read it back in wsgi. It waste time.

* * *

### How it works
1. Use urllib to gain plain text imformation from the school lan network.
2. Parse imformation with regular expression.
3. POST the imformation to server.
3. I use **Apache2 mode-wsgi** to support python server, server store imformation in MySQL and generate images.
4. Server POST imformation and images address to client, client display it with PyQT5.
