import time
import json
import datetime
import MySQLdb
import urllib.request
import ssl
from train_dict import station_dict, type_dict, type_list
ssl._create_default_https_context = ssl._create_unverified_context

class train_search(object):
    def __init__(self, data):
        data_list = data.split('@@@')
        self.username = data_list[0].strip()
        self.date = data_list[1].strip()
        self.to_station_name = data_list[2].strip()
        self.from_station_name = data_list[3].strip()
        #self.init_opener()
        if self.valid(): # if not valid, self.echo_msg set to err_str
            # generate url and set self.echo_msg with <p> (sth like <...>)
            self.err_time = 0 # try 3 times per 0.3 sec
            self.get_result() # set self.echo_msg
        else:
            self.echo_msg = "<p align='center'><b>" + self.echo_msg + "</b></p>"

    def init_opener(self):
        self.cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate, br'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', '	keep-alive'),
                                  ('Host', 'kyfw.12306.cn'),
                                  ('Upgrade-Insecure-Requests', '1'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0')]

    def valid(self):
        self.echo_msg = False # default no error
        # check whether no input
        if len(self.from_station_name) == 0:
            self.echo_msg = "请输入出发站"
        elif len(self.to_station_name) == 0:
            self.echo_msg = "请输入到站"
        elif len(self.date) == 0:
            self.echo_msg = "请输入日期"
        if self.echo_msg != False:
            return False

        db = MySQLdb.connect(host = 'localhost', user = 'zpoint', passwd = 'a19950614', db = 'site', charset="utf8")
        cur = db.cursor()
        q = "SELECT username from train WHERE username = '%s'" % (self.username)
        cur.execute(q.encode('utf8'))
        fetch = cur.fetchone()
        cur.close()
        db.close()
        if fetch == None:
            self.echo_msg = "该用户未注册, 请注册"
            return False
        else:
            try:
                timestruct = time.strptime(self.date, "%Y-%m-%d")
                dusr = datetime.datetime(timestruct.tm_year, timestruct.tm_mon, timestruct.tm_mday)
                dnow = datetime.datetime.now()
                days_distance = (dusr - dnow).days
                if days_distance < -1 or (days_distance == -1 and time.strftime("%Y-%m-%d") != self.date):
                    self.echo_msg = "输入的日期在今天 %s 之前" % time.strftime("%Y-%m-%d")
                    return False
                elif (dusr - dnow).days > 58:
                    self.echo_msg = "只能查询到距今日60天内的日期，您输入的日期超出范围"
                    return False
                self.from_station_num = station_dict[self.from_station_name]
            except ValueError:
                self.echo_msg = "日期格式不对或没有该日期: %s, 请输入如下格式: %s" % (self.date, time.strftime("%Y-%m-%d"))
                return False
            except KeyError:
                self.echo_msg = "没有站台 %s , 请查证后重新输入(出发站)" % self.from_station_name
                return False
            
            try:
                self.to_station_num = station_dict[self.to_station_name]
            except KeyError:
                self.echo_msg = "没有站台 %s , 请查证后重新输入(目的站)" % self.to_station_name

        self.date = "%04d-%02d-%02d" % (timestruct.tm_year, timestruct.tm_mon, timestruct.tm_mday)
        return True if self.echo_msg == False else False

    def get_result(self):
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (self.date, self.from_station_num, self.to_station_num)
        try:
            f = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            if self.err_time < 3:
                self.err_time += 1
                return self.get_result()
            else:
                self.echo_msg = "<p align='center'><b>服务器正忙,HTTP请求异常, 请稍后重试!!!</b></p>"
                return False

        try:
            contStr = f.read().decode('utf-8')
            self.train_data_list = self.generate_new_list(url, contStr)
        except (json.decoder.JSONDecodeError, UnicodeDecodeError) as e:
            f = open('/var/www/py/train/err_search.txt', 'a+', encoding='utf8')
            f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '\t url:\t'+ url + '\treason:' + str(e) + '\n')
            f.close()
            if self.err_time < 3:
                self.err_time += 1
                return self.get_result()
            else:
                self.echo_msg = "<p align='center'><b>服务器正常,12306服务器正忙, 请稍后重试!!!</b></p>"
                return False

        if len(self.train_data_list) == 0:
            self.echo_msg = '<p align="center"><b>%s 这一天, 没有从 %s 到 %s 的车次</b></p>' % (self.date, self.from_station_name, self.to_station_name)
        else:
            self.echo_msg = '<table align="center" border=1><tr><td align="center">车次</td><td align="center">发车日期</td><td align="center">发车时间</td><td align="center">到站时间</td><td align="center">始发站</td><td align="center">终点站</td><td align="center">备注</td><td align="center">添加到监控列表</td></tr>'
            for each_dict in self.train_data_list:
                input_value = url + "@@@" + each_dict['车次'] # check train.php
                self.echo_msg += '<form id="resultform" action="train.php" method="post" ><tr><td align="center">%s</td><td align="center">%s</td><td align="center">%s</td><td align="center">%s</td><td align="center">%s</td><td align="center">%s</td><td align="center">%s</td><td align="center">%s</td></tr></form>' % (each_dict['车次'], each_dict['发车日期'][:4] + '-' + each_dict['发车日期'][4:6] + '-' + each_dict['发车日期'][6:], each_dict['发车时间'], each_dict['到站时间'], each_dict['始发站'], each_dict['终点站'], each_dict['备注'], '<input type="hidden" name="add_url" value="%s" /><input type="submit" align="center" value="添加" />' % (input_value))
            self.echo_msg += '</table>'

    def generate_new_list(self, url, contStr):
        def parse(each_train_dict, dic):
            for key, value in each_train_dict.items():
                if isinstance(value, dict):
                    parse(value, dic)
                else:
                    if key in type_list:
                        dic[type_dict[key]] = value
            return dic

        dic = json.loads(contStr)
        train_data_list = [] # dict inside

        for key, value in dic.items():
            if key == 'data':
                for each_train_dict in value:
                    new_dic = {}
                    train_data_list.append(parse(each_train_dict, new_dic))
        return train_data_list


