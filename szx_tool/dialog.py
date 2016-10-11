"""
proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
# This time, rather than install the OpenerDirector, we use it directly:
opener.open('http://www.example.com/login.html')


def get_urlopen():
    proxy_type = get_prefs('proxy_type')
    if proxy_type == 'http':
        scheme = 'http'
        host = str(get_prefs('proxy_host'))
        port = str(get_prefs('proxy_port'))
        url = scheme + '://' + host + ':' + port
        if get_prefs('proxy_auth'):
            proxy_support = urllib2.ProxyHandler({ 'http': url, 'https': url })
            username = str(get_prefs('proxy_auth_name'))
            password = str(get_prefs('proxy_auth_password'))
            auth_handler = urllib2.ProxyBasicAuthHandler()
            auth_handler.add_password(None, url, username, password)
            return urllib2.build_opener(proxy_support, auth_handler).open
        else:
            proxy_support = urllib2.ProxyHandler({ 'http': url, 'https': url })
            return urllib2.build_opener(proxy_support).open
    elif proxy_type == 'system':
        if 'http_proxy' in os.environ and os.environ["http_proxy"]:
            url = os.environ["http_proxy"]
        elif 'HTTP_PROXY' in os.environ and os.environ["HTTP_PROXY"]:
            url = os.environ["HTTP_PROXY"]
        else:
            url = None

        if not url:
            return urllib2.urlopen
        else:
            proxy_support = urllib2.ProxyHandler({ 'http': url, 'https': url })
            return urllib2.build_opener(proxy_support).open
    else:
        return urllib2.urlopen


"""
import sys
import os
import base64
from tempfile import gettempdir
from PyQt5 import QtWidgets
from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from collections import OrderedDict
from szx_class import szx_edu_grade
class mywindow(QtWidgets.QMainWindow):
    def __init__(self, **kwargs):
        super(mywindow, self).__init__(**kwargs)
        #self.d = scoreDialog()
        #self.d = LoginDlg(self)
        #self.d = proxyDialog(self)
        #self.d = helpDialog()
        self.d = updateDialog()
        self.d.exec_()

