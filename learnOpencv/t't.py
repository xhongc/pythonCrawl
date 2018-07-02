import requests

url = 'https://ipos.lakala.com/q/pay/E09D487C42B940C5820C0F9C90B22BC4/ogUppwO7bUC2YzTlcn1dox0tSgK8/000000000100'
headers = {
    'Host': 'ipos.lakala.com',
    'Connection': 'keep-alive',
    'Content-Length': '13',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://ipos.lakala.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1; CLT-AL00 Build/HUAWEICLT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060638) NetType/WIFI Language/zh_CN',
    'Content-Type': 'application/json; charset=UTF-8',
    'Referer': 'https://ipos.lakala.com/q/pay/wcpay?code=0213rSwx0qbyji1f4Ayx07P6xx03rSwc&state=5DAD063EDC8A4A46A435815D7D6034FC',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh-CN;q=0.8,en-US;q=0.6',

}
data = {
    'remark': ''
}
html = requests.post(url, headers=headers)
print(html.text)
