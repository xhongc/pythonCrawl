import requests
from pprint import pprint
import json

def get_data():
    #url ='https://wx.tenpay.com/userroll/userrolllist?count=10&sort_type=1&exportkey=ARWXt0ZDScMJgrNhzVf%2BKRQ%3D'
    url = 'https://wx.tenpay.com/userroll/userrolllist?count=5&sort_type=1&exportkey=ASYV8jvsx1DT18hVOFiMrNs%3D'
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; MI 5 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043808 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060133) NetType/WIFI Language/zh_CN',
        'Cookie': 'userroll_pass_ticket=R4jDmSFmcSxBVhSMm3idoRCbXfKn/NGk7sMC9OO+I0IHljEbCjIvBPWg6v9SQ7hx; export_key=ASYV8jvsx1DT18hVOFiMrNs=',
        #'Cookie': 'userroll_pass_ticket=7F48223D667A615458587767774758563D556A5A5F4348404A467F73B22FCB014; export_key=ASYV8jvsx1DT18hVOFiMrNs=',
        #'access_token':'6_twPg0B88ZyGlzw3QzW6WS0iTE4q0-dphZbHYkt_w5OK7RB9agWaIcYSKnWORXzW2XYZ3CNyZ7pZc_TCSbQXaRw',
        'Connection':'keep-alive',
        'X-Requested-With':'com.tencent.mm',
    }
    a = requests.get(url,verify=False,headers=headers)
    html = a.text
    res = json.loads(html,encoding='utf-8')
    #pprint(res)
    return res

def parse_data():
    res = get_data()
    record_list = res['record']
    water_list =[]
    for each in record_list:
        item = {}
        item['PayJe'] = each['fee']
        item['PayMore'] = each['title']
        item['PayNO'] = each['trans_id']
        water_list.append(item)
    return water_list

def for_api(item):
    params = item
    # print(data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    #api_url = 'http://778vpn.com/notify/selfZFBNotify?key=9902312&appid=151261552310206'
    api_url = 'http://192.168.3.111:8081/notify/selfZFBNotify?key=9902312&appid=151261552310206'
    a = requests.get(api_url, headers=headers, params=item)
    print(a.text)

def for_close_api():

    _id = conf.get('user', 'user_phone_id')
    _id = int(_id)

    sign = hashlib.md5()
    content = 'id={0}&key=BLhOMfb8THVuQDYliSzvRDyBQ47jE63p'.format(_id)
    sign.update(content.encode('utf-8'))
    sign = sign.hexdigest()
    data = {
        'id':_id,
        'sign':sign
    }
    close_url ='http://778vpn.com/other/closeChannel'
    a = requests.post(close_url,data=data)
    print(a.text)

#a = get_data()
#pprint(a)
item = {}
item['PayJe'] = 1
item['PayMore'] = '1.02'
item['PayNO'] = '100003950118020900074331252343611966'
item['payfangshi'] = 3
for_api(item)