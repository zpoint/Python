import re
import urllib.request
import urllib.parse
import os.path
from time import sleep

machine_dict = {
    '15': 'X射线小角散射仪',
    '29': '核磁共振波谱仪',
    '16': 'X-射线衍射仪',
    '17': '扫描电子显微镜',
    '18': '动态力学分析仪',
    '19': '流变仪',
    '20': '同步热分析仪（TG-DSC/DTA）',
    '21': '热机械分析仪',
    '32': '傅立叶变换红外光谱仪（PE）',
    '40': '高效液相色谱仪',
    '22': 'BET比表面仪',
    '23': '电感耦合等离子体发射光谱仪',
    '24': '电化学工作站',
    '25': '偏光显微镜',
    '26': '差示扫描量热仪（常温至500℃）',
    '27': '热膨胀仪',
    '33': '红外光谱仪（岛津）',
    '34': '紫外可见分光光度计（UV-2501PC）',
    '35': '荧光分光光度计',
    '36': '紫外可见分光光度计（UV-2550）',
    '37': '激光光散射粒度分析仪',
    '38': '凝胶渗透色谱仪(1100 SERIES)',
    '39': '凝胶渗透色谱仪（AGILENT 1200型）',
    '41': '超微量天平',
    '42': 'GPC静态激光散射仪',
    '43': '气质联用仪',
    '44': '电子拉力机',
    '45': '超临界干燥（萃取）装置',
    '46': '全自动凯氏定氮仪',
    '47': '热分析仪（仅用于-140~200℃测试）',
    '50': '元素分析仪（Vario EL cube）',
    '51': '荧光光谱仪（F7000）',
    '53': '综合电化学测试系统【仅可以使用1号通道】',
    '52': '气相色谱仪',
    '54': '综合电化学测试系统【仅可以使用3号通道】',
    '58': '综合电化学测试系统【仅可以使用2号通道】',
    '55': '综合电化学测试系统【仅可以使用5号通道】',
    '56': '综合电化学测试系统【仅可以使用7号通道】',
    '59': '综合电化学测试系统【仅可以使用4号通道】',
    '60': '综合电化学测试系统【仅可以使用6号通道】',
    '61': '综合电化学测试系统【仅可以使用8号通道】',
    '62': '红外光谱（岛津IRAffinity-1）',
    '71': '热分析仪【美国TA公司】 （TGA-Q50） ',
    '0': '纳米激光粒度分析仪',
    '63': '薄层色谱扫描仪(CD60)',
    '64': '全自动氨基酸分析仪',
    '65': '广角静态动态同步激光散射仪',
    '66': '原子力显微镜',
    '67': '全自动多站比表面微孔介孔孔隙分析和蒸汽吸附仪',
    '68': '高分子挤出流变仪（哈克转矩流变仪）',
    '69': '场发射扫描电子显微镜',
    '70': '单晶X射线衍射仪',
    '72': '振动样品磁强计',
    '73': '透射电子显微镜-能谱仪',
}
headers = {
    "Host": "192.168.30.2",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "deflate",
    "Connection": "close",
    "Content-Type": "application/x-www-form-urlencoded"
}
config_dir = "machine_config.txt"


def login(username, password):
    param = {
        "username": username.encode("gbk"),
        "password": password.encode("gbk")
    }
    url = "http://192.168.30.2/login_check.asp"
    print("正在登录, 请稍后....")
    req = urllib.request.Request(url, headers=headers)
    data = urllib.parse.urlencode(param).encode("gbk")
    response = urllib.request.urlopen(req, data=data)
    text = response.read().decode("gbk")
    if "back" in text:
        right_msg = text[text.index("'") + 1:]
        err_msg = right_msg[:right_msg.index("'")]
        print("登录失败, 请修改配置文件后重新运行程序, 错误信息: %s" % (err_msg, ))
        return False
    print("登陆成功...")
    return response


def submit(login_response, parameters):
    print("正在提交...")
    url = "http://192.168.30.2/booking_submit.asp?action=mach&userid=1399"
    # init parameters
    parameters.pop("username")
    parameters.pop("password")
    cookies = login_response.headers["Set-Cookie"].split(";")[0]
    left, right = cookies.split("=")
    parameters[left] = right
    for key, value in parameters.items():
        parameters[key] = value.encode("gbk")
    headers["Cookie"] = cookies

    req = urllib.request.Request(url, headers=headers)
    data = urllib.parse.urlencode(parameters).encode("gbk")
    response = urllib.request.urlopen(req, data=data)
    text = response.read().decode("gbk")
    if "成功" in text:
        succ_msg = text[text.index("'")+1:]
        succ_msg = succ_msg[:succ_msg.index("'")]
        if not succ_msg:
            succ_msg = "提交成功"
        return True, succ_msg
    elif "错误" in text:
        err_msg = "提交后返回错误, 参数有误, 请修改后重新提交..."
    elif "已经有人预约" in text:
        err_msg = text[text.index("'")+1:]
        err_msg = err_msg[:err_msg.index("'")]
    elif "不能超过两个星期" in text:
        err_msg = text[text.index("'")+1:]
        err_msg = err_msg[:err_msg.index("'")]
    else:
        err_msg = text
    return False, err_msg


