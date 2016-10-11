import sys
import os
import base64
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import Qt
from PyQt5 import QtCore
from shutil import copyfile
from re_szx import rrre
from szx_class import szx_edu_grade
from request import get_response_picture
from choose_class_data import school_data_class
from major_choose_class import get_major_choose_class
from dialog import scoreDialog, LoginDlg, helpDialog, updateDialog

class mywindow(QtWidgets.QMainWindow):
    def __init__(self, **kwargs):
        super(mywindow, self).__init__(**kwargs)
        self.force_clsoe = False
        if self.init_login() == 0:
            self.force_clsoe = True
            self.close()

    def closeEvent(self, event):
        if not self.force_clsoe:
            self.write_to_temp_file()
        event.accept()
        self.deleteLater() 
    
    def init_login(self):
        self.school_data = school_data_class()
        self.logindlg = LoginDlg(self)
        return self.logindlg.exec_()

    def continue_init(self):
        self.logindlg.setWindowTitle('正在初始化数据,请稍后...')
        if self.logindlg.cache_flag:
            self.message_list = self.logindlg.message_list
            self.szx_rrre = rrre(self.logindlg.SEMESTERS_LIST, html_flag = False)
            self.elective_class = get_major_choose_class(self, self.message_list, self.szx_rrre.SEMESTERS_LIST, self.school_data, retrieve = False, cache_flag = True)
            self.get_photo(0, len(self.szx_rrre.SEMESTERS_LIST) - 1)
        else:
            self.message_list = self.class_grade.get_mainmessage()
            #self.grade_html = self.class_grade.get_grade()
            self.szx_rrre = rrre(self.class_grade.get_grade(), html_flag = True)
            self.elective_class = get_major_choose_class(self, self.message_list, self.szx_rrre.SEMESTERS_LIST, self.school_data, retrieve = False) #elective
            self.logindlg.setWindowTitle('正在获取图表,请耐心等待并保持网络畅通....')
            self.photo_byte = self.class_grade.getphoto()  
            if self.get_photo(0, len(self.szx_rrre.SEMESTERS_LIST) - 1) == False:
                self.logindlg.setWindowTitle("深圳大学 学分统计工具登录窗口")
                return False
            self.elective_class = self.response.elective_class  #final elective
        self.refresh_dict()
        self.logindlg.setWindowTitle('正在显示窗口, 请稍后...')
        self.get_rest_dlg = scoreDialog(self)
        self.init_get_rest_score()
        self.helpdlg = helpDialog(self)
        self.resize(900, 600)
        self.init_menu()
        self.init_toolbar()
        self.init_layout() # normal
        ## move to the middle
        self.center()
        self.setWindowTitle('学分统计助手 V'+ "2.02" + ' (不清楚如何使用请点击帮助)')
        if not self.logindlg.cache_flag and not self.elective_class.retrieve:
            self.write_to_temp_file()
        self.logindlg.accept()
        self.statusBar().showMessage('加载完成辣~\(≧▽≦)/~啦啦啦！！！！')
        self.change = False
        self.show()
        if self.response.new_user_flag:
            self.helpdlg.exec_()
        if self.response.new_version != True:
            self.update_func()

    def update_func(self):
        self.updatedlg = updateDialog(self)
        self.updatedlg.exec_()

    def center(self):
        #qr = self.frameGeometry()
        #cp = QtWidgets.QDesktopWidget().availableGeometry().center()  
        #qr.moveCenter(cp)
        self.move(120, 70)

    def init_menu(self):
        self.menu_account = self.menuBar().addMenu('&账号')
        self.account_change_act = QtWidgets.QAction(QtGui.QIcon(''), '&切换账号', self, triggered = self.account_change)
        self.menu_account.addAction(self.account_change_act)
        self.account_logout_act = QtWidgets.QAction(QtGui.QIcon(''), '&注销', self, triggered = self.account_logout)
        self.menu_account.addAction(self.account_logout_act)
        self.menu_class = self.menuBar().addMenu('&选课')
        self.choose_class_act = QtWidgets.QAction(QtGui.QIcon(''), '自动选课', self, triggered = self.choose_class)
        self.menu_class.addAction(self.choose_class_act)
        self.menu_help = self.menuBar().addMenu('&帮助')
        self.help_act = QtWidgets.QAction(QtGui.QIcon(''), '查看帮助', self, triggered = self.help_func)
        self.menu_help.addAction(self.help_act)

    def choose_class(self):
        msg = QtWidgets.QMessageBox.information(self, '自动选课', '没时间，暂时不搞， 需要帮助联系zp0int@qq.com')

    def help_func(self):
        self.helpdlg.exec_()

    def account_change(self):
        self.account_logout()

    def account_logout(self):
        if self.change:
            self.write_to_temp_file()
        try:
            self.groupbox.hide()
            self.account_toolbar.hide()
            #self.menuBar().hide()
        except AttributeError:
            pass
        self.setCentralWidget(Qt.QLabel(''))
        self.logindlg = LoginDlg(self)
        if self.logindlg.exec_() == 0:
            self.force_clsoe = True
            self.close()

    def init_toolbar(self):
        self.account_toolbar = self.addToolBar('菜单栏')
        self.refresh_photo_act = QtWidgets.QAction(QtGui.QIcon(''), '&点击我来刷新右侧四张统计图片', self, triggered = self.refresh_photo)
        self.refresh_photo_act.setIconText('刷新图片')
        self.get_rest_score_act = QtWidgets.QAction(QtGui.QIcon(''), '&计算还需要多少学分可以毕业', self, triggered = self.get_rest_score)
        self.get_rest_score_act.setIconText('计算剩余学分')
        self.save_picture_act = QtWidgets.QAction(QtGui.QIcon(''), '&保存右侧四张统计图片和你的头像到指定目录', self, triggered = self.save_picture)
        self.save_picture_act.setIconText('保存图片')
        self.save_txt_act = QtWidgets.QAction(QtGui.QIcon(''), '&将你选中的学期范围内的成绩导出成txt\n(windows下乱码请用文本工具转换成utf8编码)', self, triggered = self.save_as_txt)
        self.save_txt_act.setIconText('导出成绩')
        self.account_toolbar.addAction(self.refresh_photo_act)
        self.account_toolbar.addAction(self.get_rest_score_act)
        self.account_toolbar.addAction(self.save_picture_act)
        self.account_toolbar.addAction(self.save_txt_act)

    def save_as_txt(self):
        begin = self.combox_begin.currentIndex()
        end = self.combox_end.currentIndex()
        def myalign_cn(str1, space, align = 'left'):
            length = len(str1.encode('gb2312'))
            space = space - length if space >=length else 0
            if align == 'left':
                str1 = str1 + ' ' * space
            elif align == 'right':
                str1 = ' '* space + str1
            elif align == 'center':
                str1 = ' ' * (space //2) +str1 + ' '* (space - space // 2)
            return str1

        def write_a_semester(f, semester_index):
            def get_longest_type(semester_index):
                if len(self.elective_class.normal_elective_list[0][semester_index]) > 0 or len(self.elective_class.normal_elective_list[1][semester_index]) > 0:
                    return 6
                if len(self.elective_class.major_choose_list[semester_index]) > 0:
                    return 4
                if len(self.elective_class.require_list[semester_index]) > 0:
                    return 2
                return 0
            max_for_courses = lambda courses, index : max(len(each_course[index].encode('gb2312')) for each_course in courses)
            longest_name = max_for_courses(self.szx_rrre.SEMESTERS_LIST[semester_index][4], 3)
            longest_num = max_for_courses(self.szx_rrre.SEMESTERS_LIST[semester_index][4], 2)
            longest_type = get_longest_type(semester_index)
            if longest_type == 0:
                f.write("%s :该学期无选课数据\n" % self.szx_rrre.SEMESTERS_LIST[semester_index][3])
            else:
                longest_type = 8 if longest_type * 2 < 8 else longest_type * 2 #gbk cn_width = en_width * 2
                format_str = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                f.write("%s:\n" % self.szx_rrre.SEMESTERS_LIST[semester_index][3])
                f.write(format_str % (myalign_cn("学期号", 6), myalign_cn("课程类别", longest_type), myalign_cn("课程名称", longest_name), myalign_cn("课程号", longest_num), myalign_cn("学分", 4), myalign_cn("取分", 4), myalign_cn("成绩", 4), myalign_cn("绩点", 4), myalign_cn("学分绩点", 4)))
                for each_list, type_str in (self.elective_class.require_list[semester_index], "必修"), (self.elective_class.major_choose_list[semester_index], "专业选修"), (self.elective_class.normal_elective_list[0][semester_index], "普通理科选修"), (self.elective_class.normal_elective_list[1][semester_index], "普通文科选修"):
                    for each_course in each_list:
                        f.write(format_str % (myalign_cn(each_course[1], 6), myalign_cn(type_str, longest_type), myalign_cn(each_course[3], longest_name), myalign_cn(each_course[2], longest_num), myalign_cn(each_course[5], 4), myalign_cn(each_course[6], 4), myalign_cn(each_course[7], 4), myalign_cn(each_course[8], 4), myalign_cn(each_course[9], 4)))
                temp = self.response.num_course_func(semester_index, semester_index + 1)
                f.write("\n该学期修了必修: %.1f科\t专业选修: %.1f科\t理科选修: %.1f科\t文科选修: %.1f科\t共修: %.1f科\t " % tuple(float(i) for i in temp[:-1]))
                f.write("平均绩点: %.4f\n" % float(temp[-1]))
                temp = self.response.credit_course_func(semester_index, semester_index + 1)
                f.write("该学期获得必修: %.1f分\t专业选修: %.1f分\t理科选修: %.1f分\t文科选修: %.1f分\t总共获得:%.1f分\n" % tuple([float(i) for i in temp[:-1]]))
        try:
            interval_str = self.szx_rrre.SEMESTERS_LIST[begin][3][:4] + self.szx_rrre.SEMESTERS_LIST[begin][3][-3] + '_' + self.szx_rrre.SEMESTERS_LIST[end][3][:4] + self.szx_rrre.SEMESTERS_LIST[end][3][-3]
            dir = os.getcwd() + "//" + str(self.message_list[1]) + '_' + interval_str + '_成绩学分.txt'
            directory, type_dialog = QtWidgets.QFileDialog.getSaveFileName(self, '请选择保存位置', dir, 'Txt Files(*.txt)')
            if not (directory and type_dialog):
                return False
            index = directory.find('.txt')
            if index != -1:
                init_dir = directory[:index] + '.txt'
            else:
                init_dir = dir
            with open(init_dir, 'w', encoding='utf8') as f:
                for semester_index in range(begin, end + 1):
                    write_a_semester(f, semester_index)
                    f.write('\n\n')
            QtWidgets.QMessageBox.information(self, '保存成功', self.szx_rrre.SEMESTERS_LIST[begin][3] + ' 到 ' + self.szx_rrre.SEMESTERS_LIST[end][3] + ' 的成绩数据已保存到您指定的目录!!!')

        except FileNotFoundError:
            return False

    def init_get_rest_score(self):
        if self.logindlg.cache_flag:
                message = self.logindlg.user_dict[self.logindlg.userlinecbx.currentText()][1]
                pair = message.split("@@@")[-1].split("$$$")
                self.get_rest_dlg.require_need = float(pair[3])
                self.get_rest_dlg.elective_need = float(pair[4])
                self.get_rest_dlg.major_need = float(pair[5])
                self.get_rest_dlg.normal_need_index = float(pair[6][0])
                self.get_rest_dlg.normal_need = float(pair[6][1:])
                self.get_rest_dlg.other_need = float(pair[7])
        else:
            self.get_rest_dlg.require_need = self.response.require_credit - 30 if self.response.require_credit - 30 > 0 else 0
            self.get_rest_dlg.elective_need = self.response.li_ke_credit + self.response.wen_ke_credit + self.response.major_elective_credit - 40 if self.response.li_ke_credit + self.response.wen_ke_credit + self.response.major_elective_credit - 40 > 0 else 0
            self.get_rest_dlg.major_need = self.response.major_elective_credit - 10 if self.response.major_elective_credit - 10 > 0 else 0
            self.get_rest_dlg.normal_need_index = 0
            self.get_rest_dlg.normal_need = min(self.response.wen_ke_credit, self.response.li_ke_credit) - 10 if min(self.response.wen_ke_credit, self.response.li_ke_credit) - 10 > 0 else 0
            self.get_rest_dlg.other_need = 0
        self.get_rest_dlg.compelete()
        self.get_rest_dlg.reset_value()

    def get_rest_score(self):
        self.get_rest_dlg.exec_()

    def save_picture(self):
        try:
            begin = self.combox_begin.currentIndex()
            end = self.combox_end.currentIndex()
            interval_str = self.szx_rrre.SEMESTERS_LIST[begin][3][:4] + self.szx_rrre.SEMESTERS_LIST[begin][3][-3] + '_' + self.szx_rrre.SEMESTERS_LIST[end][3][:4] + self.szx_rrre.SEMESTERS_LIST[end][3][-3]
            directory, type_dialog = QtWidgets.QFileDialog.getSaveFileName(self, '请选择保存位置', os.getcwd() + "//" + str(self.message_list[1]), 'Images (*.png *.xpm *.jpg)')
            if not (directory and type_dialog):
                return False
            name_list = [interval_str + "_总成绩统计图", interval_str + "_总选课情况统计图", interval_str + "_成绩与学分柱状图", interval_str + "_各学期成绩分布图", "_照片"]
            try:
                init_dir = directory[:directory.index('.')]
            except ValueError:
                init_dir = directory
                msg = QtWidgets.QMessageBox.information(self, '文件名称格式错误', '您输入的目录有误，将自动保存到如下目录\n %s' % os.getcwd() + "//")
            picture_list = [self.photo_pie_byte0, self.photo_pie_pyte1, self.photo_bar_byte, self.photo_radar_byte, self.photo_byte]
            for i in range(5):
                directory = init_dir + name_list[i] + '.png' if i == 0 else init_dir + name_list[i] + '.jpg'
                with open(directory, 'wb') as f:
                    f.write(picture_list[i])
        except FileNotFoundError:
            return False
        except AttributeError:
            photo_dir = self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_pie.png', self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_radar.png', self.logindlg.dir + '\\' + self.message_list[0] +  '_' + interval_str + '_pie1.png', self.logindlg.dir + '\\' + self.message_list[0] +  '_' + interval_str + '_bar.png', self.logindlg.photodir
            for i in range(5):
                directory = init_dir + name_list[i] + '.png' if i == 0 else init_dir + name_list[i] + '.jpg'
                copyfile(photo_dir[i], directory)
        self.statusBar().showMessage('保存成功！！！')
        QtWidgets.QMessageBox.information(self, '保存成功', '您当前窗口的图片已保存到您指定的目录!!!')

    def refresh_photo(self):
        if not self.change:
            msg = QtWidgets.QMessageBox.warning(self, '错误尝试', '您未做任何改变哦亲(づ￣3￣)づ╭❤～, 请更改参数后按重新统计!!!')
            return False
        self.elective_class.retrieve = True
        self.statusBar().showMessage('正在获取图片,请耐心等待......')
        self.setWindowTitle('正在获取图片,请耐心等待......')
        self.get_photo(self.combox_begin.currentIndex(), self.combox_end.currentIndex())        
        self.setWindowTitle('学分统计助手 V'+ "2.02" + ' (不清楚如何使用请点击帮助)')
        self.write_to_temp_file()
        self.change = False
        self.statusBar().showMessage('加载完成辣~\(≧▽≦)/~啦啦啦！！！！')

    def get_photo(self, start_index, end_index):
        if self.logindlg.cache_flag and not self.elective_class.retrieve:
            self.response = get_response_picture(self.szx_rrre, self.elective_class, cache_flag=True)
        else:
            try:
                if self.elective_class.retrieve:
                    self.response.refresh_photo(start_index, end_index)
                else:
                    self.response = get_response_picture(self.szx_rrre, self.elective_class)
                self.photo_pie_byte0 = self.response.pie_chart0()
                self.photo_pie_pyte1 = self.response.pie_chart1()
                self.photo_bar_byte = self.response.bar_chart()
                self.photo_radar_byte = self.response.radar_chart()
            except SyntaxError:
                msg = QtWidgets.QMessageBox.critical(self, '网络错误', '请检查网络连接(或服务器异常)')
                return False
            except UnicodeDecodeError:
                msg = QtWidgets.QMessageBox.critical(self, '网络错误', '请检查校网络连接或校内网设置\n若网络连接正常,请检查代理设置')
                return False
        self.load_photo(start_index, end_index)
        if self.elective_class.retrieve and self.response.new_version != True:
            self.update_func()

    def load_photo(self, start_index, end_index):
        if not self.elective_class.retrieve:
            self.photo_label_pie, self.photo_label_radar, self.photo_label_pie1, self.photo_label_bar, self.personal_photo_label = QtWidgets.QLabel(), QtWidgets.QLabel(), QtWidgets.QLabel(), QtWidgets.QLabel(), QtWidgets.QLabel()
        if self.logindlg.cache_flag and not self.elective_class.retrieve:
            i = 0
            interval_str = self.szx_rrre.SEMESTERS_LIST[start_index][3][:4] + self.szx_rrre.SEMESTERS_LIST[start_index][3][-3] + '_' + self.szx_rrre.SEMESTERS_LIST[end_index][3][:4] + self.szx_rrre.SEMESTERS_LIST[end_index][3][-3]
            for photo_label, photo_dir in (self.personal_photo_label, self.logindlg.photodir), (self.photo_label_pie, self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_pie.png'), (self.photo_label_radar, self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_radar.png'), (self.photo_label_pie1, self.logindlg.dir + '\\' + self.message_list[0] +  '_' + interval_str + '_pie1.png'), (self.photo_label_bar, self.logindlg.dir + '\\' + self.message_list[0] +  '_' + interval_str + '_bar.png'):
                bias = -50 if i == 0 else 0
                photo = Qt.QImage(photo_dir)
                photo_label.setPixmap(Qt.QPixmap.fromImage(photo).scaled(300 + bias, 300 + bias, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation))
                i += 1
        else:
            if not self.elective_class.retrieve:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(QtCore.QByteArray(self.photo_byte))
                self.personal_photo_label.setPixmap(pixmap.scaled(250, 250, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation))

            for label, byte in (self.photo_label_pie, self.photo_pie_byte0), (self.photo_label_radar, self.photo_radar_byte), (self.photo_label_pie1, self.photo_pie_pyte1), (self.photo_label_bar, self.photo_bar_byte):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(QtCore.QByteArray(byte))
                label.setPixmap(pixmap.scaled(300, 300, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation))
                if self.elective_class.retrieve:
                    label.repaint()

    def init_layout(self):
        self.myFont=QtGui.QFont()
        self.myFont.setBold(True)
        vbox = QtWidgets.QVBoxLayout()
        
        ############grid##############
        self.grid = QtWidgets.QGridLayout()
        grid0 = QtWidgets.QGridLayout()
        #photo
        #photo = Qt.QImage('C:/Users/sunset/Desktop/photo.jpg')

        grid0.addWidget(self.personal_photo_label, 0, 0)
        """
        photo = Qt.QImage('C:/Users/sunset/Desktop/photo.jpg')
        photo_label = QtWidgets.QLabel()
        photo_label.setPixmap(Qt.QPixmap.fromImage(photo).scaled(250, 250, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation))
        grid0.addWidget(photo_label, 0, 0)
        """
        #photo_label.setPixmap(Qt.QPixmap.fromImage(photo).scaled(150, 150, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation))
        #photo_label.setPixmap(Qt.QPixmap('C:/Users/z/Desktop/photo.jpg'))
        #grid.addWidget(photo_label, 0, 0, 4, 1)
        #photo done
        #message_list
        #0--->userid  1--->name 2--->sex 3--->birth 4--->ID 
        #5--->nation   6--->grade i.e. 2013  7-->学院  8--->major
        #9--->class   10--->phone_num   11--->zip code  12--->address
        #13--->parent_name 14--->home_phone_num
        grid1 = QtWidgets.QGridLayout()
        grid1.addWidget(QtWidgets.QLabel('姓名：'), 0, 0)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[1]), 0, 1) 
        grid1.addWidget(QtWidgets.QLabel('学号：'), 0, 2)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[0]), 0, 3) #
        grid1.addWidget(QtWidgets.QLabel('性别：'), 1, 0)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[2]), 1, 1) #
        grid1.addWidget(QtWidgets.QLabel('民族：'), 1, 2)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[5]), 1, 3)  #
        grid1.addWidget(QtWidgets.QLabel('出生日期：'), 2, 0)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[3]), 2, 1) #
        grid1.addWidget(QtWidgets.QLabel('星座：'), 2, 2)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[15]), 2, 3)
        grid1.addWidget(QtWidgets.QLabel('学院：'), 3, 0)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[7]), 3, 1) #
        grid1.addWidget(QtWidgets.QLabel('主修专业：'), 3, 2)
        grid1.addWidget(QtWidgets.QLabel(self.message_list[8]), 3, 3)   #
        ################################
        self.combox_begin, self.combox_end = self.create_combox_begin_end()
        grid1.addWidget(Qt.QLabel('起始学期：'), 4, 0)
        grid1.addWidget(self.combox_begin, 4, 1)
        grid1.addWidget(Qt.QLabel('结束学期：'),4, 2)
        grid1.addWidget(self.combox_end, 4, 3)
                
        grid1.setColumnStretch(0, 10)
        grid1.setColumnStretch(1, 15)
        grid1.setColumnStretch(2, 10)
        grid1.setColumnStretch(3, 15)
        #vbox.addWidget(grid2Widget)
        ########grid2 done###############
        grid1Widget = QtWidgets.QWidget()
        grid1Widget.setLayout(grid1)
        grid0.addWidget(grid1Widget, 0, 1)
        grid0Widget = QtWidgets.QWidget()
        grid0Widget.setLayout(grid0)
        grid0.setColumnStretch(0, 10)
        grid0.setColumnStretch(0, 15)
        self.grid.addWidget(grid0Widget, 0, 0)

        self.grid.addWidget(self.photo_label_pie, 0, 1)        
        self.grid.addWidget(self.photo_label_radar, 0, 2)

        """
        gridWidget = QtWidgets.QWidget()
        gridWidget.setLayout(grid)
        """
        ########grid done###############
        #################################
        ####QTableWidget begin##########
        self.create_table(0, len(self.szx_rrre.SEMESTERS_LIST))
        #self.set_table_widget(0, len(self.szx_rrre.SEMESTERS_LIST))
        self.grid.addWidget(self.tw, 1, 0)
        self.grid.addWidget(self.photo_label_bar, 1, 1)               
        self.grid.addWidget(self.photo_label_pie1, 1, 2)

        self.grid.setColumnStretch(0, 10)
        self.grid.setColumnStretch(1, 15)
        self.grid.setColumnStretch(2, 15)
        gridWidget = QtWidgets.QWidget()
        gridWidget.setLayout(self.grid)
        vbox.addWidget(gridWidget)
        #vbox.addWidget(tw)
        ####QTableWidget end##########
        ########grid3 begin#############
        grid =  QtWidgets.QGridLayout()
        self.total_label = Qt.QLabel(str(round(self.response.total_credit, 2)))
        
        self.require_label = Qt.QLabel(str(round(self.response.require_credit, 2)))
        self.li_ke_label = Qt.QLabel(str(round(self.response.li_ke_credit, 2)))
        self.wen_ke_label = Qt.QLabel(str(round(self.response.wen_ke_credit, 2)))
        self.major_require_label = Qt.QLabel(str(round(self.response.major_elective_credit, 2)))
        self.get_avg_label_name = lambda : self.szx_rrre.SEMESTERS_LIST[self.combox_begin.currentIndex()][3][:4] + self.szx_rrre.SEMESTERS_LIST[self.combox_begin.currentIndex()][3][-3] + '-' + self.szx_rrre.SEMESTERS_LIST[self.combox_end.currentIndex()][3][:4] + self.szx_rrre.SEMESTERS_LIST[self.combox_end.currentIndex()][3][-3] +' 的平均绩点：'
        self.avg_gpa_label_name = Qt.QLabel(self.get_avg_label_name())
        self.avg_gpa_label_credit = Qt.QLabel(str(round(self.response.ave_gpa, 4)))
        
        total_label_name = Qt.QLabel('总共取得学分：')
        require_label_name = Qt.QLabel('其中必修：')
        li_ke_label_name = Qt.QLabel('普通理科选修：')
        wen_ke_label_name = Qt.QLabel('普通文科选修：')
        major_require_label_name = Qt.QLabel('专业选修：')
        for each_label in self.total_label, self.require_label, self.li_ke_label, self.wen_ke_label, self.major_require_label, self.avg_gpa_label_name, self.avg_gpa_label_credit, total_label_name, require_label_name, li_ke_label_name, wen_ke_label_name, major_require_label_name:
            each_label.setFont(self.myFont)
        grid.addWidget(total_label_name, 0, 0)
        grid.addWidget(self.total_label, 0, 1)
        grid.addWidget(require_label_name, 0, 2)
        grid.addWidget(self.require_label, 0, 3)   
        grid.addWidget(li_ke_label_name, 0, 4)
        grid.addWidget(self.li_ke_label, 0, 5)
        grid.addWidget(wen_ke_label_name, 0, 6)
        grid.addWidget(self.wen_ke_label, 0, 7)
        grid.addWidget(major_require_label_name, 0, 8)
        grid.addWidget(self.major_require_label, 0, 9)
        grid.addWidget(self.avg_gpa_label_name, 0, 10)
        grid.addWidget(self.avg_gpa_label_credit, 0, 11)
        #str(round(self.szx_rrre.ave_gpa, 2))
        self.label_dict = {0 : self.major_require_label, 1 : self.li_ke_label, 2 : self.wen_ke_label, 3 : self.require_label}
        grid.addWidget(Qt.QLabel('辅修专业所在学院：'), 0, 12)
        self.combox_second_major = QtWidgets.QComboBox()
        self.combox_second_major.addItem('无辅修专业', '0')
        i = 1
        for name_str, cnname in self.school_data.name_dict.items():
            self.combox_second_major.addItem(cnname, name_str)
            self.school_data.index_dict[name_str] = i
            i += 1
        if self.elective_class.major_elective_en_num == '0':
            index = 0
        else:
            index = self.school_data.index_dict[self.elective_class.major_elective_en_num]

        self.combox_second_major.setCurrentIndex(index)
        grid.addWidget(self.combox_second_major, 0, 13)
        #grid.addWidget(Qt.QLabel('(选择完成请点击左上角"重新统计"按钮刷新结果)'), 0, 12)        

        gridWidget = QtWidgets.QWidget()
        gridWidget.setLayout(grid)
        vbox.addWidget(gridWidget)
        ########grid3 done#############
        self.groupbox = QtWidgets.QWidget()
        self.groupbox.setLayout(vbox)
        self.setCentralWidget(self.groupbox)   

    def write_to_temp_file(self):
        interval_str = self.szx_rrre.SEMESTERS_LIST[self.combox_begin.currentIndex()][3][:4] + self.szx_rrre.SEMESTERS_LIST[self.combox_begin.currentIndex()][3][-3] + '_' + self.szx_rrre.SEMESTERS_LIST[self.combox_end.currentIndex()][3][:4] + self.szx_rrre.SEMESTERS_LIST[self.combox_end.currentIndex()][3][-3]
        photodir = self.logindlg.dir + "\\" + self.message_list[0] + '.jpg'
        if not os.path.isdir(self.logindlg.dir):
            os.mkdir(self.logindlg.dir)
        try:
            photos = (self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_pie.png', self.photo_pie_byte0), (self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_radar.png', self.photo_radar_byte), (self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_pie1.png', self.photo_pie_pyte1), (self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_bar.png', self.photo_bar_byte)
            if not os.path.isfile(photodir):
                with open(photodir, 'wb') as f:
                    f.write(self.photo_byte)
            for each_dir, byte in photos:
                with open(each_dir, 'wb') as f:
                    f.write(byte)
        except AttributeError: # old usr never press retrieve
            pass
        string = str(self.message_list[0]) + "!!!" + str(int(self.logindlg.remember_pwd_flag)) + str(int(self.logindlg.auto_login_flag)) + str(int(self.logindlg.remember_proxy_flag)) + str(self.message_list[16]) + "###" + str(self.message_list) + "@@@" + str(self.szx_rrre.SEMESTERS_LIST) + "@@@" + str(self.elective_class.require_list) + "@@@" + str(self.elective_class.major_choose_list) + "@@@" + str(self.elective_class.normal_elective_list) + "@@@" + str(self.logindlg.proxy_usr) +  "$$$" + str(self.logindlg.proxy_pwd) + '$$$' + str(self.logindlg.proxy_url) + '$$$' + str(self.get_rest_dlg.require_need) + '$$$'  + str(self.get_rest_dlg.elective_need) + '$$$' + str(self.get_rest_dlg.major_need) + '$$$' + str(int(self.get_rest_dlg.normal_need_index)) + str(self.get_rest_dlg.normal_need) + '$$$' + str(self.get_rest_dlg.other_need)
        encrypt = base64.b64encode(string.encode('utf8'))
        with open(self.logindlg.file_dir, 'w', encoding='utf8') as f:
            f.write(encrypt.decode('utf8') + '\n')
            for usr, pair in self.logindlg.user_dict.items():
                if usr != str(self.message_list[0]):
                    string = usr + "!!!" + pair[0] + "###" + pair[1]
                    encrypt = base64.b64encode(string.encode('utf8'))
                    f.write(encrypt.decode('utf8') + '\n')

    def create_table(self, start_index, stop_index_plus_one):
        def add_to_table(tw, course_list, course_type, semester_index): #course type ===> 0:专业选修   1:普通理科选修   2:普通文科选修   3:必修
            nonlocal y
            for each_course in course_list:
                for index in range(len_xlist):
                    if index == 2 and (course_type != 3 or self.logindlg.require_flag):
                        v = QtWidgets.QComboBox()
                        for i in range_len:
                            v.addItem(self.type_dict[i])
                        v.semester_index = semester_index
                        v.old_type_index = course_type
                        v.course = each_course
                        v.setCurrentIndex(course_type)
                        v.currentIndexChanged.connect(self.signalMapper.map)
                        self.signalMapper.setMapping(v, v)
                        tw.setCellWidget(y, index, v)
                    else:
                        v = QtWidgets.QTableWidgetItem(each_course[xlist[index]])
                        v.setTextAlignment(Qt.Qt.AlignCenter)
                        tw.setItem(y, index, v)
                y += 1

        if not self.elective_class.retrieve:
            self.type_dict = {0 : "专业选修", 1 : "普通理科选修", 2 : "普通文科选修", 3 : "必修"}
            self.elective_dict = {0 : self.elective_class.major_choose_list, 1 : self.elective_class.normal_elective_list[0], 2 : self.elective_class.normal_elective_list[1], 3 : self.elective_class.require_list} 
        self.signalMapper = QtCore.QSignalMapper(self)
        self.signalMapper.mapped[QtWidgets.QWidget].connect(self.course_change_current_index)
        tw = QtWidgets.QTableWidget(self.response.current_total_count, 8)
        tw.setHorizontalHeaderLabels(['学期号', '课程名','类别','取得学分', '绩点', '成绩','学分绩点','课程号'])
        xlist = [1, 3, 4, 6, 8, 7, 9, 2]
        len_xlist = len(xlist)
        range_len = range(4) if self.logindlg.require_flag else range(3)
        y = 0
        for semester_index in range(start_index, stop_index_plus_one):
            add_to_table(tw, self.elective_class.major_choose_list[semester_index], 0, semester_index)
            add_to_table(tw, self.elective_class.normal_elective_list[0][semester_index], 1, semester_index)
            add_to_table(tw, self.elective_class.normal_elective_list[1][semester_index], 2, semester_index)
            add_to_table(tw, self.elective_class.require_list[semester_index], 3, semester_index)

        tw.setSortingEnabled(True)
        tw.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw = tw

    @QtCore.pyqtSlot(QtWidgets.QWidget)
    def course_change_current_index(self, cbx_obj):
        self.change = True
        old_type_index = cbx_obj.old_type_index
        new_type_index = cbx_obj.currentIndex()
        if new_type_index == old_type_index:
            return False
        semester_index = cbx_obj.semester_index
        #update
        self.update_score(old_type_index, new_type_index, cbx_obj.course)
        self.elective_dict[new_type_index][semester_index].append(cbx_obj.course) #append
        self.elective_dict[old_type_index][semester_index].remove(cbx_obj.course) #del
        #update cbx
        cbx_obj.old_type_index = new_type_index

    def update_score(self, old_type_index, new_type_index, course):
        self.count_dict[old_type_index] -= 1
        self.count_dict[new_type_index] += 1
        self.current_count_dict[old_type_index] -= 1
        self.current_count_dict[new_type_index] += 1
        self.credit_dict[old_type_index] -= float(course[6])
        self.credit_dict[new_type_index] += float(course[6])
        self.current_credit_dict[old_type_index] -= float(course[6])
        self.current_credit_dict[new_type_index] += float(course[6])
        self.label_dict[old_type_index].setText(str(round(self.current_credit_dict[old_type_index], 2)))
        self.label_dict[old_type_index].repaint()
        self.label_dict[new_type_index].setText(str(round(self.current_credit_dict[new_type_index], 2)))
        self.label_dict[new_type_index].repaint()

    def create_combox_begin_end(self):
        combox_begin, combox_end = QtWidgets.QComboBox(), QtWidgets.QComboBox()
        for each_semester_list in self.szx_rrre.SEMESTERS_LIST:
            combox_begin.addItem(each_semester_list[3], each_semester_list[3][:4] + each_semester_list[3][-3])
            combox_end.addItem(each_semester_list[3],  each_semester_list[3][:4] + each_semester_list[3][-3])
        combox_begin.prev_index = 0
        combox_begin.setCurrentIndex(0)
        combox_end.setCurrentIndex(len(self.szx_rrre.SEMESTERS_LIST) - 1)
        combox_end.prev_index = len(self.szx_rrre.SEMESTERS_LIST) - 1
        combox_begin.currentIndexChanged.connect(self.combox_index_change)
        combox_end.currentIndexChanged.connect(self.combox_index_change)
        return combox_begin, combox_end

    def combox_index_change(self, new_index):
        new_begin_index = self.combox_begin.currentIndex()
        new_end_index = self.combox_end.currentIndex()
        if new_begin_index == self.combox_begin.prev_index and new_end_index == self.combox_end.prev_index:
            return False
        if new_begin_index > new_end_index:
            QtWidgets.QMessageBox.critical(self, '选择错误', '起始学期在结束学期之后，请重新选择！')
            if new_begin_index != self.combox_begin.prev_index:
                self.combox_begin.setCurrentIndex(self.combox_begin.prev_index)
            elif new_end_index != self.combox_end.prev_index:
                self.combox_end.setCurrentIndex(self.combox_end.prev_index)
            return False
        self.change = True #
        self.response.refresh_current_value(new_begin_index, new_end_index + 1)
        self.refresh_dict()
        #self.tw.clear()
        y = 0
        self.tw.clear()
        self.grid.removeWidget(self.tw)
        #create a new one, use the old one remains some bug
        self.create_table(new_begin_index, new_end_index + 1)
        self.grid.addWidget(self.tw, 1, 0)

        self.total_label.setText(str(round(self.response.current_total_credit, 2)))
        self.total_label.repaint()
        self.require_label.setText(str(round(self.response.current_require_credit, 2)))
        self.require_label.repaint()
        self.li_ke_label.setText(str(round(self.response.current_li_ke_credit, 2)))
        self.li_ke_label.repaint()
        self.wen_ke_label.setText(str(round(self.response.current_wen_ke_credit, 2)))
        self.wen_ke_label.repaint()
        self.major_require_label.setText(str(round(self.response.current_major_elective_credit, 2)))
        self.major_require_label.repaint()
        self.avg_gpa_label_name.setText(self.get_avg_label_name())
        self.avg_gpa_label_name.repaint()
        self.avg_gpa_label_credit.setText(str(round(self.response.current_ave_gpa, 4)))
        self.avg_gpa_label_credit.repaint()

        self.combox_begin.prev_index = new_begin_index
        self.combox_end.prev_index = new_end_index

        interval_str = self.szx_rrre.SEMESTERS_LIST[self.combox_begin.currentIndex()][3][:4] + self.szx_rrre.SEMESTERS_LIST[self.combox_begin.currentIndex()][3][-3] + '_' + self.szx_rrre.SEMESTERS_LIST[self.combox_end.currentIndex()][3][:4] + self.szx_rrre.SEMESTERS_LIST[self.combox_end.currentIndex()][3][-3]
        if os.path.isfile(self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_pie.png'):
            for photo_label, photo_dir in (self.photo_label_pie, self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_pie.png'), (self.photo_label_radar, self.logindlg.dir + '\\' + self.message_list[0] + '_' + interval_str + '_radar.png'), (self.photo_label_pie1, self.logindlg.dir + '\\' + self.message_list[0] +  '_' + interval_str + '_pie1.png'), (self.photo_label_bar, self.logindlg.dir + '\\' + self.message_list[0] +  '_' + interval_str + '_bar.png'):
                photo = Qt.QImage(photo_dir)
                photo_label.setPixmap(Qt.QPixmap.fromImage(photo).scaled(300, 300, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation))
                photo_label.repaint()

    def refresh_dict(self):
        self.count_dict = {0 : self.response.major_elective_count, 1 : self.response.li_ke_count, 2 : self.response.wen_ke_count, 3 : self.response.require_count}
        self.current_count_dict = {0 : self.response.current_major_elective_count, 1 : self.response.current_li_ke_count, 2 : self.response.current_wen_ke_count, 3 : self.response.current_require_count}
        self.credit_dict = {0 : self.response.major_elective_credit, 1 : self.response.li_ke_credit, 2 : self.response.wen_ke_credit, 3 : self.response.require_credit}
        self.current_credit_dict = {0 : self.response.current_major_elective_credit, 1 : self.response.current_li_ke_credit, 2 : self.response.current_wen_ke_credit, 3 : self.response.current_require_credit}

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = mywindow()

    sys.exit(app.exec_())
