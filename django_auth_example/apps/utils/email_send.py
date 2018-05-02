from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from django_auth_example.settings import EMAIL_FROM

def random_str(random_length=8):
    str =''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8080/active/{0}'.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    if send_type == 'forget':
        email_title = '找回密码链接'
        email_body = '请点击下面的链接找回你的密码：http://127.0.0.1:8080/reset/{0}'.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
if __name__ == '__main__':
    send_register_email('2324369231@qq.com')