import time
import logging
import json
import copy
import requests
import re
from selenium import webdriver
import selenium.common.exceptions
import urllib.parse
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def button_wrapper(method):
    def inner_helper(*args):
        try:
            method(*args)
        except selenium.common.exceptions.NoSuchElementException:
            args[0].click_notify_button()
            args[0].loop()
    return inner_helper


DEFAULT_CLICK_TIME = 1.5
class teambition(object):
    def __init__(self, userid, passwd, apiuserid, apipasswd):
        self.userid = userid
        self.passwd = passwd
        self.apiuserid = apiuserid
        self.apipasswd = apipasswd

        self.driver = webdriver.Firefox()
        self.unsolved_list = []
        self.api_login()  # login api page
        self.login()  # login teambition
        time.sleep(3)  # for login, the "wait until" in selenium has bug
        self.get_notify()  # find notify in DOM
        self.loop_time = 1
        self.loop()

    @button_wrapper
    def loop(self):
        while True:
            self.get_api_list()  # refresh api list
            self.click_down_notify(DEFAULT_CLICK_TIME)  # click down my task
            # filter the robot tasks
            for each_tasks in self.get_tasks():
                self.parse_tasks_ul(each_tasks)

            self.recheck()  # check whether cause by timeout or not, if timeout, reset it
            self.click_up_notify(DEFAULT_CLICK_TIME)  # click up for later refresh
            self.loop_time += 1
            logging.info("%-4d times loops done" % (self.loop_time, ))
            time.sleep(random.randint(3, 10))  # sleep

    def login(self):
        url = "https://account.teambition.com/login"
        xpaths = {
            "email": '//input[@name="email"]',
            "passwd": '//input[@name="password"]',
            "button": '//button[@class="btn btn-primary anim-blue-all" and @type="submit"]'
        }
        logging.info("Logging: " + url)
        self.driver.get(url)
        #self.driver.maximize_window()

        # Clear Username TextBox if already allowed "Remember Me"
        self.driver.find_element_by_xpath(xpaths["email"]).clear()
        self.driver.find_element_by_xpath(xpaths["passwd"]).clear()

        self.driver.find_element_by_xpath(xpaths["email"]).send_keys(self.userid)
        self.driver.find_element_by_xpath(xpaths["passwd"]).send_keys(self.passwd)
        self.driver.find_element_by_xpath(xpaths["button"]).click()
        """
        try:
            e = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="nav-body-handler my-handler"]'))
            )
            logging.info("Success in logging in")
        finally:
            self.driver.quit()
        """
        print(self.driver.get_cookies())
        print(self.driver.current_url)

    def get_notify(self):
        xpaths = {
            "my_notify": '//a[@class="nav-body-handler my-handler"]'
        }
        self.my_notify = self.driver.find_element_by_xpath(xpaths["my_notify"])

    def click_down_notify(self, seconds):
        self.my_notify.click()
        time.sleep(seconds)
        if seconds < 4:
            try:
                self.get_tasks()
            except selenium.common.exceptions.NoSuchElementException:
                logging.warning("Error calling click_down_notify, seconds: " + str(seconds))
                self.click_down_notify(seconds + 1)
        else:
            self.click_notify_button()
            self.click_down_notify(DEFAULT_CLICK_TIME)

    def click_up_notify(self, seconds):
        self.my_notify.click()
        time.sleep(seconds)
        if seconds < 4:
            try:
                self.get_tasks()
            except selenium.common.exceptions.NoSuchElementException:
                return
            self.click_up_notify(seconds + 1)
        self.click_notify_button()
        self.click_down_notify(DEFAULT_CLICK_TIME)

    def click_notify_button(self):
        xpath = "//button[@class='request-permission-btn btn btn-primary btn-block']"
        button = self.driver.find_element_by_xpath(xpath)
        print(button)
        button.click()

    def get_tasks(self):
        xpaths = {
            "today_tasks": '//div[@class="today-tasks"]/ul[@class="task-list my-list"]',
            "tomorrow_tasks": '//div[@class="tomorrow-tasks"]/ul[@class="task-list my-list"]',
            "week_tasks": '//div[@class="week-tasks"]/ul[@class="task-list my-list"]'
        }
        today_tasks_ul = self.driver.find_element_by_xpath(xpaths["today_tasks"])
        return (today_tasks_ul, )

    def parse_tasks_ul(self, tasks):
        ls_items = tasks.find_elements_by_xpath('./li')
        print(ls_items)
        print(len(ls_items))
        for each_li in ls_items:
            box = each_li.find_element_by_xpath('./a[@class="check-box"]')
            content_div = each_li.find_element_by_xpath('./div[@class="task-content-set"]')
            if "ApiBugList_AUTO_TASK" in content_div.text:
                self.unsolved_list.append((box, content_div))

    def click_box(self, solved_text_list):
        for i in range(len(solved_text_list)):
            each_text = solved_text_list[i]
            today_tasks_ul = self.get_tasks()[0]
            ls_items = today_tasks_ul.find_elements_by_xpath('./li')
            try:
                for each_li in ls_items:
                    box = each_li.find_element_by_xpath('./a[@class="check-box"]')
                    content_div = each_li.find_element_by_xpath('./div[@class="task-content-set"]')
                    if content_div.text == each_text:
                        box.click()
                        logging.info("Teambition box click Done " + each_text)
                        break
            except selenium.common.exceptions.StaleElementReferenceException:
                print("StaleElementReferenceException", solved_text_list[i])
                self.click_box(solved_text_list[i:])

    def recheck(self):
        solved_text_list = []
        rgx = re.compile(r".+?(http://.+?)｜")
        for box, content_div in self.unsolved_list:
            url = re.match(rgx, content_div.text).group(1).strip()
            logging.info(url)
            r = requests.get(url)
            json_obj = json.loads(r.content.decode())
            print(json_obj)
            api = urllib.parse.urlparse(url).path[1:]
            if "data" in json_obj and len(json_obj["data"]) > 0:
                logging.info(api + " behave correct")
                solved_text_list.append(content_div.text)
                for each_data in self.api_list_response:
                    if each_data["api"] == api and each_data["status"] == "0":
                        self.monitor(each_data)
                        each_data["status"] = "1"
                        break
            else:
                logging.info(api + " behave error")
        self.unsolved_list = []
        self.click_box(solved_text_list)

    def api_login(self):
        payload = {
            "username": self.apiuserid,
            "password": self.apipasswd
        }
        self.api_headers = {
            "Host": "120.25.255.56",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) "
                          "Gecko/20100101 Firefox/50.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://120.25.255.56/login",
            "Connection": "close"
        }
        url = "http://120.25.255.56/login/logindo"
        logging.info(url)
        self.api_login_response = requests.post(url, data=payload, headers=self.api_headers)
        print(self.api_login_response.content)
        self.api_cookies = self.api_login_response.headers["Set-Cookie"].split(";")[0].split("=")[1]
        print(self.api_cookies)


    def get_api_list(self):
        payload = {
            "ci_session": self.api_cookies,
            "order": "asc",
            "offset": "0",
            "limit": "50"
        }
        self.api_loin_headers = copy.deepcopy(self.api_headers)
        self.api_loin_headers["Cookie"] = "ci_session=" + self.api_cookies
        url = "http://120.25.255.56/api/tableView"
        logging.info(url)
        response = requests.post(url, data=payload, headers=self.api_loin_headers)
        response_json = json.loads(response.content.decode())
        if "error" in response_json:
            print(response_json)
            self.api_login()
            self.get_api_list()
        else:
            self.api_list_response = response_json["data"]


    def monitor(self, dataobj):
        payload = {
            "ci_session": self.api_cookies,
            "ids": dataobj["id"]
        }
        url = "http://120.25.255.56/api/monitor"
        logging.info(dataobj["name"] + " " + url)
        response = requests.post(url, data=payload, headers=self.api_loin_headers)
        content = json.loads(response.content.decode())
        print(content)
        if content["error"] != 0:
            if content['msg'] == 'API测试失败':
                logging.info(content)
            else:
                logging.info(content)
                self.api_login()
                self.monitor(dataobj)
