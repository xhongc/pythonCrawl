import requests
from scrapy.selector import Selector
import pymysql
import json
import time
from pprint import pprint

def get_data():
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBills.do'
    headers = {
        'Host': 'qr.chinaums.com',
        'Connection': 'keep-alive',
        'Content-Length': '89',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://qr.chinaums.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': 'SESSION=1b3ac271-d9eb-42bc-8b77-fb6e87a04ed0; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088'

    }

    data = {
        'reqMid':'898393058120502',
        'pageSize':'15',
        'curPage':'1',
        'billDate':'2018年03月08日'
    }

    html = requests.post(url,headers=headers,data=data)
    pprint(html.text)
    # pprint(json.loads(html.text))
def login():
    global session
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do'
    headers = {
        'Host': 'qr.chinaums.com',
        'Connection': 'keep-alive',
        'Content-Length': '114',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://qr.chinaums.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
        'Referer': 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do?instMid=QMFDEFAULT&bizType=bills&appId=9&category=BILLS&wxAppId=wx3220f3baaad5ed30',
        'Cookie': 'SESSION=1b3ac271-d9eb-42bc-8b77-fb6e87a04ed0; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088'
    }

    data={
        'bizType':'bills',
        'appId':'9',
        'instMid':'QMFDEFAULT',
        'category':'BILLS',
        'userId':'XMCLCY',
        'userPwd':'Xm123456',
        'nickName':'高磊'
    }
    session = requests.session()
    html = session.post(url,headers=headers,data=data)
    print(html.text)


#before_login()
login()
#get_data()