def get_config(first_time=True):
    def make_content(describe, middle, annotation):
        content = b"%-20s\t%-5s\t%-100s\r\n" % (describe.encode("gbk"), middle.encode("gbk"), annotation.encode("gbk"))
        return content.decode("gbk")

    def init_file():
        with open(config_dir, "w", encoding="gbk") as f:
            # gbk can align chinese characters
            content = "#请将回答填在下列括号内, 确保准确无误, 填写非中文字符时确保输入法切成英文\r\n"
            content += "#为了方便使用windows的童鞋, 读写本文件的时候请保持gbk编码\r\n"
            content += "#更新日期: 2016-12-31\r\n"
            content += "#源码: https://github.com/zpoint/Python/tree/master/submit_script\r\n"
            content += make_content("用户名：", "()", "#用于登录")
            content += make_content("密码：", "()", "#用于登录")
            content += make_content("能否独立使用仪器：", "()", "#能填数字0, 不能填数字1")
            content += make_content("要预约的仪器序号:", "()", "#将本文档往下拉查看序号, 如预约荧光光谱仪（F7000）则填入51")
            content += make_content("使用方向:", "()", "#填中文 (参考预约页面)")
            content += make_content("开始日期:", "()", "#格式: 2017-01-07 9:00:00")
            content += make_content("截止日期:", "()", "#格式: 2017-01-07 12:00:00")
            content += make_content("样品数量:", "()", "#整数")
            content += make_content("样品前处理:", "()", "#不需要数字:0, 需要:数字1")
            content += make_content("测试目的:", "()", "#可填中文")
            content += make_content("样品组成及描述:", "()", "#可填中文")
            content += make_content("测试参数:", "()", "#可填中文")
            content += make_content("特殊要求:", "()", "#可填中文")
            content += make_content("测完样品如何处理:", "()", "#样品自行取回数字:0, 直接废弃处理数字:1")
            content += make_content("备注说明:", "()", "#可填中文")
            content += "\r\n" * 5
            content += (b"#%-60s\t %-3s\r\n" % ("仪器型号".encode("gbk"), "仪器序号".encode("gbk"))).decode("gbk")
            for key, value in machine_dict.items():
                gbk_content = b"#%-60s\t %-3s\r\n" % (value.encode("gbk"), key.encode("gbk"))
                content += gbk_content.decode("gbk")
            f.write(content)
        input("已初始化配置文件, 请在当前目录打开 %s 修改并保存按确认键继续....\r\n\r\n" % (config_dir, ))

    paramaters = {}
    file_order = ("username", "password", "independence", "machid", "direction", "startdate", "starttime",
                  "enddate", "endtime", "sample", "handle", "aim", "describle", "argument", "special", "handles",
                  "remark")
    rgx = re.compile("\s+\((.+?)\)\s+")
    debug_line = ""
    if not os.path.exists(config_dir):
        init_file()
    try:
        with open(config_dir, "r", encoding="gbk") as f:
            i = 0
            for line in f.readlines():
                debug_line = line
                if line and line[0] != "#" and line[0] != "\n":
                    text = re.search(rgx, line).group(1).strip()
                    if "date" in file_order[i]:
                        date, time = text.split(" ")
                        paramaters[file_order[i]] = date
                        paramaters[file_order[i + 1]] = time
                        i += 2
                    else:
                        paramaters[file_order[i]] = text
                        i += 1
        if len(paramaters) != len(file_order):
                raise ValueError
        return paramaters
    except (ValueError, AttributeError) as e:
        if first_time:
            print("当前目录下的 %s 填写格式错误\n%s正在恢复默认文件格式..." % (config_dir, "请更正该行: " + debug_line if debug_line else ""))
        else:
            print("数据格式不符")
        init_file()
        return get_config()


if __name__ == "__main__":
    interval = 0.1
    parameters = get_config()  # fill in paramaters
    login_response = login(parameters["username"], parameters["password"])
    while not login_response:
        input("请打开当前目录的 %s 文件进行修改, 保存后按确认键继续....\r\n\r\n" % (config_dir,))
        parameters = get_config()
        login_response = login(parameters["username"], parameters["password"])

    success, msg = submit(login_response, parameters)
    while not success:
        print("发生错误:", msg)
        if "不能超过两个星期" in msg:
            print("%.2f 秒后重试" % (interval, ))
            sleep(interval)
            success, msg = submit(login_response, parameters)
        else:
            input("请打开当前目录的 %s 文件进行修改, 保存后按确认键继续....\r\n\r\n" % (config_dir,))
            parameters = get_config(False)
            success, msg = submit(login_response, parameters)

    input("成功提交: " + msg + "\n按任意键继续")
