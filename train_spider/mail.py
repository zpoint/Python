import smtplib
import random
import time
from email.mime.text import MIMEText
class sendmail(object):
    def __init__(self, user = "zp0int@qq.com", pwd  = "password"):
        self.user = user
        self.pwd = pwd

    def login(self, deep=0):
        try:
            self.s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            self.s.login(self.user, self.pwd)
            return True
        except smtplib.SMTPException as e:
            f = open("mail.log", "a+", encoding="utf8")
            f.write("%s login_err: %s, deep:%d\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), str(e), deep))
            f.close()
            return False

    def send(self, to, text, subject, deep=0):
        self.to = to
        self.text = text
        self.subject = subject
        self.msg = MIMEText(text)
        self.msg["Subject"] = subject
        self.msg["From"]    = self.user
        self.msg["To"]      = to

        try:
            self.s.sendmail(self.user, self.to, self.msg.as_string())
            return True
        except smtplib.SMTPException as e:
            f = open("mail.log", "a+", encoding="utf8")
            f.write("%s to: %s, subject: %s, send_err: %s, deep:%d\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), self.to, self.subject, str(e), deep))
            f.close()
            self.login(deep + 1)
            if deep < 5:
                return self.send(self.to, self.text, self.subject, deep+1)
            else:
                return False

    def quit(self):
        self.s.quit()

class verify_email(object):
    def __init__(self, string):
        array = string.split('!!!!')
        if len(array) < 2:
            self.echo_msg = "参数不正确"
        else:
            self.tomail = array[0]
            self.subject = array[1]
            self.verify_code = "%04d" % random.randint(0, 10000) # str
            self.text = "请在页面对话框中输入您的验证码:\n" + self.verify_code + '\n若不是您本人操作, 请忽略此邮件\n'
            mail = sendmail()
            if not mail.login():
                self.echo_msg = "服务器邮件客户端登录故障，请稍后再试"
            elif not mail.send(self.tomail, self.text, self.subject):
                self.echo_msg = "暂时无法发送邮件给您,请稍后再试"
            else:
                self.echo_msg = self.verify_code
