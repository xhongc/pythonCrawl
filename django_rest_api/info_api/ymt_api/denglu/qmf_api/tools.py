import requests
import re
import json
import time, random
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
        'Cookie': 'fishmsg=1; uisroute=81db7a754b2503b3a951d254eb8f8b4e; nuismerwebsessionId=chinaums-newuis-dde134dd-a04f-4065-9eb3-dcd2ee801102; _ga=GA1.2.65013444.1530761979; Hm_lvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531993020; _gid=GA1.2.1285314808.1531993020; Hm_lpvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531993147',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/68.0.3440.17 Safari/537.36'
    }
    data = {
        'productName': productName,
        'amountType': '1',
        'productAmout': productAmout,
        'productId': productId
    }
    html = requests.post(url=url, headers=headers, data=data)
    data = {}
    res = html.text
    res = json.loads(res)

    data['code'] = '000000'
    data['data'] = res['qrCodeUrl']
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


def get_qmt_data(cookie, page):
    url = 'https://service.chinaums.com/uis-wxfront/wx/common/request/doProcess.do'
    page = int(page) - 1

    headers = {

        'Host': 'service.chinaums.com',
        'Connection': 'keep-alive',
        'Content-Length': '127',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://service.chinaums.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36 MicroMessenger/6.6.7.1320(0x26060734) NetType/WIFI Language/zh_CN',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://service.chinaums.com/uiswx/BIZ-WF-BILL/dang.html?role=2&userAppType=2&mchntName=%E6%AD%A6%E5%A4%B7%E5%B1%B1%E5%B8%82%E8%83%9C%E5%87%AF%E8%8C%B6%E4%B8%9A%E5%BA%97',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.9',
        # 'Cookie': 'uiswxftroute=8f244af579fb1977c154a6b4e377a7d6; Hm_lvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531476076; _ga=GA1.2.910577194.1531476077; _gid=GA1.2.1871546130.1531476077; Hm_lpvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531476096; JSESSIONID=D8CTyL0vVKpzqyZze4nia1pm3rol0jFfTvpp8Fo8zhcYybdfTQne!-2024523785',
        'Cookie': cookie,
        'X-Requested-With': 'com.tencent.mm',

    }
    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    # print(dt)
    data = {"appRequestDate": dt,
            "service": "qryRealTransListForWx",
            "pageSize": "15",
            "page": str(page),
            "isTotal": "",
            "qryRealType": "03"}
    data = json.dumps(data)
    html = requests.post(url, headers=headers, data=data)
    html = json.loads(html.text)

    try:
        html = html['content']

    except:
        data = {'code': '11', 'msg': '无html数据'}
        return data
    item = []
    for each in html:
        seqId = each['seqId']
        item.append(seqId)

    return item


def get_qmf_beizhu(seqId, cookie):
    url = 'https://service.chinaums.com/uis-wxfront/wx/common/request/doProcess.do '
    headers = {
        'Host': 'service.chinaums.com',
        'Connection': 'keep-alive',
        'Content-Length': '114',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://service.chinaums.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/64.0.3282.137 Mobile Safari/537.36 MicroMessenger/6.6.7.1320(0x26060734) NetType/WIFI Language/zh_CN',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://service.chinaums.com/uiswx/BIZ-WF-BILL/CSAOBDetails.html?billDate=20180713&seqId=6276888387&mchntName=%E6%AD%A6%E5%A4%B7%E5%B1%B1%E5%B8%82%E8%83%9C%E5%87%AF%E8%8C%B6%E4%B8%9A%E5%BA%97',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.9',
        # 'Cookie': 'uiswxftroute=8f244af579fb1977c154a6b4e377a7d6; Hm_lvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531476076; _ga=GA1.2.910577194.1531476077; _gid=GA1.2.1871546130.1531476077; Hm_lpvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531476096; JSESSIONID=D8CTyL0vVKpzqyZze4nia1pm3rol0jFfTvpp8Fo8zhcYybdfTQne!-2024523785',
        'Cookie': cookie,
        'X-Requested-With': 'com.tencent.mm'
    }
    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    billDate = datetime.now().strftime('%Y%m%d')
    data = {"appRequestDate": dt, "service": "qryRealTransDetailForWx", "billDate": billDate,
            "seqId": seqId}
    data = json.dumps(data)
    html = requests.post(url, headers=headers, data=data)
    html = html.text
    html = json.loads(html, encoding='utf-8')

    item = {}

    if html['responseCode'] == '555555':
        return '007', '007'
    pay_money = html['total_amount'] * 0.01
    item['pay_money'] = pay_money
    item['order_no'] = html['mer_order_id']
    try:
        item['beizhu'] = html['memo']
    except:
        item['beizhu'] = '无'
    item['trade_status'] = html['status']
    item['c_time'] = html['pay_time']
    try:
        item['beizhu2'] = html['counter_no']
    except:
        item['beizhu2'] = '无'
    item['trade_type'] = html['target_sys']
    # print(item)
    return item, pay_money


