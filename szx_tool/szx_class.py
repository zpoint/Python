import urllib.request
import urllib.parse
import http.cookiejar
import random
import re
import base64

class szx_edu_grade(object):
    def __init__(self):
        self.cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))

    def setproxy(self, proxyurl, card_num, pwd):
        proxy_handler = urllib.request.ProxyHandler({'http': proxyurl, 'https': proxyurl})
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        proxy_auth_handler = urllib.request.ProxyBasicAuthHandler(password_mgr)
        proxy_auth_handler.add_password(None, proxyurl, card_num, pwd)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie), proxy_handler, proxy_auth_handler)

    def unset_proxy(self):
        self.__init__()

    def init_user_pwd(self, userid, password, code):
        self.userid = str(userid)
        self.password = str(password)
        self.code = str(code)
        

    def getcode(self):
        try:
            self.opener.open('http://192.168.2.20/') 
        except urllib.error.HTTPError as e:
            return (2, 'HTTPError')
        except urllib.error.URLError as e:
            return (3, 'URLError')

        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', '	keep-alive'),
                                  ('Host', '192.168.2.20'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]
        response = self.opener.open('http://192.168.2.20/mycode/code.asp?id=!!!&random=' + str(random.random()))
        jpg = response.read()
        return jpg

    def login(self):
        "return True if success in logging in, False if not"

        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', 'keep-alive'),
                                  ('Host', '192.168.2.20'),
                                  ('Referer', 'http://192.168.2.20/disp.aspx?url=axsxx/AASZUstd.ASP'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]
        value = {'GetCode':self.code,
                 'PASSWORD':self.password,
                 'USERID': self.userid}

        url = 'http://192.168.2.20/axsxx/AALICENSEstd.asp'
        data = urllib.parse.urlencode(value)
        data = data.encode('ascii')
        response = self.opener.open(url, data = data)
        response_header = response.getheaders()
        for i,j in response_header:
            if i == 'Content-Length':
                if j == '50':
                    return True
                else:
                    return False

    def get_mainmessage(self):
        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', '	keep-alive'),
                                  ('Host', '192.168.2.20'),
                                  ('Referer', 'http://192.168.2.20/AXSXX/xjxxcheck.aspx'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]
        value = {'GetCode':self.code,
                 'PASSWORD':self.password,
                 'PMSFILEC':'AXSXX/aipconstd.asp',
                 'PMSFILEM':'AXSXX/xjxxcheck.asp',
                 'StuXjxxcheck':'1',
                 'USERID':'',
                 'cetlogflag':'True',
                 'level':'0',
                 'stulogflag':'True',
                 'useridSTD':self.userid,
                 'userpms':'S',
                 'userxhSTD':self.userid
                 }
        url = 'http://192.168.2.20/AXSXX/xjxxcheck.aspx'
        data = urllib.parse.urlencode(value)
        data = data.encode('ascii')
        response = self.opener.open(url, data = data)
        html = response.read()
        html = html.decode('gbk')
        pattern = re.compile('.+?lblXh">(.+?)<.+?lblXm">(.+?)<.+?lblXb">(.+?)<.+?lblCsrq">(.+?)<.+?lblSfzh">(.+?)<.+?lblMz">(.+?)<.+?lblNj">(.+?)<.+?lblXy">(.+?)<.+?lblZxzy">(.+?)<.+?lblBj">(.+?)<.+?lblKsh">(.+?)<.+?lblXmpy">(.+?)<.+?lblLxdh">(.+?)<.+?lblYzbm">(.+?)<.+?lblJtdz">(.+?)<.+?lblJzxm">(.+?)<.+?lblJtdh">(.+?)<', re.DOTALL)
        match = re.match(pattern, html)
        #0--->userid  1--->name 2--->sex 3--->birth 4--->ID 
        #5--->nation   6--->grade i.e. 2013  7-->学院  8--->major
        #9--->class   10--->exam_num   11--->en_name  12--->phone_num
        #13--->zip_code 14--->address 15--->conste 16--->password  17--->second_major

        message_list = []
        for i in range(15):
            message_list.append(match.group(i + 1).strip())
        message_list.append(self.get_conste(message_list[3]))
        message_list.append(self.password)
        message_list.append('0')
        return message_list

    def get_conste(self, birth_str):
        birth = birth_str[4:]
        birth = int(birth)
        if birth >= 321:
            if birth <= 419:
                return '白羊座'
            elif birth <= 520:
                return '金牛座'
            elif birth <= 621:
                return '双子座'
            elif birth <= 722:
                return '巨蟹座'
            elif birth <= 822:
                return '狮子座'
            elif birth <= 922:
                return '处女座'
            elif birth <= 1023:
                return '天秤座'
            elif birth <= 1122:
                return '天蝎座'
            elif birth <= 1221:
                return '射手座'
            else:
                return '摩羯座'
        elif birth >= 219:
            return '双鱼座'
        elif birth >= 120:
            return '水瓶座'
        else:
            return '摩羯座'



    def getphoto(self):
        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', '	keep-alive'),
                                  ('Host', '192.168.2.20'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')] 
        
        response = self.opener.open('http://192.168.2.20/ksb/NewCETSignup/getphoto.asp')
        for i in response.getheaders():
            if i[0] == 'Content-Length' and int(i[1]) == 0:
                return False

        jpg = response.read()
        return jpg

    def get_grade(self):
        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', '	keep-alive'),
                                  ('Host', '192.168.2.20'),
                                  ('Referer', 'http://192.168.2.20/AXSXX/aipconstd.asp'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]

        response = self.opener.open('http://192.168.2.20/AXSXX/aCHENGJISTD.asp')
        #check whether success
        if response.getcode() != 200:
            print('fail')
            return False
        html = response.read()
        html = html.decode('gbk')
        return html

    def get_current_lesson(self):
        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', '	keep-alive'),
                                  ('Host', '192.168.2.20'),
                                  ('Referer', 'http://192.168.2.20/AXSXX/aipconstd.asp'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]

        response = self.opener.open('http://192.168.2.20/AXSXX/axuankeSTD.asp')
        #check whether success
        if response.getcode() != 200:
            print('fail')
            return False
        html = response.read()
        html = html.decode('gbk')

class szx_edu_choose_class(object):
    def __init__(self, userid, password):
        self.userid = str(userid)
        self.password = str(password)
        self.cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))

    def login(self):
        self.opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding','gzip, deflate'),
                                  ('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection','keep-alive'),
                                  ('Host','192.168.240.168'),
                                  ('Referer','http://192.168.240.168/xuanke/edu_login.asp'),
                                  ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]
        url = 'http://192.168.240.168/xuanke/code.asp?id=!!!&random=' + str(random.random())
        jpg = self.opener.open(url).read()
        file = open('2.jpg', 'wb')
        file.write(jpg)
        file.close()

        url = 'http://192.168.240.168/xuanke/entrance1.asp'
        self.code = input('code')
        value = {'stu_no':self.userid,
                 'passwd':self.password,
                 'GetCode':self.code}
        data = urllib.parse.urlencode(value)
        data = data.encode('ascii')

        try:
            response = self.opener.open(url, data = data)
        except urllib.error.HTTPError as e:
            print(e)
            return False
        html = response.read()

#a.getphoto()
#urllib.request.urlopen('http://192.168.240.168/xuanke/entrance1.asp')

header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
          'Connection': 'keep-alive',
          'Host': '192.168.240.168',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
          'Cookie':'ASPSESSIONIDACQDTSQB=LBCEPMDAOCDJBIJNNGLFCLGG; F5-BIGIP-2000S=3455101120.20480.0000'}

value = {'GetCode':502,
                 'PASSWORD':'137138',
                 'PMSFILEC':'AXSXX/aipconstd.asp',
                 'PMSFILEM':'AXSXX/xjxxcheck.asp',
                 'StuXjxxcheck':'1',
                 'USERID':'',
                 'cetlogflag':'True',
                 'level':'0',
                 'stulogflag':'True',
                 'useridSTD':'2013140033',
                 'userpms':'S',
                 'userxhSTD':'2013140033'
                 }
"""
data = urllib.parse.urlencode(value)
data = data.encode('ascii')
req = urllib.request.Request('http://192.168.2.20/AXSXX/xjxxcheck.aspx', data = data, headers = header)
response = urllib.request.urlopen(req)
print('response header:')
for i in response.getheaders():
    print(i[0], ' : ', i[1])
"""