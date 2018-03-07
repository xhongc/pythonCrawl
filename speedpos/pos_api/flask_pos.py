import requests
def search():
    url = 'http://192.168.3.17:8080/search'
    login_url = 'http://192.168.3.17:8080/login'
    params = {
        'start_time':'2018-03-01 00:00:00',
        'end_time':'2018-03-01 23:59:59',
        'time_by':'create_time',
        'trade_type':'',
        'order_status':1
    }
    data = {
            'login_name': '123',
            'login_pwd': '123'
        }


    res = requests.post(login_url,data=data)
    res = requests.get(url,params=params)
    print(res.text)
def shan():
    url = 'http://192.168.3.17:8080/shan'
    data = {
        'id':4
    }
    params = {
        'id':5
    }
    html = requests.get(url,params=params)
    print(html.text)

def cha():
    url = 'http://192.168.3.17:8080/cha'

    html = requests.get(url)
    print(html.text)
def zeng():
    url = 'http://192.168.3.17:8080/zeng'
    data = {
        'login_name':'123333',
        'login_pwd':'123',
        'user_name':'456',
        'user_pwd':'456'
    }
    html = requests.post(url,data=data)
    print(html.text)

def gai():
    url = 'http://192.168.3.17:8080/gai'
    data = {
        'id':10,
        # 'login_name': '1231111aaaa1111',
        # 'login_pwd': '123',
        'user_name': '7777777777',
        'user_pwd': '4111111asd11156'

    }
    html = requests.post(url,data=data)
    print(html.text)

gai()