class LoginDlg(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDlg, self).__init__(parent)
        self.parent = parent
        self.photo_label = QtWidgets.QLabel()

        self.proxy_usr = ""
        self.proxy_pwd = ""
        self.require_flag = False
        self.cache_flag = False
        self.lock_refresh = False
        self.proxyflag = False
        self.remember_pwd_flag = False
        self.auto_login_flag = False
        self.remember_proxy_flag = False
        self.proxy_url = 'http://proxy.szu.edu.cn:8080/'

        self.class_grade = szx_edu_grade()
        self.dlgLayout = Qt.QVBoxLayout()
        self.dlgLayout.setContentsMargins(15, 15, 15, 15)
        self.dlgLayout.addLayout(self.init_grid())
        self.dlgLayout.addStretch(40)
        self.dlgLayout.addLayout(self.init_cbx())
        self.dlgLayout.addLayout(self.init_btn())

        if len(self.user_dict) != 0:
            self.get_check_box(self.userlinecbx.currentText(), self.user_dict[self.userlinecbx.currentText()][0])
            self.cache_flag_checkbox.setChecked(True)
            self.set_cache_flag()

            

        self.setLayout(self.dlgLayout)
        self.setWindowTitle("深圳大学 学分统计工具登录窗口")
        self.resize(300, 170)
        if not self.cache_flag:
            self.refresh()
        if self.auto_login_flag:
            self.pwdLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)

    def init_grid(self):
        user = QtWidgets.QLabel('学号：')
        pwd = QtWidgets.QLabel('选课密码： ')
        getcode = QtWidgets.QLabel('验证码： ')

        self.user_dict = self.get_user_dict()

        self.userlinecbx = QtWidgets.QComboBox()
        for usr, pair in self.user_dict.items():
            self.userlinecbx.addItem(usr)
        self.userlinecbx.setEditable(True)

        self.userlinecbx.currentIndexChanged.connect(self.change_current_index)
        self.userlinecbx.currentTextChanged.connect(self.change_current_text)
        """
        self.userLineEdit = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(0, 9999999999999, self.userLineEdit)
        self.userLineEdit.setValidator(validator)
        """
        self.pwdLineEdit = QtWidgets.QLineEdit()
        self.pwdLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.getcodeEdit = QtWidgets.QLineEdit()
        
        grid = QtWidgets.QGridLayout()
        grid.addWidget(user, 0, 0, 1, 1)
        grid.addWidget(pwd, 1, 0, 1, 1)
        grid.addWidget(getcode, 2, 0, 1, 1)
        grid.addWidget(self.userlinecbx, 0, 1, 1, 3)
        grid.addWidget(self.pwdLineEdit, 1, 1, 1, 3)
        grid.addWidget(self.getcodeEdit, 2, 1, 1, 1)
        grid.addWidget(self.photo_label, 2, 3)

        return grid

    def change_current_text(self, text):
        try:
            pwd = self.user_dict[text][0]
            self.get_check_box(text, pwd)
            self.cache_flag = True
            self.cache_flag_checkbox.setChecked(True)
            self.getcodeEdit.setEnabled(False)
        except KeyError:
            self.set_default_box()

    def change_current_index(self, index): #change index
        usr = self.userlinecbx.currentText().strip()
        pwd = self.user_dict[usr][0]
        self.get_check_box(usr, pwd)
        self.cache_flag = True
        self.cache_flag_checkbox.setChecked(True)

    def load_and_set_proxy(self, usr):
            message = self.user_dict[usr][1]
            proxy_pair = message.split("@@@")[-1].split("$$$")
            self.proxy_usr = proxy_pair[0]
            self.proxy_pwd = proxy_pair[1]
            self.proxy_url = proxy_pair[2]
            self.class_grade.setproxy(self.proxy_url, self.proxy_usr, self.proxy_pwd)
            self.proxyflag = True

    def get_check_box(self, usr, pwd):
        ##set check box and password if password remembered
        self.remember_pwd_flag = True if pwd[0] == '1' else False
        self.auto_login_flag = True if pwd[1] == '1' else False 
        self.remember_proxy_flag = True if pwd[2] == '1' else False
        #self.require_flag = True if pwd[3] == '1' else False
        
        self.remember_pwd_checkbox.setChecked(self.remember_pwd_flag)
        self.auto_login_checkbox.setChecked(self.auto_login_flag)
        self.remember_proxy_checkbox.setChecked(self.remember_proxy_flag)
        self.require_flag_checkbox.setChecked(self.require_flag)
        if self.remember_pwd_flag:
            self.pwdLineEdit.setText(pwd[3:])
        if self.remember_proxy_flag:
            self.load_and_set_proxy(usr)

    def set_default_box(self):
        if self.proxyflag:
            self.unset_proxy()
        self.remember_pwd_flag = False
        self.auto_login_flag = False 
        self.remember_proxy_flag = False  
        self.require_flag = False
        self.cache_flag = False

        self.remember_pwd_checkbox.setChecked(self.remember_pwd_flag)
        self.auto_login_checkbox.setChecked(self.auto_login_flag)
        self.remember_proxy_checkbox.setChecked(self.remember_proxy_flag)
        self.require_flag_checkbox.setChecked(self.require_flag)
        self.cache_flag_checkbox.setChecked(False)
        self.getcodeEdit.setEnabled(True)
        self.pwdLineEdit.clear()
        

    def show_code(self):
        ##check network environment
        if isinstance(self.getcode_response, tuple):
            if self.getcode_response[0] == 2:
                warning = '无法连接到网络, 请检查您的网络连接'
            if self.getcode_response[0] == 3:
                warning = '无法连接到服务器， 若不在校内网环境， 请设置代理'
            Qt.QMessageBox.warning(self, '警告', warning, Qt.QMessageBox.Yes)
            return False

        pixmap = QtGui.QPixmap()
        success_load = pixmap.loadFromData(QtCore.QByteArray(self.getcode_response))
        if success_load:
            self.photo_label.setPixmap(pixmap)
        else:
            Qt.QMessageBox.warning(self, '警告', '无法解析验证码，请刷新', Qt.QMessageBox.Yes)

    def init_btn(self):
        okbtn = Qt.QPushButton('确定')
        okbtn.clicked.connect(self.log_check)
        refreshbtn = Qt.QPushButton('刷新验证码')
        refreshbtn.clicked.connect(self.refresh)
        self.proxybtn = Qt.QPushButton('设置代理(未设置)')
        self.proxybtn.clicked.connect(self.proxydialog)
        quitbtn = Qt.QPushButton('退出')
        quitbtn.clicked.connect(QtCore.QCoreApplication.quit)
        
        btnLayout = Qt.QHBoxLayout()
        btnLayout.setSpacing(17)
        btnLayout.addWidget(okbtn)
        btnLayout.addWidget(refreshbtn)
        btnLayout.addWidget(self.proxybtn)
        btnLayout.addWidget(quitbtn)
        return btnLayout

    def init_cbx(self):
        self.remember_pwd_checkbox = QtWidgets.QCheckBox()
        self.remember_pwd_checkbox.clicked.connect(self.remember_pwd)
        self.auto_login_checkbox = QtWidgets.QCheckBox()
        self.auto_login_checkbox.clicked.connect(self.auto_login)
        self.remember_proxy_checkbox = QtWidgets.QCheckBox()
        self.remember_proxy_checkbox.clicked.connect(self.remember_proxy)
        self.require_flag_checkbox = QtWidgets.QCheckBox()
        self.require_flag_checkbox.clicked.connect(self.set_require_flag)
        self.cache_flag_checkbox = QtWidgets.QCheckBox()
        self.cache_flag_checkbox.clicked.connect(self.set_cache_flag)

        cbxLayout = Qt.QHBoxLayout()
        #cbxLayout.setSpacing(10)
       
        rem_Layout = Qt.QHBoxLayout()
        rem_Layout.setSpacing(1)
        rem_Layout.addWidget(self.remember_pwd_checkbox)
        rem_Layout.addWidget(QtWidgets.QLabel("记住密码"))
        rem_Widget = QtWidgets.QWidget()
        rem_Widget.setLayout(rem_Layout)
        
        auto_login_Layout = Qt.QHBoxLayout()
        auto_login_Layout.setSpacing(1)
        auto_login_Layout.addWidget(self.auto_login_checkbox)
        auto_login_Layout.addWidget(Qt.QLabel("显示密码"))
        auto_login_Widget = QtWidgets.QWidget()
        auto_login_Widget.setLayout(auto_login_Layout)

        rem_proxy_Layout = Qt.QHBoxLayout()
        rem_proxy_Layout.setSpacing(1)
        rem_proxy_Layout.addWidget(self.remember_proxy_checkbox)
        rem_proxy_Layout.addWidget(Qt.QLabel("记住代理"))
        rem_proxy_Widget = QtWidgets.QWidget()
        rem_proxy_Widget.setLayout(rem_proxy_Layout)

        require_flag_Layout = Qt.QHBoxLayout()
        require_flag_Layout.setSpacing(1)
        require_flag_Layout.addWidget(self.require_flag_checkbox)
        require_flag_Layout.addWidget(Qt.QLabel("更改必修"))
        require_flag_Widget = QtWidgets.QWidget()
        require_flag_Widget.setLayout(require_flag_Layout)

        cache_flag_Layout = Qt.QHBoxLayout()
        cache_flag_Layout.setSpacing(1)
        cache_flag_Layout.addWidget(self.cache_flag_checkbox)
        cache_flag_Layout.addWidget(Qt.QLabel("读取缓存"))
        cache_flag_Widget = QtWidgets.QWidget()
        cache_flag_Widget.setLayout(cache_flag_Layout)

        #cbxLayout.setSpacing(5)
        cbxLayout.addWidget(rem_Widget)
        cbxLayout.addWidget(auto_login_Widget)
        cbxLayout.addWidget(rem_proxy_Widget)
        cbxLayout.addWidget(require_flag_Widget)
        cbxLayout.addWidget(cache_flag_Widget)
        return cbxLayout


    def remember_pwd(self):
        if self.remember_pwd_checkbox.isChecked() == True: ##when you click , become true
            self.remember_pwd_flag = True
        else:
            self.remember_pwd_flag = False
            if self.auto_login_flag == True:
                self.auto_login_flag = False
                self.auto_login_checkbox.setChecked(False)

    def auto_login(self):
        if self.auto_login_checkbox.isChecked() == True:
            self.auto_login_flag = True
            self.pwdLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.auto_login_flag = False
            self.pwdLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

    def remember_proxy(self):
        if self.remember_proxy_checkbox.isChecked() == True:
            if not self.proxyflag:
                Qt.QMessageBox.warning(self, '您未设置代理', '您还未设置代理，无法记住', Qt.QMessageBox.Yes)
                self.remember_proxy_checkbox.setChecked(False)
                return False
            self.remember_proxy_flag = True
        else:
            self.remember_proxy_flag = False

    def set_require_flag(self):
        if self.require_flag_checkbox.isChecked() == True:
            Qt.QMessageBox.warning(self, '您正在尝试更改必修的类型', '为了界面简洁，必修类型默认禁止修改，若勾上该选项，必修类型将可以修改\n若不是选课时必修有错误，不建议勾上该选项', Qt.QMessageBox.Yes)
            self.require_flag = True
        else:
            self.require_flag = False

    def set_cache_flag(self):
        if self.cache_flag_checkbox.isChecked() == True:
            if len(self.user_dict) == 0 or self.userlinecbx.currentText().strip() not in self.user_dict:
                Qt.QMessageBox.warning(self, '该用户无缓存数据', '\n 您输入的账号未在本机登陆过， 无法开启该功能。\n成功登陆过后再次登录会自动启用！当你成功登陆后，会在本机生成缓存文件\n再次登录时数据会从缓存文件中读取\n以此来加速您的登录速度\n当该选项开启时，默认从缓存文件中读取数据', Qt.QMessageBox.Yes)
                self.cache_flag_checkbox.setChecked(False)
                return False
            else:    
                self.getcodeEdit.setEnabled(False)
                self.cache_flag = True
        else:
            Qt.QMessageBox.warning(self, '您正在更改登陆数据的读取方式', '当该选项为选中状态时，您的选课数据会从从本机读取。\n此时，无需输入验证码，无需登陆校内网\n1.对于首次在本机登陆的用户，因为没有数据缓存在本机，勾选与不勾选效果相同\n2.对于成功登陆过的用户,勾选此项后，无需输入验证码即可登陆，将从本地读取数据。\n---------------------------------------------------------------------------------\n为了使程序运行快速，减少您的等待时间,当您第一次登陆过后，该选项默认开启\n当该选项开启时，程序将从本地加载数据，即使不在校园网下,也可以不设置代理而进行登录\n建议当获得的真实学分与缓存学分不符时，取消勾选次项', Qt.QMessageBox.Yes)
            self.getcodeEdit.setEnabled(True)
            self.cache_flag = False
            self.refresh()

    def log_check(self):
        assert self.remember_proxy_flag == self.remember_proxy_checkbox.isChecked()
        assert self.remember_pwd_flag == self.remember_pwd_checkbox.isChecked()
        assert self.auto_login_flag == self.auto_login_checkbox.isChecked()
        assert self.require_flag == self.require_flag_checkbox.isChecked()
        assert self.cache_flag == self.cache_flag_checkbox.isChecked()

        username = self.userlinecbx.currentText().strip()
        pwd = self.pwdLineEdit.text().strip()
        getcode = self.getcodeEdit.text().strip()

        warning = False
        if len(username) == 0:
            warning = '请输入您的学号！！！'
        #elif not username.isdigit():
        #    warning = '学号格式有误，请检查后重新输入！！！'
        elif len(pwd) == 0:
            warning = '请输入密码！！！'
        elif len(pwd) < 6 or len(pwd) > 15:
            warning = '密码长度不符！！！'
        elif self.cache_flag == False:
            if len(getcode) == 0:
                warning = '请输入验证码！！！'
            elif len(getcode) > 8:
                warning = '验证码长度不符！！！'
            elif not getcode.isdigit():
                warning = '验证码为纯数字，请重新输入！！！'

        if warning != False:
            Qt.QMessageBox.warning(self, '警告', warning, Qt.QMessageBox.Yes)
            self.userlinecbx.setFocus()
            self.pwdLineEdit.clear()
        elif self.cache_flag == False:
            self.class_grade.init_user_pwd(username, pwd, getcode)
            if self.class_grade.login() == False:
                Qt.QMessageBox.warning(self, '无法登陆', '请检查用户,密码,验证码是否正确', Qt.QMessageBox.Yes)
                self.refresh()
                if self.cache_flag:
                    self.cache_flag_checkbox.setChecked(False)
                    self.cache_flag = False
            else: ##cache_flag = False, new_usr
                self.parent.class_grade = self.class_grade
                self.parent.continue_init()
        else:
            message_list = self.user_dict[username][1].split('@@@')
            exec("self.message_list = " + message_list[0])
            exec("self.SEMESTERS_LIST = " + message_list[1])
            exec("self.require_list = " + message_list[2])
            exec("self.major_choose_list = " + message_list[3])
            exec("self.normal_elective_list = " + message_list[4])
            self.photodir = self.dir + '\\' + username + '.jpg'
            #print(self.photodir)
            self.parent.continue_init()

    def refresh(self):
        if self.cache_flag == True:
            Qt.QMessageBox.information(self, '注意', '请取消勾选"读取缓存"选项，再刷新编辑您的验证码\n您的"读取缓存"勾选框为勾选状态，数据将会从本地读取\n当数据从本地读取时，不需要输入验证码\n若想在线读取您的数据, 请取消勾选"读取缓存"', Qt.QMessageBox.Yes)
            return False
        if self.lock_refresh == True:
            Qt.QMessageBox.information(self, '操作过快', '上一个验证码正在加载中，请一会再刷新', Qt.QMessageBox.Yes)
            return False
        self.lock_refresh = True
        self.getcode_response = self.class_grade.getcode()
        self.show_code()
        self.lock_refresh = False

    def proxydialog(self):
        proxyDialog(self).exec_()

    def setproxy(self, proxyurl, card_num, pwd):
        self.proxy_usr = card_num
        self.proxy_pwd = pwd
        self.class_grade.setproxy(proxyurl, card_num, pwd)
        self.proxyflag = True
        self.proxybtn.setText('设置代理(已设置)')
        self.proxybtn.repaint()

    def unset_proxy(self):
        self.class_grade.unset_proxy()
        self.proxyflag = False
        self.proxybtn.setText('设置代理(未设置)')
        self.proxybtn.repaint()

    def get_user_dict(self):
        #user_dict = {(usr : (pwd, "nessage")} all string type   real_pwd = pwd[3:]  pwd[0] = remember_pwd_flag  pwd[1] = auto_login_flag  pwd[2] = remember_proxy_flag '1' for True, '0' for False
        #usr !!! pwd ### main_message @@@ require @@@ major_choose @@@ normal_elective
        #The top one is the latest one
        user_dict = OrderedDict()
        self.dir = gettempdir() + '\\szx'
        self.file_dir = self.dir + "\\szx"
        if not os.path.isdir(self.dir):
            return OrderedDict()
        if os.path.isfile(self.file_dir):
            f = open(self.file_dir, 'r', encoding='utf8')
            try:
                for line in f.readlines():
                    line = base64.b64decode(line.encode('utf8'))
                    line = line.decode('utf8')
                    pair = line.split("###")
                    if len(pair) != 2:
                        Qt.QMessageBox.warning(self, '警告', "您统计工具缓存位置的数据被修改，若不是本人操作，请检测电脑安全", Qt.QMessageBox.Yes)
                        f.close()
                        os.remove(self.file_dir) 
                        return OrderedDict()

                    self.usr_pwd_pair = tuple(pair[0].split('!!!'))
                    if not os.path.isfile(self.dir + '\\' + self.usr_pwd_pair[0] + '.jpg'):
                        Qt.QMessageBox.warning(self, '警告', "您统计工具缓存位置的图像数据被修改过，若不是本人操作，请检测电脑安全", Qt.QMessageBox.Yes)
                        f.close()
                        os.remove(self.file_dir)
                        return OrderedDict()
                    user_dict[self.usr_pwd_pair[0]] = (self.usr_pwd_pair[1], pair[1])
            except UnicodeDecodeError:
                Qt.QMessageBox.warning(self, '警告', "您统计工具缓存位置的数据(文件格式)被修改，若不是本人操作，请检测电脑安全", Qt.QMessageBox.Yes)
                f.close()
                os.remove(self.file_dir)
                return OrderedDict()
            f.close()
        return user_dict

class proxyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(proxyDialog, self).__init__(parent)
        self.parent = parent
        self.defaulturl = self.parent.proxy_url
        self.initUI()
        self.setWindowTitle("代理设置")
        self.resize(230, 100)

    def initUI(self):
        grid = QtWidgets.QGridLayout()

        self.card_numline = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(0, 999999999, self.card_numline)
        self.card_numline.setValidator(validator)
        self.card_numline.setText(self.parent.proxy_usr)

        self.pwdline = QtWidgets.QLineEdit()
        self.pwdline.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwdline.setText(self.parent.proxy_pwd)

        self.radiobutton = QtWidgets.QRadioButton()
        self.radiobutton.clicked.connect(self.proxy_warn)
        self.proxyline = QtWidgets.QLineEdit()
        self.proxyline.setText(self.defaulturl)
        self.proxyline.setEnabled(False)

        okbtn = Qt.QPushButton('设置代理')
        quitbtn = Qt.QPushButton('解除已设置代理') 
        okbtn.clicked.connect(self.accept)  # 确定
        quitbtn.clicked.connect(self.unset)  # 取消

        grid.addWidget(QtWidgets.QLabel("请输入校园卡卡号:"), 0, 0)
        grid.addWidget(self.card_numline, 0, 1)
        grid.addWidget(QtWidgets.QLabel('请输入查询密码:'), 1, 0)
        grid.addWidget(self.pwdline, 1, 1)

        proxyLayout = Qt.QHBoxLayout()
        proxyLayout.setSpacing(5)
        proxyLayout.addWidget(self.radiobutton)
        proxyLayout.addWidget(QtWidgets.QLabel('更改'))
        proxyLayout.addWidget(self.proxyline)
        proxyWidget = QtWidgets.QWidget()
        proxyWidget.setLayout(proxyLayout)
        grid.addWidget(proxyWidget, 2, 0, 1, 2)
        #grid.setColumnStretch(0, 10)
        #grid.setColumnStretch(1, 15)
        btnLayout = Qt.QHBoxLayout()
        btnLayout.setSpacing(16)
        btnLayout.addWidget(okbtn)
        btnLayout.addWidget(quitbtn)
        btnWidget = QtWidgets.QWidget()
        btnWidget.setLayout(btnLayout)
        grid.addWidget(btnWidget, 3, 0, 1, 2)

        self.setLayout(grid)

    def unset(self):
        if not self.parent.proxyflag:
            Qt.QMessageBox.warning(self, '警告', "您并未设置过代理，目前没有设置代理，取消失败", Qt.QMessageBox.Yes)
            self.reject()
            return False
        self.parent.unset_proxy()
        Qt.QMessageBox.information(self, '设置', "您的代理已经取消成功, 请点击刷新验证码", Qt.QMessageBox.Yes)
        self.reject()

    def accept(self):
        pwd = self.pwdline.text().strip()
        card_num = self.card_numline.text().strip()
        if len(pwd) == 0:
            Qt.QMessageBox.warning(self, '警告', "请输入密码", Qt.QMessageBox.Yes)
            return False
        elif len(card_num) == 0:
            Qt.QMessageBox.warning(self, '警告', "请输入校园卡号", Qt.QMessageBox.Yes)
            return False
        proxyurl = self.proxyline.text().strip()
        if proxyurl != self.defaulturl:
            if proxyurl[0:7] != "http://" or proxyurl[0:8] != "https://":
                 Qt.QMessageBox.warning(self, '警告', "代理地址格式有误，请重新输入http或https开头的格式", Qt.QMessageBox.Yes)
                 return False
            find_index = proxyurl.find(':')
            if find_index == -1:
                Qt.QMessageBox.warning(self, '警告', "代理地址未指明端口号", Qt.QMessageBox.Yes)
                return False
            elif proxyurl[find_index + 1:].find(':') != -1:
                Qt.QMessageBox.warning(self, '警告', "代理地址格式有误，请重新输入", Qt.QMessageBox.Yes)
                return False
        if len(pwd) > 15:
            Qt.QMessageBox.warning(self, '警告', "密码过长，请重新输入", Qt.QMessageBox.Yes)
            return False
        self.parent.setproxy(proxyurl, card_num, pwd)
        Qt.QMessageBox.information(self, '设置', "您的代理已经设置成功, 请刷新获得验证码", Qt.QMessageBox.Yes)
        self.reject()

    def proxy_warn(self):
        if self.radiobutton.isChecked() == True: ##when you click , become true
            Qt.QMessageBox.warning(self, '警告', "您正在尝试更改代理地址，如果你不知道自己在做什么，请保留为默认值.\n当更改按钮为未选中状态时，自动还原为默认值", Qt.QMessageBox.Yes)
            self.proxyline.setEnabled(True)
        else:
            self.proxyline.setText(self.defaulturl)
            self.proxyline.setEnabled(False)



