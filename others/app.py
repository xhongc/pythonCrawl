import requests
import time
session = requests.session()
a = time.time()
url = 'http://127.0.0.1:8080/login/'
params = {'page': '1', 'page_size': '1'}
data = {'password':'adminadmin'}

html = session.post(url, data=data)
print(html.text)
b = time.time()
print(b - a)
html = session.get('http://127.0.0.1:8080/event/')
print(html.text)