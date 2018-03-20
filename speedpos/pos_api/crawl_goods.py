import requests
import configparser
from datetime import datetime
import json
import time
from scrapy.selector import Selector
import hashlib

conf = configparser.ConfigParser()
conf.read('goods.conf',encoding='utf-8')

def get_beizhu(params,wx_session):
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBill.do'
    params = params


    # print(params)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Host': 'qr.chinaums.com',
        'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=GMMdB5gvvcQjvhVv0NyJdy1CwtZrcQBSHj21-Q3cdpgu73bmjFZV!-1058374088' % (
            wx_session)
    }
    html = requests.get(url, params=params, headers=headers)
    # print(html.text)
    selector = Selector(html)
    detail = selector.xpath('//div[@class ="ums_text"]/span[@class="ums_text_value ums_margin_right8"]/text()').extract()[4].replace(' ', '').replace('\n', '')
    # print(detail)

    return detail

def get_data(page='1', switch='false', trade_type=''):

    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBills.do'
    wx_session = conf.get('settings','wx_session')
    reqmid = conf.get('settings','reqmid')
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
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    #billDate = '%s-%s-%s'%(year,month,day)
    billDate = '2018-03-19'
    # print('1a1a',reqmid)
    data = {
        'reqMid': reqmid,
        'pageSize': '15',
        'curPage': page,
        'billDate': '2018年03月19日' # % (year, month, day)
    }
    # print(data)

    html = requests.post(url, headers=headers, data=data)
    # print(trade_type)
    # print(json.loads(html.text))
    html = json.loads(html.text, encoding='utf-8')

    list_all = html['paymentList']['content']
    items = []
    for each in list_all:
        item = {}
        if each['targetSys'] == trade_type and trade_type == 'Alipay 2.0':
            #pay_time = each['payTime'] * 0.001
            # pay_time = time.localtime(pay_time)
            # dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
            # item['pay_time'] = dt
            item['PayNO'] = each['merOrderId']
            item['PayJe'] = round(each['totalAmount'] * 0.01, 2)
            item['trade_type'] = '1'
            if switch == 'true':
                params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                params = {
                    'billsQueryInfo': str(params_data),
                    'role': 'Merchant'}
                item['PayMore'] = get_beizhu(params,wx_session)
            items.append(item)
        elif each['targetSys'] == trade_type and trade_type == 'WXPay':
            # pay_time = each['payTime'] * 0.001
            # pay_time = time.localtime(pay_time)
            # dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
            # item['pay_time'] = dt
            item['PayNO'] = each['merOrderId']
            item['PayJe'] = round(each['totalAmount'] * 0.01, 2)
            item['payType'] = '6'
            if switch == 'true':
                params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                params = {
                    'billsQueryInfo': str(params_data),
                    'role': 'Merchant'}
                item['PayMore'] = get_beizhu(params,wx_session)
            items.append(item)
        elif trade_type == '':
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
    # print(items)
    return items

def for_api(item):
    params = item
    # print(data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    #api_url = 'http://778vpn.com/notify/selfZFBNotify?key=9902312&appid=151261552310206'
    api_url = 'http://uupp777.vicp.cc:28771/notify/selfZFBNotify?key=9902312&appid=151261552310206'
    a = requests.get(api_url, headers=headers, params=item)
    print(a.text)

def for_close_api():

    _id = conf.get('settings', 'id')
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

count =1
water_copy = []
def main():
    global count

    info = get_data(page='1', switch='true', trade_type='')
    try:
        for item in info:
            if count == 1:
                print('once%s' % item)
                for_api(item)
            elif item not in water_copy and len(water_copy) != 0:
                print('second%s' % item)
                for_api(item)
            else:
                pass
                # 　for_api(item)
                # print('不需要重复数据！')

        for item in info:
            water_copy.append(item)

        count = 2
    except TypeError as e:
        print(e)

while 1:

    main()
    time.sleep(1)