class scoreDialog(QtWidgets.QDialog): 
    def __init__(self, parent=None): 
        super(scoreDialog, self).__init__(parent)
        self.parent = parent
        self.initUI()  
        self.setWindowTitle("请按本科修读指南填写") 
        self.resize(240, 150)

    def initUI(self): 
        grid = QtWidgets.QGridLayout() 
        grid.addWidget(QtWidgets.QLabel("必修学分最低要求:"), 0, 0) 
        self.countSpineBox_total = QtWidgets.QDoubleSpinBox()
        self.countSpineBox_total.setRange(30, 100)
        #self.pathLineEdit = QtWidgets.QLineEdit() 
        #self.pathLineEdit.setFixedWidth(200) 
        #self.pathLineEdit.setText(os.getcwd())
        grid.addWidget(self.countSpineBox_total, 0, 1)
        #button = QtWidgets.QPushButton("更改") 
        #button.clicked.connect(self.changePath)
        grid.addWidget(QtWidgets.QLabel('(所有)选修最低要求:'), 1, 0)
        self.countSpineBox_total_elective = QtWidgets.QDoubleSpinBox()
        self.countSpineBox_total_elective.setRange(20, 100)
        grid.addWidget(self.countSpineBox_total_elective, 1, 1)

        grid.addWidget(QtWidgets.QLabel('专业选修最低要求:'), 2, 0)
        self.countSpineBox_elective = QtWidgets.QDoubleSpinBox()
        self.countSpineBox_elective.setRange(0, 150)
        grid.addWidget(self.countSpineBox_elective, 2, 1)
 
        cbx = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout()
        self.major_cbx = QtWidgets.QComboBox()
        self.major_cbx.addItem("普通理科选修", '0')
        self.major_cbx.addItem("普通文科选修", '1')

        hbox.addWidget(self.major_cbx)
        hbox.addWidget(QtWidgets.QLabel("最低要求"))
        cbx.setLayout(hbox)
        grid.addWidget(cbx, 3, 0)
        self.countSpineBox_normal = QtWidgets.QDoubleSpinBox()
        self.countSpineBox_normal.setRange(0, 50)
        grid.addWidget(self.countSpineBox_normal, 3, 1)
        #grid.addWidget(QtWidgets.QLabel("<font color='#ff0000'>包含Keywords.xml、Avatar,AvatarSet,Market.xls的路径</font>"), 1, 0, 1, 3) 
        #buttonBox.setOrientation(Qt.Horizontal)  # 设置为水平方向
        grid.addWidget(QtWidgets.QLabel("已获得其他学分:(没有则为0)\n创新学分,实践学分等"), 4, 0)
        self.countSpineBox_other = QtWidgets.QDoubleSpinBox()
        self.countSpineBox_other.setRange(0, 50)
        grid.addWidget(self.countSpineBox_other, 4, 1)

        myFont=QtGui.QFont()
        myFont.setBold(True)
        #myFont.setPixelSize(100)
        self.rest_require = QtWidgets.QLabel('\n')
        self.rest_require.setFont(myFont)
        self.rest_require_name = QtWidgets.QLabel('\n还需必修:')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.rest_require_name)
        hbox.addWidget(self.rest_require)
        grid.addLayout(hbox, 5, 0)
        
        self.rest_major_elective = QtWidgets.QLabel('\n')
        self.rest_major_elective.setFont(myFont)
        self.rest_major_elective_name = QtWidgets.QLabel('\n需专业选修:')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.rest_major_elective_name)
        hbox.addWidget(self.rest_major_elective)
        grid.addLayout(hbox, 5, 1)

        self.rest_normal_li_ke = QtWidgets.QLabel('')
        self.rest_normal_li_ke.setFont(myFont)
        self.rest_normal_li_ke_name = QtWidgets.QLabel('需理科选修:')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.rest_normal_li_ke_name)
        hbox.addWidget(self.rest_normal_li_ke)
        grid.addLayout(hbox, 6, 0)

        self.rest_normal_wen_ke = QtWidgets.QLabel('')
        self.rest_normal_wen_ke.setFont(myFont)
        self.rest_normal_wen_ke_name = QtWidgets.QLabel('需文科选修:')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.rest_normal_wen_ke_name)
        hbox.addWidget(self.rest_normal_wen_ke)
        grid.addLayout(hbox, 6, 1)

        self.total_gain = QtWidgets.QLabel('')
        self.total_gain.setFont(myFont)
        self.total_gain_name = QtWidgets.QLabel('已修满(含实践):')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.total_gain_name)
        hbox.addWidget(self.total_gain)
        grid.addLayout(hbox, 7, 0)

        self.total = QtWidgets.QLabel('')
        self.total.setFont(myFont)
        self.total_name = QtWidgets.QLabel('还需普通选修:')
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.total_name)
        hbox.addWidget(self.total)
        grid.addLayout(hbox, 7, 1)

        quitbtn = Qt.QPushButton('关闭窗口') 
        quitbtn.clicked.connect(self.reject)  # 取消
        btnLayout = Qt.QHBoxLayout()
        btnLayout.setSpacing(50)
        btnLayout.addWidget(quitbtn)
        grid.addLayout(btnLayout, 8, 0, 1, 2)

        self.setLayout(grid) 

    def compelete(self):
        self.major_cbx.prev_index = self.normal_need_index
        self.major_cbx.setCurrentIndex(self.normal_need_index)
        self.countSpineBox_total.setValue(self.require_need)
        self.countSpineBox_normal.setValue(self.normal_need)
        self.countSpineBox_other.setValue(self.other_need)
        self.countSpineBox_elective.setValue(self.major_need)
        self.countSpineBox_total_elective.setValue(self.elective_need)

        self.countSpineBox_total.valueChanged.connect(self.reset_value)
        self.countSpineBox_total_elective.valueChanged.connect(self.reset_value)
        self.countSpineBox_elective.valueChanged.connect(self.reset_value)
        self.countSpineBox_normal.valueChanged.connect(self.reset_value)
        self.countSpineBox_other.valueChanged.connect(self.reset_value)

    def major_cbx_index_change(self, index):
        if self.major_cbx.currentIndex() == 0:
            self.normal_need_index = 0
            self.major_cbx.prev_index = 0
        else:
            self.normal_need_index = 1
            self.major_cbx.prev_index = 1
        self.reset_value()

    def reset_value(self, float_number=0.0):
        require = self.countSpineBox_total.value()
        normal = self.countSpineBox_normal.value()
        other = self.countSpineBox_other.value()
        major = self.countSpineBox_elective.value()
        elective_total = self.countSpineBox_total_elective.value()

        rest_require = require - self.parent.response.require_credit
        rest_major = major - self.parent.response.major_elective_credit
        if self.major_cbx.currentIndex() == 0:
            rest_li_ke = normal - self.parent.response.li_ke_credit
            rest_wen_ke = '无要求'
        else:
            rest_wen_ke = normal - self.parent.response.wen_ke_credit
            rest_li_ke = '无要求'

        self.set_label(rest_require, self.rest_require_name, self.rest_require, "还需必修", "超出必修")
        self.set_label(rest_major, self.rest_major_elective_name, self.rest_major_elective, "需专业选修", "超专业选修")
        self.set_label(rest_li_ke, self.rest_normal_li_ke_name, self.rest_normal_li_ke, "需理科选修", "超理科选修")
        self.set_label(rest_wen_ke, self.rest_normal_wen_ke_name, self.rest_normal_wen_ke, "需文科选修", "超文科选修")
        self.set_label_positive(self.parent.response.total_credit + other, self.total_gain)
        if rest_wen_ke == '无要求' and rest_li_ke > 0:
            self.set_label(rest_li_ke, self.total_name, self.total, "还需普通选修:", "超过普通选修:")
        elif rest_li_ke == '无要求' and rest_wen_ke > 0:
            self.set_label(rest_wen_ke, self.total_name, self.total, "还需普通选修:", "超过普通选修:")
        total_normal = elective_total - major - self.parent.response.li_ke_credit - self.parent.response.wen_ke_credit
        self.set_label(total_normal, self.total_name, self.total, "还需普通选修:", "超过普通选修:")

        self.require_need = require
        self.normal_need = normal
        self.other_need = other
        self.major_need = major
        self.elective_need = elective_total

    def set_label(self, value, label_name, label_value, text_normal, text_exceed):
        if isinstance(value, str) or value >= 0:
            label_name.setText(text_normal)
            label_value.setText(str(value))
        else:
            label_name.setText(text_exceed)
            label_name.repaint()
            label_value.setText(str(abs(value)))
        label_name.repaint()
        label_value.repaint()

    def set_label_positive(self, value, label_value):
        label_value.setText(str(value))
        label_value.repaint()

