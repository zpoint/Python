import copy
class get_major_choose_class(object):
    def __init__(self, parent, message_list, SEMESTERS_LIST, school_data, retrieve = False, cache_flag = False):
        self.parent = parent
        self.message_list = message_list
        self.school_data = school_data
        self.retrieve = retrieve
        self.SEMESTERS_LIST = SEMESTERS_LIST
        self.require_flag = self.parent.logindlg.require_flag
        try:
            self.major_elective_en_num
        except AttributeError:
            self.major_elective_en_num = '0'			# id i.e d123456
        self.major_num_str = self.get_major_num()
        if cache_flag == True:
            self.major_choose_list, self.require_list, self.normal_elective_list = self.parent.logindlg.major_choose_list, self.parent.logindlg.require_list, self.parent.logindlg.normal_elective_list
        else:    
            self.major_choose_list, self.require_list, self.normal_elective_list = self.get_major_choose_list()

    def get_major_num(self):
        for key,value in self.school_data.name_dict.items():
            if self.message_list[7] == value:
                return key
        return 'd2220161'

    def check(self, course):
        "return 0 for li_ke, 1 for wen_ke, 2 for major_choose"
        def check_in_data_whether_major_course(parent, course_cnname):
            find = course_cnname.find('(')
            if find > 1:
                course_cnname = course_cnname[:find]
            for each_list in parent.school_data.class_num_dict[parent.major_num_str]:
                if course_cnname in each_list[2] and each_list[3] != '**':
                    return True
                elif course_cnname == '化学软件应用' or course_cnname == '涂料工艺实验':
                    return True
            return False
        return 2 if check_in_data_whether_major_course(self, course[3]) else 0
        

    def get_major_choose_list(self):
        major_elective = []
        require = []
        normal_elective = [[], []]
        for semester_list in self.SEMESTERS_LIST:
            each_semester_major_elective = []
            each_semester_require = []
            each_semester_normal_elective = []
            elective_wen_ke = []
            for each_course in semester_list[4]:
                if each_course[4] == '选修':
                    check = self.check(each_course)
                    #print("each-course:{},check:{}, type(check):{}".format(each_course, check, str(type(check))))
                    if check == 2: #major_choose
                        #print("check == 2")
                        each_semester_major_elective.append(each_course)
                    elif check == 1: #wen_ke
                        #print("check == 1")
                        elective_wen_ke.append(each_course)
                    else:  #li_ke  check == 0
                        #print("check == esle check:", check)
                        each_semester_normal_elective.append(each_course)                      
                else:
                    each_semester_require.append(each_course)
            major_elective.append(each_semester_major_elective)
            require.append(each_semester_require)
            normal_elective[0].append(each_semester_normal_elective)
            normal_elective[1].append(elective_wen_ke)
        return major_elective, require, normal_elective

"""
    def retrieve_get_major_choose_list(self, start_index, stop_index, prev_start_index, prev_stop_index):
        def update(new_major_courses, new_normal_li_ke, new_normal_wen_ke, old_major_courses, old_normal_li_ke, old_normal_wen_ke):
            print ('before update')
            print ('\nnew_major_courses\n')
            for i in new_major_courses:
                print(i)
            print('\nnew_normal_courses\n')
            for i in new_normal_courses:
                print(i)
            print('\nold_major_courses\n')
            for i in old_major_courses:
                print (i)
            print ('\nold_normal_courses\n')
            for i in old_normal_courses:
                print(i)
            for each_course in new_major_courses:
                if each_course not in old_major_courses and each_course not in old_normal_li_ke and each_course not in old_normal_wen_ke:
                    old_major_courses.append(each_course)
            for each_course in new_normal_li_ke:
                if each_course not in old_major_courses and each_course not in old_normal_li_ke and each_course not in old_normal_wen_ke:
                    old_normal_li_ke.append(each_course)
            for each_course in new_normal_wen_ke:
                if each_course not in old_major_courses and each_course not in old_normal_li_ke and each_course not in old_normal_wen_ke:
                    old_normal_wen_ke.append(each_course)
            print ('after update')
            print('\nold_major_courses\n')
            for i in old_major_courses:
                print (i)
            print ('\nold_normal_courses\n')
            for i in old_normal_courses:   
                print(i)         
            return old_major_courses, old_normal_li_ke, old_normal_wen_ke

        if stop_index < prev_start_index or prev_stop_index < start_index:
            return False
        repeat_index_list = [x for x in range(start_index, stop_index + 1) if x in range(prev_start_index, prev_stop_index + 1)]
        for each_index in repeat_index_list:
            new_offset = each_index - start_index
            old_offset = each_index - prev_start_index
            #print ('new_offset\t', new_offset, 'old_offset\t', old_offset)
            #print('self.major_choose_list[new_offset]', self.major_choose_list[new_offset])
            #print('self.normal_elective_list[0][new_offset]', self.normal_elective_list[0][new_offset])
            #print('self.normal_elective_list[1][new_offset]',self.normal_elective_list[1][new_offset])
            #print('self.old_elective.major_choose_list[old_offset]\n', self.old_elective.major_choose_list[old_offset])
            #print('self.old_elective.normal_elective_list[0][old_offset]\n',self.old_elective.normal_elective_list[0][old_offset])
            #print('self.old_elective.normal_elective_list[1][old_offset]\n',self.old_elective.normal_elective_list[1][old_offset])
            self.major_choose_list[new_offset], self.normal_elective_list[0][new_offset], self.normal_elective_list[1][new_offset] = update(self.major_choose_list[new_offset], self.normal_elective_list[0][new_offset], self.normal_elective_list[1][new_offset], self.old_elective.major_choose_list[old_offset], self.old_elective.normal_elective_list[0][old_offset], self.old_elective.normal_elective_list[1][old_offset])

    def update_init_choose_list(self):
        def search_and_pop(course, l1, l2):
            try:
                l1.remove(course)
            except ValueError:
                l2.remove(course)
        
        for index in range(self.prev_start_index, self.prev_end_index + 1):
            short_index = index - self.prev_start_index

            for each_course in self.old_elective.major_choose_list[short_index]:  #major choose
                if each_course not in self.parent.init_major_choose_list[index]:
                     self.parent.init_major_choose_list[index].append(each_course)
                     search_and_pop(each_course, self.parent.init_normal_elective_list[0][index], self.parent.init_normal_elective_list[1][index])
            
            for each_course in self.old_elective.normal_elective_list[0][short_index]: #li ke
                if each_course not in self.parent.init_normal_elective_list[0][index]:
                    print("\nI am in li ke not in init li ke\n each_course:{}".format(each_course))
                    self.parent.init_normal_elective_list[0][index].append(each_course)
                    search_and_pop(each_course, self.parent.init_major_choose_list[index], self.parent.init_normal_elective_list[1][index])

            for each_course in self.old_elective.normal_elective_list[1][short_index]: #wen ke
                if each_course not in self.parent.init_normal_elective_list[1][index]:
                    print("\nI am in wen ke not in init wen ke\n each_course:{}".format(each_course))
                    self.parent.init_normal_elective_list[1][index].append(each_course)
                    search_and_pop(each_course, self.parent.init_major_choose_list[index], self.parent.init_normal_elective_list[0][index])

        for i in self.parent.init_normal_elective_list[1]:
            print('init wen ke', i)

        for i in self.parent.init_normal_elective_list[0]:
            print('init li ke', i)
"""