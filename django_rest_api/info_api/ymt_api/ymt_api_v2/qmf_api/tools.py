import requests
import re
import json
import time
from datetime import datetime
from scrapy.selector import Selector


def login_qmf():
    global code
    code = {}
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do'

    headers = {
        'Host': 'qr.chinaums.com',
        'Connection': 'keep-alive',
        'Content-Length': '114',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://qr.chinaums.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 \
        (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 \
        MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp\
        ,image/apng,*/*;q=0.8',
        'Referer': 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do?instMid=QMFDEFAULT&bizType=bills\
        &appId=9&category=BILLS&wxAppId=wx3220f3baaad5ed30',

        'Cookie': 'SESSION=b1c93c27-9674-48cf-b271-71a5cb8330fd; route=ff7ccc9ac07719e8e706ebafb1588dfa; \
        JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088'
    }

    data = {
        'bizType': 'bills',
        'appId': '9',
        'instMid': 'QMFDEFAULT',
        'category': 'BILLS',
        'userId': 'lsszqqwlg',
        'userPwd': 'Xm123456',
        'nickName': '雷仕秀'
    }
    # print(data)
    try:
        html = requests.post(url, headers=headers, data=data)
        # print(html.text)
    except BaseException as e:
        print(e)
    html = html.text

    reqmid = re.search('var reqMid = "(.*?)";', html)
    # print(reqmid)
    return reqmid


def get_data(page='1', switch='1', trade_type='', wx_session=None, reqmid=None,
             billDate=datetime.now().strftime('%Y-%m-%d')):
    try:
        url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBills.do'

        # print(wx_session)
        headers = {
            'Host': 'qr.chinaums.com',
            'Connection': 'keep-alive',
            'Content-Length': '89',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://qr.chinaums.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 \
            (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36\
             MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; \
            JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088' % (wx_session)

        }
        # billDate = datetime.now().strftime('%Y-%m-%d')
        year = billDate.split('-')[0]
        month = billDate.split('-')[1]
        day = billDate.split('-')[2]

        # print('1111111', billDate)
        # reqmid = 898352254990101

        data = {
            'reqMid': reqmid,
            'pageSize': '15',
            'curPage': page,
            'billDate': '%s年%s月%s日' % (year, month, day)
        }
        # print(data)

        html = requests.post(url, headers=headers, data=data, timeout=10)

        # print(trade_type)
        # print(json.loads(html.text))
        html = json.loads(html.text, encoding='utf-8')
        # print(html)

        list_all = html['paymentList']['content']
        items = []
        data = {}
        total_money = 0

        for each in list_all:
            item = {}
            if each['targetSys'] == trade_type and trade_type == 'Alipay 2.0':
                c_time = each['payTime'] * 0.001
                c_time = time.localtime(c_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", c_time)
                item['c_time'] = dt
                item['order_no'] = each['merOrderId']
                item['pay_money'] = round(each['totalAmount'] * 0.01, 3)
                item['trade_type'] = '支付宝支付'
                if switch == '1':
                    params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                    params = {
                        'billsQueryInfo': str(params_data),
                        'role': 'Merchant'}
                    item['beizhu'] = get_beizhu(params, wx_session)[0]
                    item['beizhu2'] = get_beizhu(params, wx_session)[1]
                item['trade_status'] = '支付成功'
                items.append(item)
            elif each['targetSys'] == trade_type and trade_type == 'WXPay':
                c_time = each['payTime'] * 0.001
                c_time = time.localtime(c_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", c_time)
                item['c_time'] = dt
                item['order_no'] = each['merOrderId']
                item['pay_money'] = round(each['totalAmount'] * 0.01, 3)
                item['trade_type'] = '微信支付'
                if switch == '1':
                    params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                    params = {
                        'billsQueryInfo': str(params_data),
                        'role': 'Merchant'}
                    item['beizhu'] = get_beizhu(params, wx_session)[0]
                    item['beizhu2'] = get_beizhu(params, wx_session)[1]
                item['trade_status'] = '支付成功'
                items.append(item)
            elif trade_type == '':
                c_time = each['payTime'] * 0.001
                c_time = time.localtime(c_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", c_time)
                item['c_time'] = dt
                item['order_no'] = each['merOrderId']
                item['pay_money'] = round(each['totalAmount'] * 0.01, 3)
                item['trade_type'] = each['targetSys'].replace('Alipay 2.0', '支付宝支付').replace('WXPay', '微信支付')
                if switch == '1':
                    params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                    params = {
                        'billsQueryInfo': str(params_data),
                        'role': 'Merchant'}
                    item['beizhu'] = get_beizhu(params, wx_session)[0]
                    item['beizhu2'] = get_beizhu(params, wx_session)[1]
                item['trade_status'] = '支付成功'
                items.append(item)
                # print(items)
            total_money += round(each['totalAmount'] * 0.01, 3)
        # items = json.dumps(items, ensure_ascii=False)
        data['code'] = '000000'
        data['data'] = items
        data['total_page'] = int(html['paymentList']['total'] / 15) + 1
        data['count'] = html['paymentList']['total']
        data['total_money'] = str(total_money)
        # print('data:', data)

        return data
    except BaseException as e:
        data = {'code': '1', 'msg': '未登录wx'}
        print('aaaaaaaaaa', e)
        return data


def get_beizhu(params, wx_session):
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBill.do'
    params = params

    # print(params)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 \
        (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 \
        MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Host': 'qr.chinaums.com',
        'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; \
        JSESSIONID=GMMdB5gvvcQjvhVv0NyJdy1CwtZrcQBSHj21-Q3cdpgu73bmjFZV!-1058374088' % (wx_session)
    }
    html = requests.get(url, params=params, headers=headers)
    # print(html.text)
    selector = Selector(html)
    beizhu = \
        selector.xpath('//div[@class ="ums_text"]/span[@class="ums_text_value ums_margin_right8"]/text()').extract()[
            5].replace(' ', '').replace('\n', '')
    # print(beizhu)
    beizhu2 = \
        selector.xpath('//div[@class ="ums_text"]/span[@class="ums_text_value ums_margin_right8"]/text()').extract()[
            4].replace(' ', '').replace('\n', '')
    # print(beizhu, beizhu2)
    return beizhu, beizhu2


def applyCode(productName, productAmout, productId):
    url = 'https://service.chinaums.com/uis/qrCodeController/applyQRCode'
    headers = {
        'Cookie': 'uisroute=52f19a93ba008e36206cbb159c674dac; nuismerwebsessionId=chinaums-newuis-0b6d3140-b79d-4e1f-a11b-b576361bbeb4; _ga=GA1.2.65013444.1530761979; Hm_lvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531374562; _gid=GA1.2.211168171.1531374562; _gat=1; Hm_lpvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531374745',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/68.0.3440.17 Safari/537.36'
    }
    data = {
        'productName': productName,
        'amountType': '1',
        'productAmout': productAmout,
        'productId': productId
    }
    html = requests.post(url=url, headers=headers)

    data = html.text

    return data


def for_api(item):
    params = item

    # print(data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

    }
    api_url = 'http://778vpn.com/notify/selfYLSWNotify?key=9902312&appid=151261552310206'
    # api_url = 'http://192.168.3.23:8081/notify/selfZFBNotify'
    a = requests.get(api_url, headers=headers, params=item, timeout=20)
    a = a.text
    data = {}
    data['code'] = '000000'
    data['data'] = a
    return data


if __name__ == '__main__':
    # print(applyCode('1', '2', '3'))
    print(get_data(wx_session='5427ee52-24ad-47f0-b46c-bfde60417d96', reqmid='898352259410102'))
