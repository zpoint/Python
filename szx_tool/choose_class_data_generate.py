import urllib.request
import urllib.parse
import http.cookiejar
import random
import re
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
        file = open('C:/Users/sunset/Desktop/xuanke.jpg', 'wb')
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
        print (html)

    def menu(self):
       self.opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding','gzip, deflate'),
                                  ('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection','keep-alive'),
                                  ('Host','192.168.240.168'),
                                  ('Referer','http://192.168.240.168/xuanke/edu_main.asp?xq=20161'),
                                  ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]
        
       url = 'http://192.168.240.168/xuanke/coursehtm/dept20161.htm'
       response = self.opener.open(url)
       html = response.read().decode('gbk')
       file = open('C:/Users/sunset/Desktop/menu.html', 'w')
       file.write(html)
       file.close()

    def get_courses_info(self, url):
        self.opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding','gzip, deflate'),
                                  ('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection','keep-alive'),
                                  ('Host','192.168.240.168'),
                                  ('Referer','http://192.168.240.168/xuanke/coursehtm/dept20161.htm'),
                                  ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')]
        
        response = self.opener.open(url)
        html = response.read().decode('gbk')
        return html
href_list = [
              	['d120161', 'http://192.168.240.168/xuanke/coursehtm/d120161.htm', 'MOOC'], 
              	['d220161', 'http://192.168.240.168/xuanke/coursehtm/d220161.htm', '材料学院'], 
              	['d320161', 'http://192.168.240.168/xuanke/coursehtm/d320161.htm', '传播学院'], 
              	['d420161', 'http://192.168.240.168/xuanke/coursehtm/d420161.htm', '创业学院'], 
              	['d520161', 'http://192.168.240.168/xuanke/coursehtm/d520161.htm', '大学英语教学部'], 
              	['d620161', 'http://192.168.240.168/xuanke/coursehtm/d620161.htm', '电子科学与技术学院'], 
              	['d720161', 'http://192.168.240.168/xuanke/coursehtm/d720161.htm', '法学院'], 
              	['d820161', 'http://192.168.240.168/xuanke/coursehtm/d820161.htm', '港澳基本法研究中心'], 
              	['d920161', 'http://192.168.240.168/xuanke/coursehtm/d920161.htm', '高等研究院'], 
              	['d1020161', 'http://192.168.240.168/xuanke/coursehtm/d1020161.htm', '管理学院'], 
              	['d1120161', 'http://192.168.240.168/xuanke/coursehtm/d1120161.htm', '光电工程学院'], 
              	['d1220161', 'http://192.168.240.168/xuanke/coursehtm/d1220161.htm', '国际交流学院'], 
              	['d1320161', 'http://192.168.240.168/xuanke/coursehtm/d1320161.htm', '化学与环境工程学院'], 
              	['d1420161', 'http://192.168.240.168/xuanke/coursehtm/d1420161.htm', '机电与控制工程学院'], 
              	['d1520161', 'http://192.168.240.168/xuanke/coursehtm/d1520161.htm', '计算机与软件学院'], 
              	['d1620161', 'http://192.168.240.168/xuanke/coursehtm/d1620161.htm', '建筑与城市规划学院'], 
              	['d1720161', 'http://192.168.240.168/xuanke/coursehtm/d1720161.htm', '经济学院'], 
              	['d1820161', 'http://192.168.240.168/xuanke/coursehtm/d1820161.htm', '人文学院'], 
                ['d1920161', 'http://192.168.240.168/xuanke/coursehtm/d1920161.htm', '社会科学学院'], 
              	['d2020161', 'http://192.168.240.168/xuanke/coursehtm/d2020161.htm', '生命与海洋科学学院'], 
              	['d2120161', 'http://192.168.240.168/xuanke/coursehtm/d2120161.htm', '师范学院'], 
              	['d2220161', 'http://192.168.240.168/xuanke/coursehtm/d2220161.htm', '师范学院(高尔夫学院)'], 
              	['d2320161', 'http://192.168.240.168/xuanke/coursehtm/d2320161.htm', '数学与统计学院'], 
              	['d2420161', 'http://192.168.240.168/xuanke/coursehtm/d2420161.htm', '体育部'], 
              	['d2520161', 'http://192.168.240.168/xuanke/coursehtm/d2520161.htm', '图书馆'], 
              	['d2620161', 'http://192.168.240.168/xuanke/coursehtm/d2620161.htm', '土木工程学院'], 
              	['d2720161', 'http://192.168.240.168/xuanke/coursehtm/d2720161.htm', '外国语学院'], 
              	['d2820161', 'http://192.168.240.168/xuanke/coursehtm/d2820161.htm', '文化产业研究院'], 
              	['d2920161', 'http://192.168.240.168/xuanke/coursehtm/d2920161.htm', '武装部'], 
              	['d3020161', 'http://192.168.240.168/xuanke/coursehtm/d3020161.htm', '物理与能源学院'], 
              	['d3120161', 'http://192.168.240.168/xuanke/coursehtm/d3120161.htm', '心理与社会学院'], 
              	['d3220161', 'http://192.168.240.168/xuanke/coursehtm/d3220161.htm', '信息工程学院'], 
              	['d3320161', 'http://192.168.240.168/xuanke/coursehtm/d3320161.htm', '学生部'], 
              	['d3420161', 'http://192.168.240.168/xuanke/coursehtm/d3420161.htm', '医学院'], 
              	['d3520161', 'http://192.168.240.168/xuanke/coursehtm/d3520161.htm', '艺术设计学院'], 
              	['d3620161', 'http://192.168.240.168/xuanke/coursehtm/d3620161.htm', '招生就业办公室'], 
              	['d3720161', 'http://192.168.240.168/xuanke/coursehtm/d3720161.htm', '中国经济特区研究中心'], 
]

