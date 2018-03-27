import requests
import json
import re
def get():
    code = {}
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do'
    wx_session = '3723bf35-dfec-42e2-b408-a2f794c51544'

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
        # 'Cookie': 'SESSION=c9f5243a-4c3c-4825-ac4b-8236f717762c; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088',
        'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088' % (
            wx_session)
    }

    data = {
        'bizType': 'bills',
        'appId': '9',
        'instMid': 'QMFDEFAULT',
        'category': 'BILLS',
        'userId': 'XMSYSC',
        'userPwd': 'Xm123456',
        'nickName': '郑思凤'
    }
    # print(data)
    try:
        html = requests.post(url, headers=headers, data=data)
        # print(html.text)
    except:
        code['code'] = 0
        code['msg'] = u'登录失败！'
        code = json.dumps(code, ensure_ascii=False)
        return code

    html = html.text
    reqmid = re.search('var reqMid = "(.*?)";', html)
    print(reqmid)
    if reqmid is None:
        code['code'] = 0
        code['msg'] = u'账户已登录！请在微信上退出'
        code = json.dumps(code, ensure_ascii=False)
        return code



get()
