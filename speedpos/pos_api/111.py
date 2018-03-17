import requests
import json
def get():
    url = 'https://qr.chinaums.com/netpay-mer-portal/wxmanage/queryOrder.do'
    data = {
        'reqMid':'898393056911161',
        'merOrderId':'100018031586624041913340980',
        'billDate':'2018年03月15日'
    }
    headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
            'Host': 'qr.chinaums.com',
            'Cookie': 'SESSION=047879fd-89f0-4384-861f-f5c7602913ba; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=GMMdB5gvvcQjvhVv0NyJdy1CwtZrcQBSHj21-Q3cdpgu73bmjFZV!-1058374088'

        }
    html = requests.post(url,data=data,headers=headers)

    html = json.loads(html.text, encoding='utf-8')
    html = html['model']
    print(html)
    if html['targetSys'] == trade_type and trade_type == 'Alipay 2.0':
        item = {}
        items= []
        pay_time=html['payTime'] * 0.001
        pay_time = time.localtime(pay_time)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
        item['paytime'] = dt
        item['order_num'] = html['merOrderId']
        item['pay_money'] = round(html['totalAmount'] * 0.01, 2)
        item['trade_type'] = '支付宝支付'
        if switch == 'true':
            params_data = {'merOrderId': html['merOrderId'], 'billDate': billDate, 'mid': reqmid}
            params = {
                'billsQueryInfo': str(params_data),
                'role': 'Merchant'}
            item['detail'] = get_beizhu(params)
        items.append(item)

    elif html['targetSys'] == trade_type and trade_type == 'WXPay':
        item = {}
        items = []
        pay_time = html['payTime'] * 0.001
        pay_time = time.localtime(pay_time)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
        item['paytime'] = dt
        item['order_num'] = html['merOrderId']
        item['pay_money'] = round(html['totalAmount'] * 0.01, 2)
        item['trade_type'] = '支付宝支付'
        if switch == 'true':
            params_data = {'merOrderId': html['merOrderId'], 'billDate': billDate, 'mid': reqmid}
            params = {
                'billsQueryInfo': str(params_data),
                'role': 'Merchant'}
            item['detail'] = get_beizhu(params)
        items.append(item)
    items = json.dumps(items, ensure_ascii=False)

    return items
def get_data():
    url = 'https://mch.speedpos.cn/orders/single'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data= {
        'out_trade_no':'',
        'order_no':order_num,
        'transaction_id':''
    }
    cookie = session['upSession']
    res = requests.post('https://mch.speedpos.cn/orders/lists', headers=headers, data=post_data, cookies=cookie)
    selector = Selector(res)
    res_list = selector.xpath('//tr[@class="selectline"]')
    items = []
    total_money = 0
    for each in res_list:
        item = {}
        each = each.xpath('./td/text()').extract()
        item['pay_time'] = each[0]
        item['order_time'] = each[1]
        item['order_num'] = each[3]
        # item['pay_mode'] = each[5]
        if each[5] == '微信公众号支付':
            item['pay_mode'] = '微信支付'
        else:
            return '不支持该类型支付'
        item['pay_status'] = each[6]
        item['pay_money'] = each[7]
        # total_money += int(each[7])
        if switch == 'true':
            # print('switch is true')
            item['store_name'] = get_name(item['order_num'])
        # print(item)
        items.append(item)
        return result