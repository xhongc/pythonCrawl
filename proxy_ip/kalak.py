import requests

url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxc1e0b68d0ca63981&redirect_uri=https%3A%2F%2Fipos.lakala.com%2Fq%2Fpay%2Fwcpay&response_type=code&scope=snsapi_base&state=9F62EEA004CC4C6E9CC0336976EE66FD&connect_redirect=1#wechat_redirect'
# headers = {
#     'Host': 'ipos.lakala.com',
#     'Connection': 'keep-alive',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': "zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4"}
# session = requests.Session()
# html = session.get(url)
# print(html.status_code,html.text)
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1; CLT-AL00 Build/HUAWEICLT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044109 Mobile Safari/537.36 MicroMessenger/6.6.6.1300(0x26060638) NetType/WIFI Language/zh_CN'

}
url2 = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxc1e0b68d0ca63981&redirect_uri=https%3A%2F%2Fipos.lakala.com%2Fq%2Fpay%2Fwcpay&response_type=code&scope=snsapi_base&state=A858FC0C9D8348A0BB60EBBD48E9B321&connect_redirect=1#wechat_redirect'
html = requests.get(url2, headers=headers2)
print(html.text)
