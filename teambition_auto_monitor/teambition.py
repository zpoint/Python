import urllib.request
import urllib.parse
import http.cookiejar
import json
import requests
import func

class teambition(object):
    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.cookie = http.cookiejar.MozillaCookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        self.cookie.load(filename="/home/zpoint/Desktop/cookies.txt")

        for i in self.cookie:
            print(i.name, i.value, i.domain)


    def refresh(self):
        for i in self.cookie:
            if i.name == "TEAMBITION_SESSIONID":
                self.sessionid = i.value
            elif i.name == "TEAMBITION_SESSIONID.sig":
                self.sig = i.value

        refresh_paramaters = {
            "sort": "updated",
            "type": "normal",
            "count": "20",
            "page": "1",
            "TEAMBITION_SESSIONID": self.sessionid,
            "TEAMBITION_SESSIONID.sig": self.sig,
            "_cioid": self.email
        }

        self.opener.addheaders = [("Host", "www.teambition.com"),
                                  ("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"),
                                  ("Accept", "application/json, text/javascript, */*; q=0.01"),
                                  ("Accept-Language", "en-US,en;q=0.5"),
                                  ("Accept-Encoding", "deflate"),
                                  ("X-Requested-With", "XMLHttpRequest"),
                                  ("Referer", "https://www.teambition.com/project/57a6ecd2e5eecf796c7c2732/tasks/scrum/57a6ecd2826a02c2690d9e7e"),
                                  ("Connection", "close")
                                  ]
        url = "https://www.teambition.com/api/v2/messages?" + urllib.parse.urlencode(refresh_paramaters)
        print(url)
        resposne = self.opener.open(url)
        response_json = json.loads(resposne.read().decode())

        self.task_list = []
        for each_task in response_json:
            print(each_task)
            if each_task["creator"]["name"] == "Spaceman.robot" or each_task["title"] == "started redoing the task" or each_task["title"] == "重做了任务":
                self.task_list.append((each_task["_objectId"], each_task["subtitle"].split("API:")[1].split("｜")[0].strip()))
        print(self.task_list)
        self.commit(self.task_list[0][0])


    def commit(self, id):
        commit_headers = {"Host": "www.teambition.com",
                          "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
                          "Accept": "application/json, text/javascript, */*; q=0.01",
                          "Accept-Language": "en-US,en;q=0.5",
                          "Accept-Encoding": "gzip, deflate, br",
                          "Content-Type": "application/json",
                          "X-Requested-With": "XMLHttpRequest",
                          "Referer": "https://www.teambition.com/projects",
                          "Content-Length": "30",
                          "Connection": "close",
                          "Cookie": 'TEAMBITION_SESSIONID=eyJhdXRoVXBkYXRlZCI6MTQ4MDY2NTkwOTA1NSwibmV4dFVybCI6Imh0dHBzOi8vd3d3LnRlYW1iaXRpb24uY29tL3Byb2plY3QvNTdhNmVjZDJlNWVlY2Y3OTZjN2MyNzMyL3Rhc2tzL3NjcnVtLzU3YTZlY2QyODI2YTAyYzI2OTBkOWU3ZSIsInRzIjoxNDgwNjc2MTI0OTIwLCJ1aWQiOiI1ODJhNzM2YzVjMWIyYzBjNDVhYmEwMDgiLCJ1c2VyIjp7ImF2YXRhclVybCI6Imh0dHBzOi8vc3RyaWtlci50ZWFtYml0aW9uLm5ldC90aHVtYm5haWwvMTEwbTg1YTA1NmMwOGRiZDM4OTRhOTY2MjU0MjlkMTdmODRhL3cvMjAwL2gvMjAwIiwibmFtZSI6IumDreazveW5syIsImVtYWlsIjoiemVwaW5nLmd1b0BiaXQtYmV5b25kLmNvbSIsIl9pZCI6IjU4MmE3MzZjNWMxYjJjMGM0NWFiYTAwOCIsImlzTmV3Ijp0cnVlLCJyZWdpb24iOiJjbiJ9fQ==; TEAMBITION_SESSIONID.sig=XiLcnASntbhFJYL57f76sLNio7M; Hm_lvt_ec912ecc405ccd050e4cdf452ef4e85a=1480662055,1480676236,1480902920,1480909603; _ga=GA1.2.1108335841.1480676120; lang=zh; mp_tbpanel__c=1; _cioid=zeping.guo@bit-beyond.com; _cio=ad9d196e-ab1c-73d1-27af-49d0f98cdad8; mp_eSpCz4lYpMYgtuhdH0F6Wgtt_mixpanel={"distinct_id": "158bf2c9566289-04a80173abb3e2-74256751-1fa400-158bf2c95675ff","$os_version": "Linux x86_64","$initial_referrer": "https://account.teambition.com/login?next_url=https://www.teambition.com/project/57a6ecd2e5eecf796c7c2732/tasks/scrum/57a6ecd2826a02c2690d9e7e","$initial_referring_domain": "account.teambition.com","userKey": "582a736c5c1b2c0c45aba008","created_at": "2016-11-15T02:31:08.332Z","userLanguage": "zh","env": "release","version": "7.19.6","daysSinceRegistered": 21,"timezone": 8,"city": "Guangzhou","country": "China","region": "Guangdong","org_subscription": true,"experiments": []}; Hm_lpvt_ec912ecc405ccd050e4cdf452ef4e85a=1480909603; fs_uid=www.fullstory.com`M776`5678104522522624:5629499534213120`582a736c5c1b2c0c45aba008`false; _gat=1'
        }
        self.opener.addheaders = [("Host", "www.teambition.com"),
                                  ("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"),
                                  ("Accept", "application/json, text/javascript, */*; q=0.01"),
                                  ("Accept-Language", "en-US,en;q=0.5"),
                                  ("Accept-Encoding", "deflate"),
                                  ("Content-Type", "application/json"),
                                  ("X-Requested-With", "XMLHttpRequest"),
                                  ("Referer", "https://www.teambition.com/projects"),
                                  ("Content-Length", "30"),
                                  ("Connection", "close")
        ]
        url = "https://www.teambition.com/api/tasks/" + id
        print(url)

        paramaters = {}
        for each_cookie in self.cookie:
            paramaters[each_cookie.name] = each_cookie.value
        for key, value in paramaters.items():
            print(key, value)
        #data = urllib.parse.urlencode(paramaters).encode()
        data = urllib.parse.urlencode(paramaters).encode("ascii")
        request = urllib.request.Request(url, data=data)
        request.get_method = lambda: 'PUT'
        response = self.opener.open(request)
        print(response.headers)
        print(response.code)
        print(response.read())
        """
        paramaters = {
            "TEAMBITION_SESSIONID": "eyJhdXRoVXBkYXRlZCI6MTQ4MDY2NTkwOTA1NSwibmV4dFVybCI6Imh0dHBzOi8vd3d3LnRlYW1iaXRpb24uY29tL3Byb2plY3QvNTdhNmVjZDJlNWVlY2Y3OTZjN2MyNzMyL3Rhc2tzL3NjcnVtLzU3YTZlY2QyODI2YTAyYzI2OTBkOWU3ZSIsInRzIjoxNDgwNjc2MTI0OTIwLCJ1aWQiOiI1ODJhNzM2YzVjMWIyYzBjNDVhYmEwMDgiLCJ1c2VyIjp7ImF2YXRhclVybCI6Imh0dHBzOi8vc3RyaWtlci50ZWFtYml0aW9uLm5ldC90aHVtYm5haWwvMTEwbTg1YTA1NmMwOGRiZDM4OTRhOTY2MjU0MjlkMTdmODRhL3cvMjAwL2gvMjAwIiwibmFtZSI6IumDreazveW5syIsImVtYWlsIjoiemVwaW5nLmd1b0BiaXQtYmV5b25kLmNvbSIsIl9pZCI6IjU4MmE3MzZjNWMxYjJjMGM0NWFiYTAwOCIsImlzTmV3Ijp0cnVlLCJyZWdpb24iOiJjbiJ9fQ==",
            "TEAMBITION_SESSIONID.sig": "XiLcnASntbhFJYL57f76sLNio7M",
            "Hm_lvt_ec912ecc405ccd050e4cdf452ef4e85a": "1480662055,1480676236,1480902920,1480909603",
            "_ga": "GA1.2.1108335841.1480676120",
            "lang": "zh",
            "mp_tbpanel__c": "0",
            "_cioid": "zeping.guo@bit-beyond.com",
            "_cio": "ad9d196e-ab1c-73d1-27af-49d0f98cdad8",
            "mp_eSpCz4lYpMYgtuhdH0F6Wgtt_mixpanel": '{"distinct_id": "158bf2c9566289-04a80173abb3e2-74256751-1fa400-158bf2c95675ff","$os_version": "Linux x86_64","$initial_referrer": "https://account.teambition.com/login?next_url=https://www.teambition.com/project/57a6ecd2e5eecf796c7c2732/tasks/scrum/57a6ecd2826a02c2690d9e7e","$initial_referring_domain": "account.teambition.com","userKey": "582a736c5c1b2c0c45aba008","created_at": "2016-11-15T02:31:08.332Z","userLanguage": "zh","env": "release","version": "7.19.6","daysSinceRegistered": 21,"timezone": 8,"city": "Guangzhou","country": "China","region": "Guangdong","org_subscription": true,"experiments": []}',
            "Hm_lpvt_ec912ecc405ccd050e4cdf452ef4e85a": "1480909603",
            "fs_uid": "www.fullstory.com`M776`5678104522522624:5629499534213120`582a736c5c1b2c0c45aba008`false",
            "_gat": '1'
        }

        r = requests.put(url, data=paramaters, headers=commit_headers)
        print(r.status_code)
        print(r.content.decode())
        """
        pass
