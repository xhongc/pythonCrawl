import requests
def login():
    data = {
        'login_name':'456',
        'login_pwd':'456'
    }
    url = 'http://192.168.3.17:8080/login'
    html = requests.post(url,data=data)
    print(html.text)
def get():
    url = 'http://192.168.3.17:8080/search'

login()
