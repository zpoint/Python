import sys
#from cgi import parse_qs
def application(environ, start_response):
    response_headers = [('Content-type', 'text/plain; charset=utf-8')]
    path = environ['PATH_INFO'].split('/')
    if path[1] == 'szx' and environ['HTTP_HOST'] == 'localhost':
        status = '200 OK'
        output = szx_app(path[2])
    else:
        status = '403  Forbidden'
        output = ['No Permission']
    #request_body = environ['wsgi.input'].read()  
    #dict = parse_qs(request_body) 
    #output = [("%s: %s\n" % (key, value)).encode('utf8') for key, value in environ.items()]
    #output = ['good'.encode('utf8')]
    start_response(status, response_headers)
    return output

def szx_app(file_name):
    sys.path.append('/var/www/py/szx')
    from szx_get_data import get_data
    from chart import chart_class
    file_name = file_name + '.txt'
    data = get_data(file_name)
    chart_c = chart_class(data.rrre, data.elective)
    output = []
    a = str(chart_c.pie_chart0) + '\n'
    output.append(a.encode('utf8'))
    a = str(chart_c.pie_chart1) + '\n'
    output.append(a.encode('utf8'))
    a = str(chart_c.radar_chart_) + '\n'
    output.append(a.encode('utf8'))
    a = str(chart_c.bar_chart) + '\n'
    output.append(a.encode('utf8'))
    if not data.elective.retrieve:
            a = str(data.elective.normal_elective_list[0]) + '#####' #li ke
            output.append(a.encode('utf8'))
            a = str(data.elective.normal_elective_list[1]) + '#####' #wen ke
            output.append(a.encode('utf8'))
            a = str(data.elective.major_choose_list) + '#####' # major choose
            output.append(a.encode('utf8'))
            a = str(data.elective.require_list) + '#####'  #require_list
            output.append(a.encode('utf8'))
            a = str(data.elective.message_list[17]) + '#####' #second major
            output.append(a.encode('utf8'))
            a = str(data.rrre.version) + '#####'
            output.append(a.encode('utf8'))
            a = str(data.rrre.new_usr)
            output.append(a.encode('utf8'))
    else:
        a = str(data.rrre.version)
        output.append(a.encode('utf8'))
    return output