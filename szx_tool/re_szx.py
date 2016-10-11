import re
from collections import OrderedDict
#course_list
#0--->num  1--->semester_num  2--->course_num
#3--->course_name  4--->course_type  5--->score
#6--->get_score  7--->grade  8--->GPA  9--->GPA_weight
class rrre(object):
    def __init__(self, content, html_flag = True):
        self.version = 2.0
        if html_flag:
            self.decode_html(content)
        else:
            self.SEMESTERS_LIST = content

    def decode_html(self, html_decoded):            
        SEMESTERS_LIST = []
        pattern = re.compile('.+?0FF">(.+?)<(.+?)center(.+?)<table border="1"(.+?)</table.+?color(.+)', re.DOTALL)
        match = re.match(pattern, html_decoded)
        while match != None:
            repeat = True if "培养方案认定类别" in match.group(2) else False
            table_data = match.group(3)
            other_table_data = match.group(4)
            semester_list = self.match_other_table(other_table_data)
            courses = self.match_table(table_data, repeat)
            semester_list.append(match.group(1))
            semester_list.append(courses)
            SEMESTERS_LIST.append(semester_list)
            try:
                match1 = re.match(pattern, match.group(5))
            except  IndexError:
                break
            
            if match1 == None:
                new_pattern = re.compile('.+?0FF">(.+?)<(.+?)center(.+?)<table border="1"(.+?)</table.+?</html>', re.DOTALL)
                match = re.match(new_pattern, match.group(5))
            else:
                match = match1

        self.SEMESTERS_LIST = SEMESTERS_LIST

    def decode_html1(self, html_decoded):            
        SEMESTERS_LIST = []
        pattern = re.compile('.+?0FF">(.+?)<(.+?)center(.+?)<table border="1"(.+?)</table.+?color(.+)', re.DOTALL)
        match = re.match(pattern, html_decoded)
        while match != None:
            #repeat = True if "培养方案认定类别" in match.group(2) else False
            repeat = False
            table_data = match.group(3)
            other_table_data = match.group(4)
            semester_list = self.match_other_table(other_table_data)
            courses = self.match_table(table_data, repeat)
            semester_list.append(match.group(1))
            semester_list.append(courses)
            SEMESTERS_LIST.append(semester_list)
            try:
                match1 = re.match(pattern, match.group(5))
            except  IndexError:
                break
            
            if match1 == None:
                new_pattern = re.compile('.+?0FF">(.+?)<.+?center(.+?)<table border="1"(.+?)</table.+?</html>', re.DOTALL)
                match = re.match(new_pattern, match.group(5))
            else:
                match = match1

        self.SEMESTERS_LIST = SEMESTERS_LIST
        #####get grade_dict in the service side
        #semester_list
        #0--->choose_credit  1--->pass_credit  2--->average_GPA  3--->semester_num  4--->courses
        #SEMESTERS_LIST ====>   [semester_list, semester_list, semester_list..........]

    def match_course(self, data, repeat):
        number_index = 6 if repeat else 5
        course_list = []
        pattern = re.compile('.+?td width.+?>(.+?)<(.+)', re.DOTALL)
        match = re.match(pattern, data)
        while match != None:
            course_list.append(match.group(1).strip())
            match = re.match(pattern, match.group(2))
        course_list.pop()
        course_list[number_index] = str(round(float(course_list[number_index]), 1))
        course_list[number_index + 1] = str(round(float(course_list[number_index + 1]), 1))
        course_list[-1] = course_list[-1][:-1]
        if repeat:
            del course_list[number_index - 2]
        return course_list

    def match_table(self, data, repeat=False):
        courses = []
        pattern = re.compile('.+?<tr>(.+?)</tr>(.+)', re.DOTALL)
        match = re.match(pattern, data)
        while match != None:
            course_data = match.group(1)
            courses.append(self.match_course(course_data, repeat))
            match = re.match(pattern, match.group(2))
        return courses

    def match_other_table(self, data):
        semester_list = []
        pattern = re.compile('.+?<small>.+?([0-9]{1,2}\.*[0-9]{0,2})<(.+)', re.DOTALL)
        match = re.match(pattern, data)
        while match != None:
            semester_list.append(match.group(1))
            match = re.match(pattern, match.group(2))
        return semester_list