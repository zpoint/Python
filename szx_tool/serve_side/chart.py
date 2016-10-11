import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.font_manager import FontProperties
zhfont = FontProperties(fname='/usr/share/fonts/myfonts/msyh.ttc')
import os
class chart_class(object):
    def __init__(self, szx_rrre, elective_class):
        self.szx_rrre = szx_rrre
        self.elective_class = elective_class
        self.filename = str(self.elective_class.major_elective_en_num) + '_' + str(self.szx_rrre.SEMESTERS_LIST[0][3][:4]) + str(self.szx_rrre.SEMESTERS_LIST[0][3][-3]) + '_' + str(self.szx_rrre.SEMESTERS_LIST[-1][3][:4]) + str(self.szx_rrre.SEMESTERS_LIST[-1][3][-3])
        """
        if update == False:
            self.pie_chart0 = "http://42.96.159.6/szx/" + str(self.elective_class.message_list[0]) + '/' + filename + '_1.png'
            self.pie_chart1 = "http://42.96.159.6/szx/" + str(self.elective_class.message_list[0]) + '/' + filename + '_3.png'
            self.radar_chart = "http://42.96.159.6/szx/" + str(self.elective_class.message_list[0]) + '/' + filename + '_2.png'
            self.bar_chart = "http://42.96.159.6/szx/" + str(self.elective_class.message_list[0]) + '/' + filename + '_4.png'
        else:
        """
        #if not os.path.exists(dir): # path not exist
        #    os.makedirs(dir) 
        # php did mkdir
        self.pie_chart0 = self.pie_chart0()
        self.pie_chart1 = self.pie_chart1()
        self.radar_chart_ = self.radar_chart()
        self.bar_chart = self.bar_chart_func()

    def pie_chart0(self):
        labels = []
        sizes = []
        explode = []
        total = 0
        c = ['#98F5FF', '#BBFFFF', '#66CDAA', '#00C5CD', '#00E5EE', '#AEEEEE', '#9BCD9B', '#4EEE94']
        colors = []
        i = 0
        lowest_position = 0
        for key,value in self.szx_rrre.grade_dict.items():
            labels.append(key + ': ' + str(value) + '科')
            sizes.append(value)
            colors.append(c[i])
            explode.append(0)
            total += value
            try:
                if lowest_value > value and value != 0:
                    lowest_value = value
                    lowest_position = i
            except NameError:
                lowest_value = value
            i += 1
        explode[lowest_position] = 0.1

        plt.cla()
        patches, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
        plt.setp(autotexts, fontproperties=zhfont)
        plt.setp(texts, fontproperties=zhfont)
        plt.axis('equal')
        plt.title('总成绩统计', fontproperties = zhfont)
        loc = str(self.elective_class.message_list[0]) + '/' + self.filename + '_1.png'
        plt.savefig('/var/www/html/szx/' + loc, bbox_inches='tight')
        #plt.show()
        """
        f_png = open('/var/www/html/szx/1.png', 'rb')
        data = f_png.read()
        f_png.close()
        """
        data = "http://42.96.159.6/szx/" + loc
        return data

    def pie_chart1(self):
        require_num = sum(len(i) for i in self.elective_class.require_list)
        major_num = sum(len(i) for i in self.elective_class.major_choose_list)
        li_ke = sum(len(i) for i in self.elective_class.normal_elective_list[0])
        wen_ke = sum(len(i) for i in self.elective_class.normal_elective_list[1])
        labels = ['必修:' + str(require_num) + '科', '专业选修:'+ str(major_num) + '科', '普通理科选修'+ str(li_ke) + '科', '普通文科选修' + str(wen_ke) + '科']
        sizes = [require_num, major_num, li_ke, wen_ke]
        explode = [0, 0, 0, 0]
        total = 0
        colors = ['#AEEEEE', '#9BCD9B', '#4EEE94', '#66CDAA']
        min_pos = 0
        min = sizes[0]
        for i in range(len(sizes)):
            if sizes[i] < min and sizes[i] != 0:
                min = sizes[i]
                min_pos = i
        explode[min_pos] = 0.1
            
        plt.cla()
        patches, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.setp(autotexts, fontproperties=zhfont)
        plt.setp(texts, fontproperties=zhfont)
        plt.axis('equal')
        plt.title('总选课情况', fontproperties = zhfont)
        loc = str(self.elective_class.message_list[0]) + '/' + self.filename + '_3.png'
        plt.savefig('/var/www/html/szx/' + loc, bbox_inches='tight')
        #plt.show()
        #f_png = open('/var/www/html/3.png', 'rb')
        #data = f_png.read()
        #f_png.close()
        data = "http://42.96.159.6/szx/" + loc
        return data
    
    def radar_chart(self):
        c = radar_chart_class(self.szx_rrre, self.elective_class, self.filename)
        return c.png()

    def bar_chart_func(self):
        n_groups = len(self.szx_rrre.SEMESTERS_LIST)
        ave_gpa_list = []
        std_gpa_list = []
        choose_credit_list = []
        std_choose_credit_list = []
        xticks_list = []
        for i in range(len(self.szx_rrre.SEMESTERS_LIST)):
            ave_gpa_list.append(float(self.szx_rrre.SEMESTERS_LIST[i][2]))
            choose_credit_list.append(float(self.szx_rrre.SEMESTERS_LIST[i][0]) / 5)

            std_gpa_list.append(0.000001)
            std_choose_credit_list.append(0.000001)
            xticks_list.append(self.szx_rrre.SEMESTERS_LIST[i][4][0][1])
        
        
        plt.cla()
        fig, ax = plt.subplots()

        index = np.arange(n_groups)
        bar_width = 0.35

        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        rects1 = plt.bar(index, choose_credit_list, bar_width,
                        alpha=opacity,
                        color='b',
                        yerr=std_choose_credit_list,
                        error_kw=error_config,
                        label='选修学分')
        i = 0
        for rect in rects1:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % self.szx_rrre.SEMESTERS_LIST[i][0], fontproperties = zhfont)
            i += 1

        rects2 = plt.bar(index + bar_width, ave_gpa_list, bar_width,
                        alpha=opacity,
                        color='r',
                        yerr=std_gpa_list,
                        error_kw=error_config,
                        label='各学期绩点')
        i = 0
        for rect in rects2:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % self.szx_rrre.SEMESTERS_LIST[i][2], fontproperties = zhfont)
            i += 1

        plt.ylabel('参照坐标轴', fontproperties = zhfont)
        plt.title('成绩学分对比', fontproperties = zhfont)
        plt.xticks(index + bar_width, xticks_list, fontproperties = zhfont)
        plt.legend(prop = zhfont)

        plt.tight_layout()
        loc = str(self.elective_class.message_list[0]) + '/' + self.filename + '_4.png'
        plt.savefig('/var/www/html/szx/' + loc, bbox_inches='tight')
        plt.close('all')
        #file = open('/var/www/html/4.png', 'rb')
        #data = file.read()
        #file.close()
        data = "http://42.96.159.6/szx/" + loc
        return data

