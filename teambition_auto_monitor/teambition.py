import urllib.request
import urllib.parse
import http.cookiejar
import json
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
            if each_task["creator"]["name"] == "Spaceman.robot" or each_task["title"] == "started redoing the task":
                self.task_list.append((each_task["_objectId"], each_task["subtitle"].split("API:")[1].split("｜")[0].strip()))
        print(self.task_list)


    def commit(self, id):
        self.opener.addheaders = [("Host", "www.teambition.com"),
                                  ("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"),
                                  ("Accept", "application/json, text/javascript, */*; q=0.01"),
                                  ("Accept-Language", "en-US,en;q=0.5"),
                                  ("Accept-Encoding", "deflate"),
                                  ("Content-Type", "application/json"),
                                  ("X-Requested-With", "XMLHttpRequest"),
                                  ("Referer", "https://www.teambition.com/project/57a6ecd2e5eecf796c7c2732/tasks/scrum/57a6ecd2826a02c2690d9e7e"),
                                  ("Content-Length", "30"),
                                  ("Connection", "close")
                                  ]
        paraamters = {
            "TEAMBITION_SESSIONID": self.sessionid,
            "TEAMBITION_SESSIONID.sig": self.sig,
            "mp_tbpanel__c": "1",
            "Hm_lvt_ec912ecc405ccd050e4cdf452ef4e85a": "1480658570,1480660265,1480662055",
            "Hm_lpvt_ec912ecc405ccd050e4cdf452ef4e85a": "1480669924",
            "_ga": "GA1.2.1393536801.1480669833",
            "_gat": "1",
            "lang": "zh",
            "_cioid": self.email,
            "_cio": "af89ae8a-4f7b-fae4-2317-0a205283274b",
            "mp_eSpCz4lYpMYgtuhdH0F6Wgtt_mixpanel":
            """
            {"distinct_id": "158becca589391-0cdebc38a382968-74256751-1fa400-158becca58a486","$os_version": "Linux x86_64","$initial_referrer": "https://account.teambition.com/login?next_url=https://www.teambition.com/project/57a6ecd2e5eecf796c7c2732/tasks/scrum/57a6ecd2826a02c2690d9e7e","$initial_referring_domain": "account.teambition.com","userKey": "582a736c5c1b2c0c45aba008","created_at": "2016-11-15T02:31:08.332Z","userLanguage": "zh","env": "release","version": "7.19.6","daysSinceRegistered": 18,"timezone": 8,"city": "Guangzhou","country": "China","region": "Guangdong","org_subscription": true,"experiments": [
            "created_after_2016_09_24_project_activity.A",
            "org_report_on.A"]}
            """,
            "fs_uid": "www.fullstory.com`M776`5636828678848512:5629499534213120`582a736c5c1b2c0c45aba008`false"
        }
        value = 'mp_tbpanel__c=1'
        for i in self.cookie:
            print(i)
        self.cookie.set_cookie(("mp_tbpanel__c=1", ".teambition.com/"))
        url = "https://www.teambition.com/api/tasks/" + id
        data = urllib.parse.urlencode(paraamters).encode("ascii")
        request = urllib.request.Request(url, data=data)
        request.get_method = lambda: 'PUT'
        response = self.opener.open(request)
        print(response.read())
        pass
