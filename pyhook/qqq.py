import requests

url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/cancelMerAuth.do'
# html = requests.get('http://39.108.5.138:8008/qmf_order')
headers = {
    'Host': 'qr.chinaums.com',
    'Connection': 'keep-alive',
    'Content-Length': '78',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://qr.chinaums.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5A Build/N2G47H; wv) AppleWebKit/537.36\
     (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 MicroMessenger/6.6.7.1320(0x26060739) \
     NetType/WIFI Language/zh_CN',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do?instMid=QMFDEFAULT&bizType=bills&appId=9&category=BILLS&wxAppId=wx3220f3baaad5ed30',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': 'SESSION=aa23815d-a216-4b00-86ca-052df67f38da; route=fa50261eb05f8f663b9307b92ceab0ae',
    'X-Requested-With': 'com.tencent.mm'

}
data = {
    'reqMid': '898352259410102',
    'instMid': 'QMFDEFAULT',
    'category': 'BILLS',
    'bizType': 'bills',
    'appId': '9'
}
html = requests.post(url=url, headers=headers, data=data)
print(html.text)