class radar_chart_class(object):
    def radar_factory(self, num_vars, frame='circle'):
        # calculate evenly-spaced axis angles
        theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
        # rotate theta such that the first axis is at the top
        theta += np.pi/2

        def draw_poly_patch(self):
            verts = self.unit_poly_verts(theta)
            return plt.Polygon(verts, closed=True, edgecolor='k')

        def draw_circle_patch(self):
            # unit circle centered on (0.5, 0.5)
            return plt.Circle((0.5, 0.5), 0.5)

        patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
        if frame not in patch_dict:
            raise ValueError('unknown value for `frame`: %s' % frame)

        class RadarAxes(PolarAxes):

            name = 'radar'
            # use 1 line segment to connect specified points
            RESOLUTION = 1
            # define draw_frame method
            draw_patch = patch_dict[frame]

            def fill(self, *args, **kwargs):
                """Override fill so that line is closed by default"""
                closed = kwargs.pop('closed', True)
                return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
                """Override plot so that line is closed by default"""
                lines = super(RadarAxes, self).plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
                # FIXME: markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.concatenate((x, [x[0]]))
                    y = np.concatenate((y, [y[0]]))
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(np.degrees(theta), labels)

            def _gen_axes_patch(self):
                return self.draw_patch()

            def unit_poly_verts(self, theta):
                x0, y0, r = [0.5] * 3
                verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
                return verts

            def _gen_axes_spines(self):
                if frame == 'circle':
                    return PolarAxes._gen_axes_spines(self)
                # The following is a hack to get the spines (i.e. the axes frame)
                # to draw correctly for a polygon frame.

                # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
                spine_type = 'circle'
                verts = self.unit_poly_verts(theta)
                # close off polygon by repeating first vertex
                verts.append(verts[0])
                path = Path(verts)

                spine = Spine(self, spine_type, path)
                spine.set_transform(self.transAxes)
                return {'polar': spine}

        register_projection(RadarAxes)
        return theta


    def unit_poly_verts(self, theta):
        """Return vertices of polygon for subplot axes.

        This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
        """
        x0, y0, r = [0.5] * 3
        verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
        return verts


    def example_data(self):
        data = [
            self.rrre_class.data_grade_list,
            ('各学期成绩情况', [each_list for each_list in self.rrre_class.each_semester_grade_list])
        ]
        """
        with open('/var/www/1.txt', 'w') as f:
            f.write('self.rrre_class.data_grade_list\n' + str(self.rrre_class.data_grade_list))
            f.write('[each_list for each_list in self.rrre_class.each_semester_grade_list]:\n')
            f.write(str(self.rrre_class.each_semester_grade_list))
        """
        return data


    def __init__(self, rrre_class, elective_class, filename):
        self.filename = filename
        plt.cla()
        self.rrre_class = rrre_class
        self.elective_class = elective_class
        N = len(rrre_class.grade_dict)
        theta = self.radar_factory(N, frame='polygon')

        data = self.example_data()
        spoke_labels = data.pop(0)

        fig = plt.figure(figsize=(9, 9))
        #fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

        colors = ['#90EE90', '#4F4F4F', '#00FF00', '#00FFFF', '#FF7256', '#FFA500', '#8B7E66', 	'#FF8247']
        # Plot the four cases from the example data on separate axes
        for n, (title, case_data) in enumerate(data):
            ax = fig.add_subplot(1, 1, n + 1, projection='radar')
            if rrre_class.biggest <= 4:
                plt.rgrids([1, 2, 3, 4])
            elif rrre_class.biggest <= 8:
                plt.rgrids([2, 4, 6, 8])
            elif rrre_class.biggest <= 12:
                plt.rgrids([3, 6, 9, 12])
            else:
                plt.rgrids([4, 8, 13, 17])
            ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                        horizontalalignment='center', verticalalignment='center', fontproperties = zhfont)
            for d, color in zip(case_data, colors):
                ax.plot(theta, d, color=color)
                ax.fill(theta, d, facecolor=color, alpha=0.25)
            ax.set_varlabels(spoke_labels)

        # add legend relative to top-left plot

        #plt.subplot(2, 2, 1)

        labels = [semester_list[3] for semester_list in self.rrre_class.SEMESTERS_LIST]
        legend = plt.legend(labels, loc=(0.52, .88), labelspacing=0.1, prop = zhfont)
        #plt.setp(legend.get_texts(), fontsize='small')

        #plt.figtext(0.5, 0.965, '5-Factor Solution Profiles Across Four Scenarios',ha='center', color='black', weight='bold', size='large')
        self.loc = str(self.elective_class.message_list[0]) + '/' + self.filename + '_2.png'
        plt.savefig('/var/www/html/szx/' + self.loc, bbox_inches='tight')

    def png(self):
        #f_png = open('/var/www/html/2.png', 'rb')
        #data = f_png.read()
        #f_png.close()
        #return data
        return "http://42.96.159.6/szx/" + self.loc