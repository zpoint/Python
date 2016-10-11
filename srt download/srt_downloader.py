import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import re
import os


class Application(object):
    def __init__(self):
        self.initial_tk()
        self.initial_Label()

        self.frm = tk.Frame(self.root)
        self.initial_frm1()
        self.initial_listbox()
        self.initial_final_button()
        self.frm.pack(side = tk.TOP)

        self.root.mainloop()

    def initial_tk(self):
        self.root = tk.Tk()
        self.root.title("Zpoint's Tools (由于抓取网站的限制，一个ip 24小时内只能下载15次)")
        self.root.geometry('600x400')
        self.root.resizable(width = False, height = False)

    def initial_Label(self):
        tk.Label(self.root, text = "美/英剧字幕下载器", font = ('黑体', 20)).pack()

    def initial_frm1(self):
        self.frm1 = tk.Frame(self.frm)
        #Entry
        self.entrytext = tk.StringVar()
        self.entry = tk.Entry(self.frm1, width = 30, textvariable = self.entrytext)
        self.entrytext.set("请输入英文剧名进行字幕搜索")
        self.entry.pack(side = tk.LEFT)
        #Button
        tk.Label(self.frm1, text = "                    ", font = ('Arial', 8)).pack(side = tk.LEFT)
        self.button_search = tk.Button(self.frm1, text = "搜索", command = self.search)
        self.button_search.pack(side = tk.RIGHT)
        self.frm1.pack(side = tk.TOP)

    def initial_listbox(self):
        self.frm2 = tk.Frame(self.frm)
        self.lbvar = tk.StringVar()
        self.lb = tk.Listbox(self.frm2, listvariable = self.lbvar, selectmode = tk.MULTIPLE, width = 80, height = 15)
        self.lbvar.set(tuple(['请键入关键字' for i in range(20)]))

        self.scrl = tk.Scrollbar(self.frm2)
        self.scrl.pack(side = tk.RIGHT, fill = tk.Y)
        self.lb.configure(yscrollcommand = self.scrl.set)
        self.scrl['command'] = self.lb.yview
        self.lb.bind('<ButtonRelease-1>', self.store_listbox_item)
        self.lb.pack(side = tk.TOP, fill = tk.BOTH)
        self.frm2.pack()

    def restore_listbox(self):
        for rdt in self.radiobuttons:
            rdt.forget()
        self.scrl.pack(side = tk.RIGHT, fill = tk.Y)
        self.lb.pack(side = tk.TOP, fill = tk.BOTH)
        self.lb.bind('<ButtonRelease-1>', self.store_listbox_item)
        #self.button_select_all.pack(side = tk.RIGHT)
        self.button_download.pack(side = tk.RIGHT)

        try:
            self.season_radiobuttons = []
            self.season_radiobuttons_vars = tk.IntVar()
            self.season_radiobuttons_vars.set(int(self.current_season))
            for i in range(int(self.maxseason)):
                radio_button = tk.Radiobutton(self.frm, text = '第'+ str(i+1) +'季', variable = self.season_radiobuttons_vars, value = i + 1, command = self.select_season)
                self.season_radiobuttons.append(radio_button)
                radio_button.pack(side = tk.LEFT)
        except AttributeError as e:
            print(e)
            return False

    def store_listbox_item(self, event):
        print (self.lb.curselection())

    def radio_button(self):
        self.radiobutton_vars = tk.IntVar()
        self.radiobutton_vars.set(2)
        self.radiobuttons = []
        i = 0
        for name,dir in self.dict_name_dir.items():
            radio_button = tk.Radiobutton(self.frm2, text = name, variable = self.radiobutton_vars, value = i, command = self.select_drama)
            self.radiobuttons.append(radio_button)
            radio_button.pack()
            i += 1
            

    def initial_final_button(self):
        #self.button_select_all = tk.Button(self.frm, text = "全选", command = self.selectall)
        self.button_quit = tk.Button(self.frm, text = "退出", command = self.root.quit)
        self.button_download = tk.Button(self.frm, text = "下载", command = self.download)

        self.button_quit.pack(side = tk.RIGHT)
        self.button_download.pack(side = tk.RIGHT)
        #self.button_select_all.pack(side = tk.RIGHT)
        
    def download(self):
        def dir():
            dir = filedialog.askdirectory(title = 'save', initialdir = os.getcwd())
            return dir
        directory = dir()
        print(directory)
        selected = self.lb.curselection()
        print(self.episode[selected[0]][5])
        
        #import zlib
        header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection':'keep-alive',
            'Host':	'www.addic7ed.com',
            'Referer':self.srt_mother_address,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}

        try:
            for i in self.lb.curselection():
                req = urllib.request.Request(self.episode[i][5], headers = header)
                print('req:',self.episode[i][5], '\n')
                respon = urllib.request.urlopen(req)
                print(respon.getheaders())
                srt = respon.read().decode('utf-8')

                filename_notmatched = respon.getheaders()[10][1]
                pattern = re.compile('.+?filename="(.+?)"', re.DOTALL)
                filename = re.match(pattern, filename_notmatched).group(1)
                print(filename)
                file = open(directory + '/' + filename, 'w')
                file.write(srt)
                file.close()
                self.entrytext.set( '下载完成 ' + filename )
        except UnicodeDecodeError:
            messagebox.showwarning(title = '警告', message = '您已经达到15次下载上限,对于该网站这个上限作者也很无奈哦，后续会更新么么哒,有问题联系 zp0int@qq.com')
            
        #srt_decompressed = zlib.decompress(respon.read(), 16+zlib.MAX_WBITS)
        #print(srt_decompressed)
        #print(respon.read().decode('utf-8'))


    def search(self):
        try:
            for rdt in self.radiobuttons:
                rdt.forget()
            self.radiobuttons = []
            for season_rbt in self.season_radiobuttons:
                season_rbt.forget()
            self.season_radiobuttons = []
        except AttributeError:
            pass
        self.search_value = self.entrytext.get()
        self.dict_name_dir = self.get_drama_name()

        self.lb.pack_forget()
        self.scrl.pack_forget()
        #self.button_select_all.forget()
        self.button_download.forget()

        self.radio_button()

    def select_drama(self):
        i = 0
        num = self.radiobutton_vars.get()
        for name,address in self.dict_name_dir.items():
            if i == num:
                self.drama_address = address
                break
            i += 1

        find = self.drama_address.find('www.addic7ed.com')
        if find < 0:
            self.drama_address = 'http://www.addic7ed.com/' + self.drama_address

        self.get_drama_srt_address()
        self.restore_listbox()
        #season, episode, title, language, compelete, url
        try:
            self.lbvar.set([('第' + arr[0] + '季' + '        第' + arr[1] + '集    ' +  '    语言: ' + arr[3] + '                      ' + arr[2].rjust(30)) for arr in self.episode])
        except AttributeError:
            return False

    def select_season(self):
        if str(self.season_radiobuttons_vars.get()) == str(self.current_season):
            return True
        self.srt_mother_address = self.url_generate(self.dramanum, str(self.season_radiobuttons_vars.get()))
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent':user_agent}
        print('self.srt_mother_address',self.srt_mother_address)
        req = urllib.request.Request(self.srt_mother_address, headers = headers)
        try:
            respon_object = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            errorcode = e.code
            messagebox.showwarning(title = 'HTTPError', message = '网络连接出现问题:'+ str(errorcode) + '请检查您的网络连接')
        except urllib.error.URLError as e:
            messagebox.showwarning(title = 'URLError', message = '无法连接到服务器，请检查网络资源是否被占用, 或联系作者 zp0int@qq.com ')
        html = respon_object.read() #byte
        html = (html.decode('utf-8')) #str
        content = html

        pattern = re.compile('.+<tr><th>S</th><th>E</th>(.+?)<thead><tr><th>Language.+?<tbody>(.+?)</tbody>', re.DOTALL)
        match = re.match(pattern, content)
        if match == None:
            self.lbvar.set(tuple(['无法找到该资源' for i in range(20)]))
            return False
        episode_content = match.group(1)
        language_content = match.group(2)

        #Get language and url, store in dict_language_address
        self.dict_language_address = {}
        pattern = re.compile('.+?<td>(.+?)</td>.+?loadShow\((.+?),(.+?),(.+?),(.+?),(.+?)\)(.+)', re.DOTALL)
        match = re.match(pattern, language_content)
        while match is not None:
            self.dict_language_address[match.group(1)] = self.url_generate(match.group(2), match.group(3), match.group(4), match.group(5), match.group(6))
            language_content = match.group(7)
            match = re.match(pattern, language_content)

        #Get current page's season, episode, title, compelete, language, and url, store in episode
        self.episode = []
        pattern = re.compile('.+?<td>(.+?)</td><td>(.+?)<.+?">(.+?)</a></td><td>(.+?)<.+?class.+?class.+?>(.*?Com.+?)<.+?href="(.+?)".+?</tr>(.+)', re.DOTALL)
        match = re.match(pattern, episode_content)
        while match is not None:
            #season, episode, title, language, compelete, address
            arr = [match.group(1), match.group(2), match.group(3), match.group(4), 100 if match.group(5) == 'Completed' else match.group(5)[:5], 'http://www.addic7ed.com' + match.group(6)]
            self.episode.append(arr)
            episode_content = match.group(7)
            match = re.match(pattern, episode_content)
        self.current_season = self.episode[0][0]

        try:
            self.lbvar.set([('第' + arr[0] + '季' + '        第' + arr[1] + '集    ' +  '    语言: ' + arr[3] + '                      ' + arr[2].rjust(30)) for arr in self.episode])
        except AttributeError:
            return False

    def url_generate(self, show, season, lang = '', hd = '', hi = ''):
        return 'http://www.addic7ed.com' + '/ajax_loadShow.php?show='+ show + '&season=' + season + '&langs=' + lang + '&hd=' + hd + '&hi=' + hi

    def get_drama_srt_address(self):
        "Fullfill dramanum, maxseason, dict_language_address, episode , current_season"
            
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent':user_agent}
        url = self.drama_address
        #HTTP GET grab the web
        req = urllib.request.Request(url, headers = headers)
        try:
            respon_object = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            errorcode = e.code
            messagebox.showwarning(title = 'HTTPError', message = '网络连接出现问题:'+ str(errorcode) + '请检查您的网络连接')
        except urllib.error.URLError as e:
            messagebox.showwarning(title = 'URLError', message = '无法连接到服务器，请检查网络资源是否被占用, 或联系作者 zp0int@qq.com ')
            print("Reason:",e.reason)

        html = respon_object.read() #byte
        html = (html.decode('utf-8')) #str

        pattern = re.compile('.+src="(.+showimages.+?)".+href="(.+)">Multi Download.+', re.DOTALL)
        match = re.match(pattern, html)
        if match == None:
            pattern = re.compile('.+href="(.+)">Multi Download.+', re.DOTALL)
            match = re.match(pattern, html)
            self.image_address = None
            self.srt_mother_address = "http://www.addic7ed.com" + match.group(1)
        else:
            self.image_address = match.group(1) #image address
        
            self.srt_mother_address = "http://www.addic7ed.com" + match.group(2) #srt address
        #
        print(self.image_address)
        print(self.srt_mother_address)
        #
        #Open srt address grab again
        req = urllib.request.Request(self.srt_mother_address, headers = headers)
        try:
            respon_object = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            errorcode = e.code
            messagebox.showwarning(title = 'HTTPError', message = '网络连接出现问题:'+ str(errorcode) + '请检查您的网络连接')
        except urllib.error.URLError as e:
            messagebox.showwarning(title = 'URLError', message = '无法连接到服务器，请检查网络资源是否被占用, 或联系作者 zp0int@qq.com ')
            print("Reason:",e.reason)
        html = respon_object.read() #byte
        html = (html.decode('utf-8')) #str
        content = html

        pattern = re.compile('.+onmouseup.+?\((.+?),(.+?).+<tr><th>S</th><th>E</th>(.+?)<thead><tr><th>Language.+?<tbody>(.+?)</tbody>', re.DOTALL)
        match = re.match(pattern, content)
        if match == None:
            self.lbvar.set(tuple(['无法找到该资源' for i in range(20)]))
            return False
        self.dramanum = match.group(1)
        self.maxseason = match.group(2)
        episode_content = match.group(3)
        language_content = match.group(4)
        url = self.url_generate(match.group(1), match.group(2))

        #Get language and url, store in dict_language_address
        self.dict_language_address = {}
        pattern = re.compile('.+?<td>(.+?)</td>.+?loadShow\((.+?),(.+?),(.+?),(.+?),(.+?)\)(.+)', re.DOTALL)
        match = re.match(pattern, language_content)
        while match is not None:
            self.dict_language_address[match.group(1)] = self.url_generate(match.group(2), match.group(3), match.group(4), match.group(5), match.group(6))
            language_content = match.group(7)
            match = re.match(pattern, language_content)

        #Get current page's season, episode, title, compelete, language, and url, store in episode
        self.episode = []
        pattern = re.compile('.+?<td>(.+?)</td><td>(.+?)<.+?">(.+?)</a></td><td>(.+?)<.+?class.+?class.+?>(.*?Com.+?)<.+?href="(.+?)".+?</tr>(.+)', re.DOTALL)
        match = re.match(pattern, episode_content)
        while match is not None:
            #season, episode, title, language, compelete, address
            arr = [match.group(1), match.group(2), match.group(3), match.group(4), 100 if match.group(5) == 'Completed' else match.group(5)[:5], 'http://www.addic7ed.com' + match.group(6)]
            self.episode.append(arr)
            episode_content = match.group(7)
            match = re.match(pattern, episode_content)
        self.current_season = self.episode[0][0]        
                 

    def get_drama_name(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent':user_agent}

        url = 'http://www.addic7ed.com/search.php'
        """
        search_value = input()
        search_value = search_value.strip()
        """
        search_value = self.search_value
        value = {'search':search_value.strip(),
                'Submit':'Search'}
        data = urllib.parse.urlencode(value)
        print(data)
        full_url = url + '?' + data

        #HTTP GET
        req = urllib.request.Request(full_url, headers = headers)
        try: 
            respon_object = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            errorcode = e.code
            messagebox.showwarning(title = 'HTTPError', message = '网络连接出现问题:'+ str(errorcode) + '请检查您的网络连接')
        except urllib.error.URLError as e:
            messagebox.showwarning(title = 'URLError', message = '无法连接到服务器，请检查网络资源是否被占用, 或联系作者 zp0int@qq.com ')
            print("Reason:",e.reason)

        html = respon_object.read() # byte
        html = (html.decode('utf-8')) #str

        #regular expression to get things
        pattern = re.compile('.+?<b>([0-9]+) results found</b>.+?<table.+?(<a href.+?</table>)', re.DOTALL)
        match = re.match(pattern, html)
        results_number = int(match.group(1))
        str_match = match.group(2)

        dict_name_dir = {}
        pattern = re.compile('.*?href="(.+?)".+?>(.+?)</a>(.+)', re.DOTALL)
        i = 1
        repeat = False

        while results_number > 0:
            sub_match = re.match(pattern, str_match)
            new_match = re.match('(.+?) - ([0-9]+)x([0-9]+) - (.+)', sub_match.group(2))
            if new_match:
                for name,value in dict_name_dir.items():
                    index = name.find("--")
                    name = name[0:index]
                    if new_match.group(1) == name:
                        repeat = True
                        break
            else:
                for name,value in dict_name_dir.items():
                    if sub_match.group(1) == name:
                        repeat = True
                        break
            if not repeat:
                if new_match:
                    dict_name_dir[new_match.group(1) + "--" + new_match.group(4)] = sub_match.group(1)
                else:
                    dict_name_dir[sub_match.group(2)] = sub_match.group(1)
            repeat = False
            str_match = sub_match.group(3)
            results_number -= 1

        return dict_name_dir
        
        

a = Application()
