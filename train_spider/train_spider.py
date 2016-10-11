import time
import json
import datetime
import MySQLdb
import urllib.request
import ssl
import sys
import random
from train_dict import station_dict, type_dict, type_list
ssl._create_default_https_context = ssl._create_unverified_context
from mail import sendmail

def myPrintDict(dic, deep=0):
    def list_print(ls, deep):
        for item in ls:
            if isinstance(item, list):
                list_print(item, deep + 1)
            elif isinstance(item, dict):
                myPrintDict(item, deep + 1)
            else:
                for i in item:
                    print(i, sep = ', ')

    for key, value in dic.items():
        if isinstance(value, list):
            print(' ' * deep, key)
            list_print(value, deep + 1)
        elif isinstance(value, dict):
            print(' ' * deep, key)
            myPrintDict(value, deep + 1)
        else:
            print(' ' * deep, key, ' : ', value)

class train_spider(object):
    def __init__(self):
        #self.init_opener()
        self.get_dict()
        self.mail = sendmail()
        self.mail.login()
        self.success_time = 0
        self.fail_connection_err = 0
        self.fail_forbidden = 0
        self.fail_UnicodeDecode = 0
        self.fail_JSONDecode = 0        		
        self.maxdeep = 0
        self.fail_remote = 0
        self.success_send = 0
        self.fail_send = 0
		
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

    def get_dict(self):
        db = MySQLdb.connect(host = 'localhost', user = 'zpoint', passwd = 'a19950614', db = 'site', charset="utf8")
        cur = db.cursor()
        q = "SELECT * from train"
        cur.execute(q.encode('utf8'))
        self.fetch = cur.fetchall() # () or ((...),(...),(...),)
        cur.close()
        db.close()
        self.url_dict = {}
        self.usr_dict = {}
        for each_usr in self.fetch:
            for each_url in each_usr[3 : each_usr[16] + 3]: # check sql struct
                if each_url == '' or each_url == None:
                    break
                else:
                    split_url = each_url.split("@@@")
                    url = split_url[0]
                    train_id = split_url[1]
                    email = each_usr[2]
                    #check date
                    i = url.index('date=')
                    date = url[i+5:i+15]
                    timestruct = time.strptime(date, "%Y-%m-%d")
                    dusr = datetime.datetime(timestruct.tm_year, timestruct.tm_mon, timestruct.tm_mday)
                    dnow = datetime.datetime.now()
                    days_distance = (dusr - dnow).days
                    if days_distance < -1 or (days_distance == -1 and time.strftime("%Y-%m-%d") != date):
                        break

                    data_list = [train_id, None, False]
                    #usr_dict
                    self.usr_dict[email] = []
                    self.usr_dict[email].append(data_list)
                    #url dict
                    try:
                        url_train_list = self.url_dict[url]
                        #search
                        if data_list not in url_train_list:
                            self.url_dict[url].append(data_list)
                    except KeyError:
                        self.url_dict[url] = []
                        self.url_dict[url].append(data_list)

    def update_url(self, url, deep=0):
        "request to refresh url in self.url_dict, since self.usr_dict contains list inslde self.url_dict, it's updated too"
        try:
            f = urllib.request.urlopen(url)
        except (urllib.error.URLError, ConnectionRefusedError) as e:
            self.fail_connection_err += 1
            if deep > self.maxdeep:
                self.maxdeep = deep  
            return self.update_url(url, deep + 1)          
        except urllib.error.HTTPError as e:
            self.fail_forbidden += 1
            #print(f.read().decode('utf8'))
            #f = open('/var/www/py/train/err.txt', 'a+', encoding='utf8')
            #f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '\t url:\t'+ url + '\treason:' + str(e) + '\n')
            #f.close()
            if deep > self.maxdeep:
                self.maxdeep = deep			
            #time.sleep(2)
            return self.update_url(url, deep + 1)
        except http.client.RemoteDisconnected as e:
            self.fail_remote += 1
            if deep > self.maxdeep:
                self.maxdeep = deep			
            #time.sleep(2)
            return self.update_url(url, deep + 1)

        train_id_list = [usr_train_list[0] for usr_train_list in self.url_dict[url]]
        #print(contStr)
        try:
            contStr = f.read().decode('utf-8')
            train_data_list = self.generate_new_list(url, contStr)
        except UnicodeDecodeError as e:
            self.fail_UnicodeDecode += 1		
            #f = open('/var/www/py/train/err.txt', 'a+', encoding='utf8')
            #f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '\t url:\t'+ url + '\treason:' + '  UnicodeDecodeError\n')
            #f.close()
            #time.sleep(0.4)
            return False
        except json.decoder.JSONDecodeError as e:
            self.fail_JSONDecode += 1		
            #f = open('/var/www/py/train/err.txt', 'a+', encoding='utf8')
            #f.write(time.strftime("%Y-%m-%d %H:%M:%S") + '\t url:\t'+ url + '\treason:\t' + 'JSONDecodeError\n')
            #f.close()
            #time.sleep(0.4)
            if deep > self.maxdeep:
                self.maxdeep = deep	
            return self.update_url(url, deep + 1)
        self.success_time += 1			
        
        for each_train_dict in train_data_list:
            if each_train_dict['车次'] in train_id_list:
                index = train_id_list.index(each_train_dict['车次'])
                if self.url_dict[url][index][1] == each_train_dict: # not change
                    self.url_dict[url][index][2] = False # set flag (not necessary)
                else: # change
                    if self.url_dict[url][index][1] == None: ## first time after get_dict()
                        self.url_dict[url][index][1] = each_train_dict # ...[index][2] remains False
                    else:
                        self.url_dict[url][index][2] = each_train_dict
        return True

    def refresh_url_dict(self):
        err_flag = False
        for url in self.url_dict.keys():
            if self.update_url(url) == False:
                err_flag = True
                continue
        return True if not err_flag else False

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

    def send_email(self):
        def get_change_text(current_dict, new_dict):
            change_flag = False
            text = '您列表里的于 '+ new_dict['发车日期'][:4] + '-' + new_dict['发车日期'][4:6] + '-' + new_dict['发车日期'][6:] + ' 从 ' + new_dict['出发站'] + ' 到 ' + new_dict['到站'] + ' 的 ' + new_dict['车次'] + '班次\n'
            for each_key in  '商务座', '特等座', '一等座', '二等座', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座', '其他', '备注':
                if current_dict[each_key] != new_dict[each_key] and new_dict[each_key] != '--' and new_dict[each_key] != '无':
                    change_flag = True
                    text += each_key + ' 由 ' + current_dict[each_key] + ' 变为了\t' + new_dict[each_key] + '\n'
                else:
                    text += each_key + ': ' + new_dict[each_key] + ' 没有变化\n'
            text += '\n'
            if change_flag:
                return new_dict['车次'] + ' ', text
            else:
                return False

        for tomail, usr_data_list in self.usr_dict.items():
            subj = '您监控的车次: '
            text = ''
            send_flag = False
            for usr_train_list in usr_data_list:
                if usr_train_list[2] != False:
                    result = get_change_text(usr_train_list[1], usr_train_list[2])
                    if result != False: # maybe '--' ===> '无'
                        send_flag = True
                        new_subj, new_text = result[0], result[1]
                        subj += new_subj
                        text += new_text
                    usr_train_list[1] = usr_train_list[2]
                    usr_train_list[2] = False
            if send_flag:
                subj += " 票数发生了变化"
                text += "若不需要监测, 请到设置网站将该车次从列表移除\n"
                if self.mail.send(tomail, text, subj) == False:
                    self.fail_send += 1
                    #print ("Fail: ", time.strftime("%Y-%m-%d %H:%M:%S"), "self.mail.send(%s, sometext, %s)" % (tomail, subj))
                else:
                    self.success_send += 1
                    #print ("Success: ", time.strftime("%Y-%m-%d %H:%M:%S"), "self.mail.send(%s, sometext, %s)" % (tomail, subj))

    def start_loop(self):
        minute = -1 #first_time_start
        prev_day = -1	
        prev_hour = -1
        while True:
            prev_minute = minute	
            date = datetime.datetime.now()
            hour = date.hour
            minute = date.minute
            day = date.day
            # 23:00 - 5:30
            if hour >= 23 or hour < 5 or (hour == 5 and minute < 30):
                time.sleep(1800)
            elif hour == 5:
                time.sleep(300)
            else: # normal time
                if minute % 3 == 0 and minute != prev_minute: # connect to database and get_dict every 3 min
                    total = self.success_time + self.fail_forbidden + self.fail_JSONDecode + self.fail_UnicodeDecode + self.fail_connection_err + self.fail_remote + self.success_send + self.fail_send
                    log = time.strftime("%Y-%m-%d %H:%M:%S") + " success: %5d, HTTP_ERR: %5d, Json_ERR: %4d, Uni_ERR: %4d, CONN_ERR: %4d,\n \t\tREMOTE_ERR = %4d,  SUCCESS_SEND = %4d, FAIL_SEND = %4d, mxdeep:%d Succ_rate: %.2f%%\n" % (self.success_time, self.fail_forbidden, self.fail_JSONDecode, self.fail_UnicodeDecode, self.fail_connection_err, self.fail_remote, self.success_send, self.fail_send, self.maxdeep, self.success_time / total *  100 if prev_minute != -1 and total != 0 else 0)
                    #print(log)
                    if (hour != prev_hour): #print log per hour
                        print(log)
                        prev_hour = hour
                    if (day != prev_day): # send log per day
                        print("day: %02d prev_day: %02d send: %s" % (day, prev_day, str(self.mail.send('zp0int@qq.com', log, 'train_spider_log: %s' % (time.strftime("%Y-%m-%d %H:%M:%S"))))))
                        prev_day = day
                    sys.stdout.flush()
                    self.get_dict()
                    self.refresh_url_dict()
                    continue
                else:
                    #print(time.strftime("%Y-%m-%d %H:%M:%S"), "success:", self.success_time, "HTTP Error:", self.fail_forbidden, "maxdeep:", self.maxdeep, "JsonDescode_err:", self.fail_JSONDecode, "UnicodeDecodeError", self.fail_UnicodeDecode)
                    self.refresh_url_dict()
                    self.send_email()
                    #self.sleep(3)					
                    time.sleep(random.randint(5, 20))

if __name__ == '__main__':
    watcher = train_spider()
    print('begin', time.strftime("%Y-%m-%d %H:%M:%S"))
    watcher.start_loop()
