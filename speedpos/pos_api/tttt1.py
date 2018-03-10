import requests
def get_data():
    url = 'https://phone-mop.chinaums.com/v1/uis/app/forward'

    headers = {
        'Content-Type': 'application/octet-stream',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 UmsOpenCore/1.0.0 00001000/ANDROIDPHONE/2.1.1',
        'X-Session-ID': '676274aa1ad644bab8256b972dcfb056',
        'Host': 'phone-mop.chinaums.com',
        'Content-Length': '204',
        'Connection': 'Keep-Alive'


    }
    data ={}
    html = requests.post(url,headers=headers,data=data)
    print(html.text)
def login():
    url = 'https://phone-mop.chinaums.com/v1/user/ump/login/withuserinformation'
    headers = {
        'Content-Type': 'application/download',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 UmsOpenCore/1.0.0 00001000/ANDROIDPHONE/2.1.1',
        'X-Session-ID': '676274aa1ad644bab8256b972dcfb056',
        'Host': 'phone-mop.chinaums.com',
        #'Content-Length': '204',
        'Connection': 'Keep-Alive'

    }
    data = {}
    html = requests.post(url,headers=headers,data=data)
    print(html.text)

login()