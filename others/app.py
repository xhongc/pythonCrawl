import requests
import json

session = requests.session()
url = 'http://127.0.0.1:8080/login/'
data = {
    'username': 'chong',
    'password': 'adminadmin'
}
html = session.post(url=url, data=data)
html = json.loads(html.text)
token = html['token']
adr_url = 'http://127.0.0.1:8080/address/'
headers = {
    'Authorization': 'jwt ' + token
}
data = {"province": "11111", "city": "2", "district": "3", "address": "", "signer_name": "",
        "add_time": "2018-08-31 15:19", "signer_mobile": ""}

html = session.post(url=adr_url, headers=headers,data=data)
print(html.text)
