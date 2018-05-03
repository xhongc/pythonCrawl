
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import random
import time

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
# mail_user = "1184405959@qq.com"  # 用户名
# mail_pass = "dwjybikeqdawhhbc"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
# sender = '1184405959@qq.com'
mail_user = "912305258@qq.com"  # 用户名
mail_pass = "nldevfdrtbejbcfi"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
sender = '912305258@qq.com'

def send_mail():

    msg = """
    ...<br>
    ...<br>
    ...<br>
    <p><a href="http://www.runoob.com">这是一个链接</a></p>
    
    """
    message = MIMEText(msg, 'html', 'utf-8')
    #　message['From'] = Header("408737515", 'utf-8')
    # message['To'] = Header("you", 'utf-8')
    message['From'] = formataddr(["abcdefg",mail_user])
    subject = 'hello'
    message['Subject'] = Header(subject, 'utf-8')
###################
    try:

        with open('emaila.txt', 'r')as f:
            for each in f.readlines():
                smtpObj = smtplib.SMTP_SSL(mail_host, 465)
                smtpObj.login(mail_user, mail_pass)
                each = each.replace('\n','') + '@qq.com'
                #print(each)
                receivers = []  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
                receivers.append(each)
                try:
                    smtpObj.sendmail(sender, each, message.as_string())
                    print(u"邮件发送成功：%s"%(each))

                except:
                    print(u"邮件发送失败: %s"%each)

                smtpObj.quit()
                time.sleep(random.uniform(4, 6))

    except smtplib.SMTPException as e:
        print(e)
######################
send_mail()