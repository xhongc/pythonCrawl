import requests

url = 'http://127.0.0.1:8080/order/'
# data = {'username': 'admin',
#         'passwd': 'admin'}
data = {'trade_type':1}
html = requests.post(url, data=data)


print(html.text)
