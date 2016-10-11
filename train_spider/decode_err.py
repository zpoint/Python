import time
import json
import datetime
import urllib.request
import http.cookiejar
import ssl
from train_dict import station_dict, type_dict, type_list
ssl._create_default_https_context = ssl._create_unverified_context
def generate_new_list(url, contStr):
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
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                                  ('Accept-Encoding', 'gzip, deflate, br'),
                                  ('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'),
                                  ('Connection', '	keep-alive'),
                                  ('Host', 'kyfw.12306.cn'),
                                  ('Upgrade-Insecure-Requests', '1'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0')]
url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2016-09-28&leftTicketDTO.from_station=IOQ&leftTicketDTO.to_station=CNQ&purpose_codes=ADULT'
#f = urllib.request.urlopen(url)
f = opener.open(url)
c = f.read()
print(c)
contStr = c.decode('utf8')
train_data_list = generate_new_list(url, contStr)
print(type(contStr))
