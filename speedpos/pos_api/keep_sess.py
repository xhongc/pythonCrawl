import requests
import time
import random


def fflash(wx_session):
    try:
        url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBills.do'
        wx_session = wx_session
        # print(wx_session)
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
            'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088' % (
                wx_session)
        }
        # year = billDate.split('-')[0]
        # month = billDate.split('-')[1]
        # day = billDate.split('-')[2]
        # reqmid = session['reqmid']
        # print('1a1a', reqmid)
        data = {
            'reqMid': '898352254990101',
            'pageSize': '15',
            'curPage': '1',
            'billDate': '2018年07月04日'
        }
        # print(data)
        html = requests.post(url, headers=headers, data=data)
        # print(html)
    except BaseException as e:
        print(e)
        return '0000'


def run():
    session_list = ['26710055-0662-4a35-b49b-ff1da810b433', 'e11b3d1b-05f3-4f49-8e74-d2c86fba068c', \
                    '0e3fe945-4391-4ba2-bdbe-399b9aad1e00', '27a696ea-1780-4c04-93ec-bd2ecf29e0e0', \
                    'a36ff750-865d-431d-b543-2e39c92491f4', 'f69c053d-94a2-4c32-aa17-9703db06d9d2', \
                    'c0a00b1a-829e-4099-ade0-d64afeb3d2bf', 'a5b704ed-e444-43ab-8f29-b51c618a51ea', \
                    'aa23815d-a216-4b00-86ca-052df67f38da'
                    ]
    for each in session_list:
        fflash(wx_session=each)
        time.sleep(1.41)
        print(each)


while 1:
    time.sleep(5)
    run()
    sleep_time = random.uniform(30, 65)
    time.sleep(sleep_time)