class helpDialog(QtWidgets.QDialog): 
    def __init__(self, parent=None): 
        super(helpDialog, self).__init__(parent)
        self.parent = parent
        self.initUI()  
        self.setWindowTitle("使用帮助") 
        self.resize(240, 150)

    def initUI(self): 
        myFont=QtGui.QFont()
        myFont.setBold(True)
        #myFont.setPixelSize(100)
        grid = QtWidgets.QGridLayout()
        string = "您是第一次使用,请看一下说明, 下次在菜单栏点击帮助我就弹出来啦:\n" if self.parent.response.new_user_flag else "帮助说明, 下次在菜单栏点击帮助我就弹出来啦:\n"
        alabel = QtWidgets.QLabel(string)
        alabel.setFont(myFont)
        begin = 0
        grid.addWidget(alabel, begin, 0, 1, 2)
        alabel = QtWidgets.QLabel("1.我只想看一个学期的数据?")
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 1, 0, 1, 2)
        alabel = QtWidgets.QLabel("直接在开始和结束的菜单栏选取就可以了.\n比如开始选2016至2017第一学期，结束也选同样的2016至2017第一学期就好啦\n")
        grid.addWidget(alabel, begin + 2, 0, 1, 2)
        alabel = QtWidgets.QLabel("2.为什么我更改选项以后图像不会刷新?")
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 3, 0, 1, 2)
        alabel = QtWidgets.QLabel('你要点左上角的刷新图片哦！！！\n')
        grid.addWidget(alabel, begin + 4, 0, 1, 2)
        alabel = QtWidgets.QLabel("3.为什么要手动点击刷新图片?")
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 5, 0, 1, 2)
        alabel = QtWidgets.QLabel('使用的图像模块太大，嵌在程序里达到几百MB了，就不是"小工具"了\n图像要从云端获得, 网络的IO速度较慢，手动刷新会提升运行速度.\n')
        grid.addWidget(alabel, begin + 6, 0, 1, 2)
        alabel = QtWidgets.QLabel("4.那为什么我有时候变更数据,图片会自动刷新?")
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 7, 0, 1, 2)
        alabel = QtWidgets.QLabel('你每次获得的图像数据缓存在本地，程序会自动把上次缓存在本地的图片显示出来.\n如果你这次选择的学期区间和之前点击"刷新图片"时的一样，就自动从本地加载了\n如果选项和上次刷新图片时不一样，请点击"刷新图片"！\n')
        grid.addWidget(alabel, begin + 8, 0, 1, 2)
        alabel = QtWidgets.QLabel("5.我的必修课程统计有错误,我要改变必修课程的类型?")
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 9, 0, 1, 2)
        alabel = QtWidgets.QLabel('请在登陆时勾选"更改必修".\n')
        grid.addWidget(alabel, begin + 10, 0, 1, 2)
        alabel = QtWidgets.QLabel('6.为什么有些课程信息都不对?')
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 11, 0, 1, 2)
        alabel = QtWidgets.QLabel('登陆的是教务系统, 里面提供的课程信息较少,请手动修改,修改过一次后会自动记住\n')
        grid.addWidget(alabel, begin + 12, 0, 1, 2)
        alabel = QtWidgets.QLabel('7.我把成绩保存成txt打开后乱码?')
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 13, 0, 1, 2)
        alabel = QtWidgets.QLabel('nwindows下文本默认是以gbk编码文本,我是以utf8格式编码保存的.\n若打开乱码请在文本编辑器选择utf8格式编码\n')
        grid.addWidget(alabel, begin + 14, 0, 1, 2)        
        alabel = QtWidgets.QLabel('8.登陆窗口的"读取缓存"是什么意思?')
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 15, 0, 1, 2)
        alabel = QtWidgets.QLabel('程序在你刷新图像的时候会把数据保存到系统临时文件目录下.\n成功登陆下次会自动从该目录加载数据, 就不需要登陆教务系统.\n不需要从云端获取图像, 登陆速度会快很多呢！！\n')
        grid.addWidget(alabel, begin + 16, 0, 1, 2)
        alabel = QtWidgets.QLabel('9.为什么程序占用空间相对大?')
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 17, 0, 1, 2)
        alabel = QtWidgets.QLabel('本工具是用python写的,\npython打包成exe文件需要把python解释器一起打包. \n比起其他用C/C++写的exe自然大很多\n')
        grid.addWidget(alabel, begin + 18, 0, 1, 2)

        alabel = QtWidgets.QLabel('需要帮助?')
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 19, 0, 1, 2)
        alabel = QtWidgets.QLabel('zp0int@qq.com\n')
        grid.addWidget(alabel, begin + 20, 0, 1, 2)
        
        self.setLayout(grid)