def get_all_data(cookie, page):
    item = get_qmt_data(cookie, page)

    items = []
    data = {}
    total_money = 0
    for each in item:
        result = get_qmf_beizhu(each, cookie)
        if result[0] == '007':
            data = {'code': '001122', 'msg': '会话失效', 'data': []}
            return data
        item = result[0]
        total_money += result[1]

        items.append(item)
    data['code'] = '000000'
    data['data'] = items

    # print(items)
    return data


USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.46 Safari/525.19',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.43 Safari/525.19 ',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.42 Safari/525.19 ',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.4.154.31 Safari/525.19 ',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.0 Safari/525.19 ',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.152.0 Safari/525.19 ',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.151.0 Safari/525.19 '
]


def random_agent():
    agent = random.choice(USER_AGENTS)
    return agent


def get_jl_data(cookie, page):
    url = 'https://b.jlpay.com/cost/queryCostincom.mt'
    headers = {
        'Cookie': cookie,
        'Host': 'b.jlpay.com',
        'Origin': 'https://b.jlpay.com',
        'Referer': 'https://b.jlpay.com/cost/toCostincom',
        'User-Agent': random_agent(),
        'X-Requested-With': 'XMLHttpRequest'
    }
    dt = datetime.now().strftime('%Y-%m-%d')
    dt = '2018-07-18'
    start_date = dt + ' 00:00:00'
    end_date = dt + ' 23:59:59'
    data = {
        'pageIndex': page,
        'pageSize': '15',
        'busiSubType': '',
        'debitCreditFlag': '',
        'starTime': start_date,
        'endTime': end_date,
        'orderNo': ''
    }
    html = requests.post(url=url, headers=headers, data=data)
    html = json.loads(html.text)

    try:
        res = html['data']
    except KeyError:
        data = {'code': '000000', 'msg': '未登录'}
        return data

    items = []
    data = {}
    for each in res:
        item = {}
        item['c_time'] = each['transTime']
        item['trade_type'] = each['tradeType']
        item['pay_money'] = each['sourceAmt']
        item['beizhu'] = each['remarks']
        item['order_no'] = each['orderId']
        items.append(item)
    data['code'] = '000000'
    data['data'] = items
    return data


if __name__ == '__main__':
    # print(applyCode('1', '2', '3'))
    # print(get_data(wx_session='5427ee52-24ad-47f0-b46c-bfde60417d96', reqmid='898352259410102'))
    # get_all_data(
    #     cookie='uiswxftroute=8f244af579fb1977c154a6b4e377a7d6; Hm_lvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531476076; _ga=GA1.2.910577194.1531476077; _gid=GA1.2.1871546130.1531476077; Hm_lpvt_1c0d3d1413bff5b48a4a97f64a35f6a4=1531476096; JSESSIONID=D8CTyL0vVKpzqyZze4nia1pm3rol0jFfTvpp8Fo8zhcYybdfTQne!-2024523785',
    #     page='1')
    print(get_jl_data(
        cookie='SESSION=3e3cd839-0ab6-4112-a897-58eb920edae3; mt_merchant_session_id=3e3cd839-0ab6-4112-a897-58eb920e;',
        page='1'))
