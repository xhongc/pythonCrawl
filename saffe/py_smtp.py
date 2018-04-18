
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "408737515@qq.com"  # 用户名
mail_pass = "uppsptidntgmbgeg"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

sender = '408737515@qq.com'
receivers = ['1840597778@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('you are big pig', 'plain', 'utf-8')
#　message['From'] = Header("408737515", 'utf-8')
# message['To'] = Header("you", 'utf-8')

subject = 'hello'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    for _ in range(2):
        smtpObj.sendmail(sender, receivers, message.as_string())
        print(u"邮件发送成功")
        time.sleep(5)
    smtpObj.quit()

except smtplib.SMTPException as e:
    print(e)

