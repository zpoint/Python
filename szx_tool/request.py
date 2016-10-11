import urllib.request
import urllib.parse
from copy import deepcopy
import base64
class get_response_picture(object):
    def __init__(self, rrre, elective_class, cache_flag=False):
        self.rrre = rrre
        self.elective_class = elective_class
        self.new_user_flag = False
        self.new_version = True
        #data_grade_list ---> serve side generate
        self.cache_flag = cache_flag
        self.value = {
                          'userid' : str(self.elective_class.message_list[0]),
                          'version' : str(self.rrre.version),
                          '0' : 'self.SEMESTERS_LIST = ' + str(self.rrre.SEMESTERS_LIST),
                          '1' : 'self.version = ' + str(self.rrre.version),

                          '2' : 'self.major_choose_list = ' + str(self.elective_class.major_choose_list),
                          '3' : 'self.require_list = ' + str(self.elective_class.require_list),
                          '4' : 'self.normal_elective_list = ' + str(self.elective_class.normal_elective_list),
                          '5' : 'self.message_list = ' + str(self.elective_class.message_list),
                          '6' : 'self.major_elective_en_num = ' + str(self.elective_class.major_elective_en_num),
                          '7' : 'self.retrieve = ' + str(self.elective_class.retrieve),
                          '8' : 'self.require_flag = ' + str(self.elective_class.require_flag)
            }
        self.encode_value()

        if not cache_flag:
            self.request_and_handle()
        self.require_count, self.major_elective_count, self.li_ke_count, self.wen_ke_count, self.total_count, self.ave_gpa = self.num_course_func(0, len(self.rrre.SEMESTERS_LIST))
        self.current_require_count, self.current_major_elective_count, self.current_li_ke_count, self.current_wen_ke_count, self.current_total_count, self.current_ave_gpa = self.require_count, self.major_elective_count, self.li_ke_count, self.wen_ke_count, self.total_count, self.ave_gpa
        self.require_credit, self.major_elective_credit, self.li_ke_credit, self.wen_ke_credit, self.total_credit, self.semester_type_credit_list = self.credit_course_func(0, len(self.rrre.SEMESTERS_LIST))
        self.current_require_credit, self.current_major_elective_credit, self.current_li_ke_credit, self.current_wen_ke_credit, self.current_total_credit = self.require_credit, self.major_elective_credit, self.li_ke_credit, self.wen_ke_credit, self.total_credit
        self.current_semester_type_credit_list = deepcopy(self.semester_type_credit_list)
    
    def refresh_current_value(self, start_index, stop_index_plus_one):
        self.current_require_count, self.current_major_elective_count, self.current_li_ke_count, self.current_wen_ke_count, self.current_total_count, self.current_ave_gpa = self.num_course_func(start_index, stop_index_plus_one)
        self.current_require_credit, self.current_major_elective_credit, self.current_li_ke_credit, self.current_wen_ke_credit, self.current_total_credit, self.current_semester_type_credit_list = self.credit_course_func(start_index, stop_index_plus_one)

    def request_and_handle(self):        
        url = 'http://42.96.159.6/szx/szx.php'
        data = urllib.parse.urlencode(self.value)
        data = data.encode('ascii')
        req = urllib.request.Request(url)
        req.add_header('Referer', 'grade_tool')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
        response = urllib.request.urlopen(req, data=data)
        response_content = response.readlines()
        self.response_list = []
        for line in response_content:
            self.response_list.append(line.decode('utf8').strip())
        other_list = self.response_list[-1].split('#####')
        if not self.elective_class.retrieve:
            if str(other_list[5]) == 'True':
                self.new_version = True
            else:
                self.new_version = str(other_list[5])
            exec ('self.elective_class.normal_elective_list[0] = ' + str(other_list[0]))
            exec ('self.elective_class.normal_elective_list[1] = ' + str(other_list[1]))
            exec ('self.elective_class.major_choose_list = ' + str(other_list[2]))
            exec ('self.elective_class.require_list = ' + str(other_list[3]))
            exec ("self.elective_class.major_elective_en_num = '" + str(other_list[4]) + "'")
            exec ("self.new_user_flag = " + str(other_list[6]))
            """
            print ('\nGET\n')
            print ('self.major_choose_list: ', self.elective_class.major_choose_list)
            for i in self.elective_class.major_choose_list:
                for j in i:
                    print (j)
            print ('理科选修')
            for i in self.elective_class.normal_elective_list[0]:
                for j in i:
                    print (j)
            print ('文科选修')
            for i in self.elective_class.normal_elective_list[1]:
                for j in i:
                    print (j)
            print ('self.elective_class.major_elective_en_num\n', self.elective_class.major_elective_en_num)
            print ('self.new_version\n', self.new_version)
            """
        else:
            if str(other_list[0]) == 'True':
                self.new_version = True
            else:
                self.new_version = str(other_list[0])
                
    def refresh_photo(self, start_index, stop_index):
        self.value = {
                          'userid' : str(self.elective_class.message_list[0]),
                          'version' : str(self.rrre.version),
                          '0' : 'self.SEMESTERS_LIST = ' + str(self.rrre.SEMESTERS_LIST[start_index : stop_index + 1]),
                          '1' : 'self.version = ' + str(self.rrre.version),

                          '2' : 'self.major_choose_list = ' + str(self.elective_class.major_choose_list[start_index : stop_index + 1]),
                          '3' : 'self.require_list = ' + str(self.elective_class.require_list[start_index : stop_index + 1]),
                          '4' : 'self.normal_elective_list = ' + str([self.elective_class.normal_elective_list[0][start_index : stop_index + 1], self.elective_class.normal_elective_list[1][start_index : stop_index + 1]]),
                          '5' : 'self.message_list = ' + str(self.elective_class.message_list),
                          '6' : 'self.major_elective_en_num = ' + str(self.elective_class.major_elective_en_num),
                          '7' : 'self.retrieve = ' + str(self.elective_class.retrieve),
                          '8' : 'self.require_flag = ' + str(self.elective_class.require_flag)
            }
        """
        print ('\nPOST\n')
        print("retrieve:", self.elective_class.retrieve)		
        print ('self.major_choose_list:')
        for list in self.elective_class.major_choose_list[start_index : stop_index + 1]:
            for j in list:
                print (j)
        print ('理科选修')
        for i in self.elective_class.normal_elective_list[0][start_index : stop_index + 1]:
            for j in i:
                print (j)
        print ('文科选修')
        for i in self.elective_class.normal_elective_list[1][start_index : stop_index + 1]:
            for j in i:
                print (j)
        print('require')
        for i in self.elective_class.require_list[start_index : stop_index + 1]:
            for j in i:
                print(j)
        print('self.rrre.SEMESTERS_LIST')
        for i in self.rrre.SEMESTERS_LIST[start_index : stop_index + 1]:
            for j in i:
                print(j)
        """
        self.encode_value()
        self.request_and_handle()

    def num_course_func(self, start_index, stop_index_plus_one):
        sum_weight = lambda course_list : sum(float(each_course[9]) for each_course in course_list)
        total_weight = sum(sum_weight(each_semester[4]) for each_semester in self.rrre.SEMESTERS_LIST[start_index : stop_index_plus_one])
        total_get = sum(float(each_semester[1]) for each_semester in self.rrre.SEMESTERS_LIST[start_index : stop_index_plus_one])
        require_count = sum(len(each_list) for each_list in self.elective_class.require_list[start_index : stop_index_plus_one])
        major_elective_count = sum(len(each_list) for each_list in self.elective_class.major_choose_list[start_index : stop_index_plus_one])
        li_ke_count = sum(len(each_list) for each_list in self.elective_class.normal_elective_list[0][start_index : stop_index_plus_one])
        wen_ke_count = sum(len(each_list) for each_list in self.elective_class.normal_elective_list[1][start_index : stop_index_plus_one])

        total_count = require_count + major_elective_count + li_ke_count + wen_ke_count
        ave_gpa = total_weight / total_get
        return require_count, major_elective_count, li_ke_count, wen_ke_count, total_count, ave_gpa
    
    def credit_course_func(self, start_index, stop_index_plus_one):
        sum_course_list = lambda course_list : sum(float(each_course[6]) for each_course in course_list)
        #type_dict = {0 : "专业选修", 1 : "普通理科选修", 2 : "普通文科选修", 3 : "必修"}
        elective_dict = {0 : self.elective_class.major_choose_list, 1 : self.elective_class.normal_elective_list[0], 2 : self.elective_class.normal_elective_list[1], 3 : self.elective_class.require_list}
        semester_type_credit_list = []
        for i in range(len(self.rrre.SEMESTERS_LIST)):
            semester_type_credit_list.append([0,0,0,0])
        for semester_index in range(start_index, stop_index_plus_one):
            for type_index in range(4):
                #print('type_index', type_index, ' semester_index', semester_index)
                semester_type_credit_list[semester_index][type_index] = sum_course_list(elective_dict[type_index][semester_index])
                #for i in semester_type_credit_list:
                    #print(i)
        require_credit = sum(each_list[3] for each_list in semester_type_credit_list)
        major_elective_credit = sum(each_list[0] for each_list in semester_type_credit_list)
        li_ke_credit = sum(each_list[1] for each_list in semester_type_credit_list)
        wen_ke_credit = sum(each_list[2] for each_list in semester_type_credit_list)
        return require_credit, major_elective_credit, li_ke_credit, wen_ke_credit, require_credit + major_elective_credit + li_ke_credit + wen_ke_credit, semester_type_credit_list         
        
    def pie_chart0(self):
        response =  urllib.request.urlopen(self.response_list[0])
        return response.read()

    def pie_chart1(self):
        response =  urllib.request.urlopen(self.response_list[1])
        return response.read()

    def radar_chart(self):
        response =  urllib.request.urlopen(self.response_list[2])
        return response.read()      

    def bar_chart(self):
        response =  urllib.request.urlopen(self.response_list[3])
        return response.read()

    def encode_value(self):
        for key, each_value in self.value.items():
            if key != 'userid' and key != 'version':
                byte_value = base64.b64encode(each_value.encode('utf8'))
                self.value[key] = byte_value.decode('utf8')