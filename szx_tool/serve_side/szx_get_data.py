import MySQLdb
import base64
from collections import OrderedDict
class temp(object):
    def __init__(self):
        pass
    def execute(self, str):
        exec(str)
    def compelete(self):
        self.data_grade_list = [key for key, value in self.grade_dict.items()]
        self.new_usr = False
        self.version = True if self.version == 2.0 else "http://www.42.96.159.6$$$吃的好$$$睡得香$$$身体棒棒"

class get_data(object):
    def __init__(self, filename):
        self.rrre = temp()
        self.elective = temp()
        file = open('/var/www/html/szx/' + filename.split('.')[0] + '/' + filename, 'r', encoding='utf8')
        i = 0
        for line in file.readlines():
            byte_line = base64.b64decode(line.encode('utf8'))
            line = byte_line.decode('utf8')
            if i <= 1:
                self.rrre.execute(line)
            else:
                self.elective.execute(line)
            i += 1
        file.close()
        self.get_grade_dict(0, len(self.rrre.SEMESTERS_LIST))
        self.rrre.compelete()
        self.write_to_sql()

    def get_rrre(self):
        return self.rrre

    def get_elective(self):
        return self.elective

    def get_grade_dict(self, start_index, stop_index_plus_one):
        def generate_list(origin_dict):
            l = []
            for key in self.rrre.grade_dict.keys():
                try:
                    l.append(origin_dict[key])
                except KeyError:
                    l.append(0)
            return l
        self.rrre.grade_dict = OrderedDict()
        self.rrre.each_semester_grade_dict_list = []
        for semester_index in range(start_index, stop_index_plus_one):
            self.rrre.each_semester_grade_dict_list.append({})
            for each_course in self.rrre.SEMESTERS_LIST[semester_index][4]:
                try:
                    self.rrre.grade_dict[each_course[7]] += 1
                except KeyError:
                    self.rrre.grade_dict[each_course[7]] = 1
                try:
                    self.rrre.each_semester_grade_dict_list[semester_index - start_index][each_course[7]] += 1
                except KeyError:
                    self.rrre.each_semester_grade_dict_list[semester_index - start_index][each_course[7]] = 1

        for i in ('A', 'B', 'C', 'D', 'F'):
            try:
                self.rrre.grade_dict[i]
            except KeyError:
                self.rrre.grade_dict[i] = 0 
        self.rrre.biggest = max(max(each_dict.values()) for each_dict in self.rrre.each_semester_grade_dict_list)
        self.rrre.each_semester_grade_list = [generate_list(each_dict) for each_dict in self.rrre.each_semester_grade_dict_list]
    def write_to_sql(self):
        #f = open('/var/www/py/szx/debug.txt', 'a+')
        try:
            self.table_name = 's' + self.elective.message_list[0]
            db = MySQLdb.connect(host = 'localhost', user = 'zpoint', passwd = 'a19950614', db = 'szx', charset="utf8")
            self.cur = db.cursor()
            #q = "SELECT name, id FROM test where id = 22"
            q = "SELECT begin_semester, end_semester, second_major  FROM mainmessage WHERE userid = '%s'" % (self.elective.message_list[0])
            self.cur.execute(q.encode('utf8'))
            fetch = self.cur.fetchone()
            if fetch == None:
                #new user
                self.rrre.new_usr = True
                self.insert_messege_create_table()
                self.insert_all_to_db()
            
            elif self.elective.retrieve == True:
                ###press the button retrieve###
                #update elective class and second_major to database
                self.update_second_major(fetch[2]) #second_major = fetch[2]
                self.update_elective_class()
                ##after update, get latest elective_list and major_choose to return
                self.get_latest_elective_class()
                self.update_time()
            else:
                ## second time login
                self.check_add_semester(fetch)  #check whether more semester's course to add
                self.get_second_major()
                self.get_latest_elective_class()
                self.update_time()
            db.commit()
        except MySQLdb.Error as e: #
        #except IOError as e:
                log = 'Mysql Error %d: %s' % (e.args[0], e.args[1])
                f = open('/var/www/html/szx/mysql_errlog.txt', 'a+') 
                f.write(str(self.elective.message_list) + '\n')
                f.write(log)
                f.close()

    def insert_all_to_db(self, begin_semester=None):
        if begin_semester == None:
            for each_list in self.elective.require_list:
                self.insert_courselist_to_db(each_list, "必修")
            for each_list in self.elective.major_choose_list:
                self.insert_courselist_to_db(each_list, "专业选修")
            for each_list in self.elective.normal_elective_list[0]:
                self.insert_courselist_to_db(each_list, "理科选修")
            for each_list in self.elective.normal_elective_list[1]:
                self.insert_courselist_to_db(each_list, "文科选修")
        else:
            for each_list in self.elective.require_list:
                if len(each_list) > 0 and self.get_semester(each_list) > begin_semester:
                    self.insert_courselist_to_db(each_list, "必修")
            for each_list in self.elective.major_choose_list:
                if len(each_list) > 0 and self.get_semester(each_list) > begin_semester:
                    self.insert_courselist_to_db(each_list, "专业选修")
            for each_list in self.elective.normal_elective_list[0]:
                if len(each_list) > 0 and self.get_semester(each_list) > begin_semester:
                    self.insert_courselist_to_db(each_list, "理科选修")
            for each_list in self.elective.normal_elective_list[1]:
                if len(each_list) > 0 and self.get_semester(each_list) > begin_semester:
                    self.insert_courselist_to_db(each_list, "文科选修")

    def insert_courselist_to_db(self, course_list, course_type):
        #list must have same course type
        for each_course in course_list:
            course_num = each_course[2] if each_course[7] !=  'F' else 'F' + str(each_course[2])
            query = """INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (self.table_name, each_course[0], each_course[1] + '#' + course_num, each_course[1], each_course[3], course_type, each_course[5], each_course[6], each_course[7], each_course[8], each_course[9])
            self.cur.execute(query.encode('utf8'))

    def update_courslist_to_db(self, course_list, course_type):
        for course in course_list:
            course_num = str(course[2]) if course[7] != 'F' else 'F' + str(course[2])
            query = "SELECT course_type from %s WHERE course_num = '%s'" % (self.table_name, str(course[1]) + '#' + course_num)
            self.cur.execute(query.encode('utf8'))
            result = self.cur.fetchone()
            if result[0] != course_type:
                query = "UPDATE %s SET course_type = '%s' where course_num = '%s'" % (self.table_name, course_type, str(course[1]) + '#' + course_num)
                self.cur.execute(query.encode('utf8'))

    def insert_messege_create_table(self):
        query = """INSERT INTO mainmessage VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s)""" % (self.elective.message_list[0], self.elective.message_list[1], self.elective.message_list[2], self.elective.message_list[3], self.elective.message_list[4], self.elective.message_list[5], self.elective.message_list[6], self.elective.message_list[7], self.elective.message_list[8], self.elective.message_list[9], self.elective.message_list[10], self.elective.message_list[11], self.elective.message_list[12], self.elective.message_list[13], self.elective.message_list[14], self.elective.message_list[15], self.elective.message_list[16], self.elective.message_list[17], self.rrre.SEMESTERS_LIST[0][4][0][1], self.rrre.SEMESTERS_LIST[-1][4][0][1], 'NOW()', self.rrre.version, 1)
        """
        f = open('/var/www/html/szx/mysql_errlog.txt', 'a+')
        f.write(str(self.elective.message_list) + '\n')
        f.write(query)
        f.close()
        """
        self.cur.execute(query.encode('utf8'))
        query = """CREATE TABLE IF NOT EXISTS %s (
                        course_order_num INT UNSIGNED NOT NULL,
                        course_num VARCHAR(30) NOT NULL PRIMARY KEY,
                        semester_num INT UNSIGNED NOT NULL,
                        course_name VARCHAR(100) NOT NULL,
                        course_type VARCHAR(20) NOT NULL,
                        score FLOAT(5) UNSIGNED NOT NULL,
                        get_score FLOAT(5) UNSIGNED NOT NULL,
                        grade VARCHAR(5) NOT NULL,
                        GPA FLOAT(5) UNSIGNED NOT NULL,
                        GPA_weight FLOAT(5) UNSIGNED NOT NULL
                        )""" % (self.table_name)
        self.cur.execute(query.encode('utf8'))

    def check_add_semester(self, fetch):
        begin_semester = int(fetch[0])
        end_semester = int(fetch[1])
        if end_semester < self.get_last_semester():
            self.insert_all_to_db(begin_semester=begin_semester)

    def update_second_major(self, second_major):
        if second_major != self.elective.message_list[17]:
            query = "UPDATE mainmessage SET second_major = '%s' WHERE userid = '%s'" % (self.elective.message_list[17], self.elective.message_list[0]) 
            self.cur.execute(query.encode('utf8'))

    def update_time(self):
        query = "UPDATE mainmessage SET time = NOW() WHERE userid = '%s'" % (self.elective.message_list[0])
        self.cur.execute(query.encode('utf8'))

    def get_second_major(self):
        query = "SELECT second_major from mainmessage WHERE userid = '%s'" % (self.elective.message_list[0])
        self.cur.execute(query.encode('utf8'))
        second_major = self.cur.fetchone()[0]
        if second_major != self.elective.message_list[17]:
            self.elective.message_list[17] = second_major

    def update_elective_class(self):
        if self.elective.require_flag:
            for course_list in self.elective.require_list:
                self.update_courslist_to_db(course_list, "必修")
        for course_list in self.elective.major_choose_list:
            self.update_courslist_to_db(course_list, "专业选修")
                #f.write('\n\nelective.normal_elective_list\n\n')
                #f.write(str(self.elective.normal_elective_list))
        for course_list in self.elective.normal_elective_list[0]:
            self.update_courslist_to_db(course_list, "理科选修")
        for course_list in self.elective.normal_elective_list[1]:
            self.update_courslist_to_db(course_list, "文科选修")

    def get_course_list_back(self, course_type):
        semester_list_dict = OrderedDict()
        semester_list = []
        for i in range(len(self.rrre.SEMESTERS_LIST)):
            semester_list_dict[str(self.rrre.SEMESTERS_LIST[i][3][:4]) + str(self.rrre.SEMESTERS_LIST[i][3][-3])] = []
            semester_list.append(str(self.rrre.SEMESTERS_LIST[i][3][:4]) + str(self.rrre.SEMESTERS_LIST[i][3][-3]))

        query = "SELECT * from %s WHERE course_type = '%s'" % (self.table_name, course_type)
        self.cur.execute(query.encode('utf8'))
        result_normal_elective = self.cur.fetchall()
        #f.write('\n'+ query +'\n')
        for each_course in result_normal_elective:
            #f.write('\n'+ str(each_course) +'\n')
            if str(each_course[2]) in semester_list:
                try:
                    if each_course[7] == 'F':
                        course_num = each_course[1].split('#')[1][1:]
                    else:
                        course_num = each_course[1].split('#')[1]
                    l = [str(each_course[0]), str(each_course[2]), course_num, str(each_course[3]), course_type[-2:], str(each_course[5]), str(each_course[6]), str(each_course[7]), str(each_course[8]), str(each_course[9])]
                    #f.write('l:\t' + str(l))
                    semester_list_dict[str(each_course[2])].append(l)
                except KeyError:
                    continue
        return [value for value in semester_list_dict.values()]

    def get_latest_elective_class(self):
        self.elective.normal_elective_list[0] = self.get_course_list_back('理科选修')
        self.elective.normal_elective_list[1] = self.get_course_list_back('文科选修')
        self.elective.major_choose_list = self.get_course_list_back('专业选修')
        self.elective.require_list = self.get_course_list_back('必修')


    def check_course_type(self, course):
        for each_course_list in self.elective.major_choose_list:
            for each_course in each_course_list:
                if str(course[2]) == str(each_course[2]) and str(course[1]) == str(each_course[1]):
                    return True 
        return False

    def get_semester(self, each_list):
        return int(each_list[0][1])

    def get_last_semester(self):
        return int(self.rrre.SEMESTERS_LIST[-1][3][:4] + self.rrre.SEMESTERS_LIST[-1][3][-3])