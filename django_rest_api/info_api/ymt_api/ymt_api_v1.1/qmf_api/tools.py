import requests
import re
import json
import time
from datetime import datetime


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

        'Cookie': 'SESSION=3c02159f-4bf7-4ea2-beab-50ee45016e35; route=ff7ccc9ac07719e8e706ebafb1588dfa; \
        JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088'
    }

    data = {
        'bizType': 'bills',
        'appId': '9',
        'instMid': 'QMFDEFAULT',
        'category': 'BILLS',
        'userId': 'wysskcyd',
        'userPwd': 'Xm123456',
        'nickName': '刘凯'
    }
    # print(data)
    try:
        html = requests.post(url, headers=headers, data=data)
        # print(html.text)
    except BaseException as e:
        print(e)
    html = html.text

    reqmid = re.search('var reqMid = "(.*?)";', html)

    return reqmid


def get_data(page='1', switch='true', trade_type='', wx_session=None, reqmid=None):
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
        # year = billDate.split('-')[0]
        # month = billDate.split('-')[1]
        # day = billDate.split('-')[2]
        billDate = datetime.now().strftime('%Y年%m月%d日')
        reqmid = 898352254990101

        data = {
            'reqMid': reqmid,
            'pageSize': '15',
            'curPage': page,
            'billDate': billDate
        }
        # print(data)

        html = requests.post(url, headers=headers, data=data)
        # print(trade_type)
        # print(json.loads(html.text))
        html = json.loads(html.text, encoding='utf-8')
        print(html)
        total_money = html['sumAmount'] * 0.001
        total_money = round(total_money, 2)
        total_dict = {'total_money': str(total_money)}
        list_all = html['paymentList']['content']
        items = []
        data = {}
        for each in list_all:
            item = {}
            if each['targetSys'] == trade_type and trade_type == 'Alipay 2.0':
                pay_time = each['payTime'] * 0.001
                pay_time = time.localtime(pay_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
                item['pay_time'] = dt
                item['order_num'] = each['merOrderId']
                item['pay_money'] = round(each['totalAmount'] * 0.001, 2)
                item['trade_type'] = '支付宝支付'
                if switch == 'true':
                    params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                    params = {
                        'billsQueryInfo': str(params_data),
                        'role': 'Merchant'}
                    item['detail'] = get_beizhu(params)
                items.append(item)
            elif each['targetSys'] == trade_type and trade_type == 'WXPay':
                pay_time = each['payTime'] * 0.001
                pay_time = time.localtime(pay_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
                item['pay_time'] = dt
                item['order_num'] = each['merOrderId']
                item['pay_money'] = round(each['totalAmount'] * 0.001, 2)
                item['trade_type'] = '微信支付'
                if switch == 'true':
                    params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                    params = {
                        'billsQueryInfo': str(params_data),
                        'role': 'Merchant'}
                    item['detail'] = get_beizhu(params)
                items.append(item)
            elif trade_type == '':
                pay_time = each['payTime'] * 0.001
                pay_time = time.localtime(pay_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
                item['pay_time'] = dt
                item['order_num'] = each['merOrderId']
                item['pay_money'] = round(each['totalAmount'] * 0.001, 2)
                item['trade_type'] = each['targetSys'].replace('Alipay 2.0', '支付宝支付').replace('WXPay', '微信支付')
                if switch == 'true':
                    params_data = {'merOrderId': each['merOrderId'], 'billDate': billDate, 'mid': reqmid}
                    params = {
                        'billsQueryInfo': str(params_data),
                        'role': 'Merchant'}
                    item['detail'] = get_beizhu(params)
                items.append(item)
                # print(items)
        items.append(total_dict)
        items = json.dumps(items, ensure_ascii=False)
        data['code'] = '000000'
        data['data'] = items
        return data
    except BaseException as e:
        data = {'code': '1', 'msg': e}
        return data


def get_beizhu(params):
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBill.do'
    params = params

    # print(params)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 \
        (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 \
        MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Host': 'qr.chinaums.com',
        'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; \
        JSESSIONID=GMMdB5gvvcQjvhVv0NyJdy1CwtZrcQBSHj21-Q3cdpgu73bmjFZV!-1058374088'
    }
    html = requests.get(url, params=params, headers=headers)
    selector = Selector(html)
    detail = \
        selector.xpath('//div[@class ="ums_text"]/span[@class="ums_text_value ums_margin_right8"]/text()').extract()[
            4].replace(' ', '').replace('\n', '')
    # print(detail)

    return detail


if __name__ == '__main__':
    # print(login_qmf())
    print(get_data())