class updateDialog(QtWidgets.QDialog): 
    def __init__(self, parent=None): 
        super(updateDialog, self).__init__(parent)
        self.parent = parent
        self.initUI()  
        self.cb = QtWidgets.QApplication.clipboard()
        self.setWindowTitle("您有新版本可以使用") 
        self.resize(240, 150)

    def initUI(self): 
        myFont=QtGui.QFont()
        myFont.setBold(True)
        #myFont.setPixelSize(100)
        begin = 0
        grid = QtWidgets.QGridLayout()
        message = self.parent.response.new_version.split("$$$")
        self.download_link = message[0]
        alabel = QtWidgets.QLabel("您有新版本可以使用, 下载地址:\n" + self.download_link)
        grid.addWidget(alabel, begin, 0)
        string = "支持以下特性:\n"
        if len(message) > 1:
            n = 1
            for i in message[1:]:
                string += str(n) + '.' + i + '\n'
        alabel = QtWidgets.QLabel(string)
        alabel.setFont(myFont)
        grid.addWidget(alabel, begin + 1, 0)
        copybtn = Qt.QPushButton('复制下载地址到剪切板')
        copybtn.clicked.connect(self.copy_to_board)
        grid.addWidget(copybtn)
        self.setLayout(grid)
    
    def copy_to_board(self):
         self.cb.setText(self.download_link)
         QtWidgets.QMessageBox.information(self, '复制成功', '成功将 ' + self.download_link + " 复制到系统剪切板")

    
"""
class userline_combox(QtWidgets.QComboBox):
    def __init__(self, parent):
        super(userline_combox, self).__init__(parent)
        self.parent = parent

    def mousePressEvent(self, QMouseEvent):
        super().mousePressEvent(QMouseEvent)
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.parent.change_current_password()

    def actionEvent(self, QActionEvent):
        super().actionEvent(QActionEvent)
        print('action')
"""
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = mywindow()
    window.show()

    sys.exit(app.exec_())