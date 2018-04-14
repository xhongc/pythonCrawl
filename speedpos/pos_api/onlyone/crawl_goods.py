import requests
import configparser
from datetime import datetime
import json
import time
from scrapy.selector import Selector
import hashlib
import threading


conf = configparser.ConfigParser()
conf.read('goods.conf',encoding='utf-8')

def get_beizhu(params,wx_session):
    try:
        url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBill.do'
        params = params


        #print(params)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
            'Host': 'qr.chinaums.com',
            'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=GMMdB5gvvcQjvhVv0NyJdy1CwtZrcQBSHj21-Q3cdpgu73bmjFZV!-1058374088' % (
                wx_session)
        }
        html = s.get(url, params=params, headers=headers,timeout = 500)
        # print(html.text)
        selector = Selector(html)
        detail = selector.xpath('//div[@class ="ums_text"]/span[@class="ums_text_value ums_margin_right8"]/text()').extract()[4].replace(' ', '').replace('\n', '')
        # print(detail)

        return detail
    except:
        return 'error'

def get_data(page='1', switch='false',user=''):
    global s

    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBills.do'
    wx_session = conf.get('settings','wx_session')
    #print(user)
    reqmid = conf.get(user,'reqmid')
    #　print(reqmid)
    # reqmid = conf.get('user1','reqmid')
    # print(wx_session)
    headers = {
        'Host': 'qr.chinaums.com',
        #'Connection': 'keep-alive',
        #'Content-Length': '89',
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
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    billDate = '%s-%s-%s'%(year,month,day)
    # billDate = '2018-03-19'
    # print('1a1a',reqmid)
    data = {
        'reqMid': reqmid,
        'pageSize': '15',
        'curPage': page,
        'billDate': '%s年%s月%s日' % (year, month, day)
    }
    # print(data)
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    try:
        html = s.post(url, headers=headers, data=data,timeout = 500)
        # print(trade_type)
        # print(json.loads(html.text))
        html = json.loads(html.text, encoding='utf-8')
        list_all = html['paymentList']['content']
        items = []
        for each in list_all:
            item = {}
            # pay_time = each['payTime'] * 0.001
            # pay_time = time.localtime(pay_time)
            # dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
            # item['pay_time'] = dt
            item['PayNO'] = each['merOrderId']
            item['PayJe'] = round(each['totalAmount'] * 0.01, 2)
            item['payType'] = each['targetSys'].replace('Alipay 2.0', '1').replace('WXPay', '6')
            if switch == 'true':
                params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                params = {
                    'billsQueryInfo': str(params_data),
                    'role': 'Merchant'}
                item['PayMore'] = get_beizhu(params,wx_session)
            items.append(item)
            # print(items)
        #items = json.dumps(items, ensure_ascii=False)
        print('%s:%s'%(user,items))
        return items
    except BaseException as e:
        print('getdata',e)
        time.sleep(3)


def for_api(item):
    params = item
    # print(data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    #api_url = 'http://778vpn.com/notify/selfZFBNotify?key=9902312&appid=151261552310206'
    api_url = 'http://778vpn.com/notify/selfYLSWNotify?key=9902312&appid=151261552310206'
    a = requests.get(api_url, headers=headers, params=item)
    print(a.text)

def for_close_api(user):

    _id = conf.get(user, 'id')
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


def main1():
    count = 1
    water_copy = []
    user = threading.current_thread().name
    while 1:
        print(user)
        info = get_data(page='1', switch='true',user=user)
        # print('1',info)
        try:
            for item in info:
                if count == 1:
                    print('%s:%s' % (user,item))
                    for_api(item)
                elif item not in water_copy and len(water_copy) != 0:
                    print('second%s' % item)
                    for_api(item)
                else:
                    pass
                    # for_api(item)
                    water_copy.clear()
                    # print('不需要重复数据！')

            # for item in info:
            #     water_copy.append(item)
            water_copy = info
            count = 2
        except BaseException as e:
            print(e)
            # for_close_api(user)
            # break
        time.sleep(1.1)


def main2():
    count = 1
    water_copy = []
    user = threading.current_thread().name
    while 1:
        print(user)
        info = get_data(page='1', switch='true',user=user)
        # print('2',info)
        try:
            for item in info:
                if count == 1:
                    print('%s:%s' % (user, item))
                    for_api(item)
                elif item not in water_copy and len(water_copy) != 0:
                    print('second%s' % item)
                    for_api(item)
                else:
                    pass
                    # for_api(item)
                    # print('不需要重复数据！')

            # for item in info:
            #     water_copy.append(item)
            water_copy = info
            count = 2
        except BaseException as e:
            print(e)
            # for_close_api(user)
            # break
        time.sleep(1.2)
def main3():
    count = 1
    water_copy = []
    user = threading.current_thread().name
    while 1:
        print(user)
        info = get_data(page='1', switch='true',user=user)
        #　print('3',info)
        try:
            for item in info:
                if count == 1:
                    print('%s:%s' % (user, item))
                    for_api(item)
                elif item not in water_copy and len(water_copy) != 0:
                    print('second%s' % item)
                    for_api(item)
                else:
                    pass
                    # for_api(item)
                    #print('不需要重复数据！')

            # for item in info:
            #     water_copy.append(item)
            water_copy = info
            count = 2
        except BaseException as e:
            print('3',e)
            # for_close_api(user)
            # break
        time.sleep(1.3)
def main4():
    count = 1
    water_copy = []
    user = threading.current_thread().name
    while 1:
        print(user)
        info = get_data(page='1', switch='true',user=user)
        # print('4',info)
        try:
            for item in info:
                if count == 1:
                    print('%s:%s' % (user, item))
                    for_api(item)
                elif item not in water_copy and len(water_copy) != 0:
                    print('second%s' % item)
                    for_api(item)
                else:
                    pass
                    # for_api(item)
                    # print('不需要重复数据！')

            # for item in info:
            #     water_copy.append(item)
            water_copy = info
            count = 2
        except BaseException as e:
            print(e)
            # for_close_api(user)
            # break
        time.sleep(1.4)

def main5():
    count = 1
    water_copy = []
    user = threading.current_thread().name
    while 1:
        print(user)
        info = get_data(page='1', switch='true',user=user)
        # print('5',info)
        try:
            for item in info:
                if count == 1:
                    print('%s:%s' % (user, item))
                    for_api(item)
                elif item not in water_copy and len(water_copy) != 0:
                    print('second%s' % item)
                    for_api(item)
                else:
                    pass
                    # for_api(item)
                    #print('不需要重复数据！')

            # for item in info:
            #     water_copy.append(item)
            water_copy = info
            count = 2
        except BaseException as e:
            print(e)
            # for_close_api(user)
            # break
        time.sleep(1.5)

if conf.get('user1','reqmid'):
    t1 = threading.Thread(target=main1,name='user1')
    t1.start()

if conf.get('user2','reqmid'):
    t2 = threading.Thread(target=main2,name='user2')
    t2.start()

if conf.get('user3','reqmid'):
    t3 = threading.Thread(target=main3,name='user3')
    t3.start()

if conf.get('user4','reqmid'):
    t4 = threading.Thread(target=main4,name='user4')
    t4.start()

if conf.get('user5','reqmid'):
    t5 = threading.Thread(target=main5,name='user5')
    t5.start()