def get_courses_list(html, key):
    pattern = re.compile('.+?value="([0-9]+)+.+?href="(.+?)".+?new">(.*?)<.+?<td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>.+?\.\.(.+?)".+?<td>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>(.*?)<.+?</tr>(.+)', re.DOTALL)
    match = re.match(pattern, html)
    courses_lists = []
    while match != None:
        courses = []
        for i in range(12):
            if i == 7:
                courses.append('http://192.168.240.168' + '/xuanke' + match.group(i + 1).strip())
            else:
                courses.append(match.group(i + 1).strip())
        courses_lists.append(courses)
        match = re.match(pattern, match.group(13))

    file = open('C:/Users/sunset/Desktop/test.py', 'a+')
    s = '\t\t' + key + ' = [\n'
    file.write(s)
    for i in courses_lists:
        file.write('\t\t' + ' '*len(s) + '\t' + str(i) + ', \n')
    file.write('\t\t]\n\n')
    file.close()


#me = szx_edu_choose_class(2013140033, 137138)
#me.login()
"""
file = open('C:/Users/sunset/Desktop/test.py', 'a+')

file.write('class school_class(object):\n')
file.write('\tdef __init__(self):\n')
file.close()

name_cnname_dict = {}
szx_class_list = []
file.write('\t\tself.class_num_dict = {\n')
file.write('\t' * 9)
count = 1
for i in href_list:
    #html = me.get_courses_info(i[1])
    #get_courses_list(html, i[0])
    name_cnname_dict[i[0]] = i[2]
    szx_class_list.append(i[0])
    file.write("'" + i[0] + "'" + ':' + i[0] + ", ")
    if count % 5 == 0:
        file.write('\n' + '\t' * 9)
    count += 1


file = open('C:/Users/sunset/Desktop/d1820161.htm', 'r', encoding = 'gbk')
get_courses_list(file.read(), 'd1820161')
"""

import sys
sys.path.append('C:/Users/sunset/Desktop')
from choose_class_data import school_data_class
school_data = school_data_class()
"""
bpattern = re.compile('.+?<.+?>(.+?)<', re.DOTALL)
apattern = re.compile('.+?<.+?>(.+)', re.DOTALL)
a = '</td><td>01-17'
b = '</td><td>本课程仅供需要重修的学生选读。每班2节实验课（课堂时间），学院自行安排机房，具体时间另行通</td></tr>\r\n<tr><td><input type="checkbox" name="no_type" value="5000690024+必修'

for key,lists in school_data.class_num_dict.items():
    print ('matching....', school_data.name_dict[key])
    m = 0
    for each_list in lists:
        for i in range(5, len(each_list)):
            match = re.match(bpattern, each_list[i])
            if match != None:
                m += 1
                each_list[i] = match.group(1)
            else:
                match = re.match(apattern, each_list[i])
                if match != None:
                    m += 1
                    each_list[i] = match.group(1)

    print ('match over', m, 'results matched')
    print ('writing...', school_data.name_dict[key], '\n\n\n')
    file.write('\n\t\t' + key + '= [\n')
    for i in range(len(lists)):

        if i == len(lists) - 1:
            file.write('\t' * 6 + str(lists[i]) + '\n')
        else:
            file.write('\t' * 6 + str(lists[i]) + ',\n')
    file.write('\t' * 5 + ']\n')

file.close()
"""