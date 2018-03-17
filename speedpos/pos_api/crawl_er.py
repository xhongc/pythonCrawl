import requests
from scrapy.selector import Selector
import pymysql
import json
import time
from flask import Flask
from flask import request
from flask import jsonify,abort
from flask_cors import *
from datetime import datetime

app = Flask(__name__)
CORS(app,supports_credentials=True)

def speedpos(start_time,end_time,time_by='create_time',trade_type=None,order_status=None,page='1'):
    global session

    items = []
    url = 'https://mch.speedpos.cn/index/index'

    data = {
        'login_name':'2100800007925',
        'login_pwd':'f9bcac36'
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer':'https://mch.speedpos.cn/index',
        'X-Requested-With':'XMLHttpRequest'
    }
    session = requests.Session()
    html = session.post(url,headers=headers,data=data)
    print(html)
    # post_data = {
    #     '_loadpage':'1',
    #     'page':page,
    #     'start_time':start_time,
    #     'end_time':end_time,
    #     'time_by':time_by,
    #     'trade_type':trade_type,
    #     'order_status':order_status,
    # }
    # try:
    #     res = session.post('https://mch.speedpos.cn/orders/lists',headers=headers,data=post_data)
    #     selector = Selector(res)
    #     res_list = selector.xpath('//tr[@class="selectline"]')
    #     for each in res_list:
    #         item = {}
    #         each = each.xpath('./td/text()').extract()
    #         item['pay_time'] = each[0]
    #         item['order_time'] = each[1]
    #         item['order_num'] = each[3]
    #         item['pay_mode'] = each[5]
    #         item['pay_status'] = each[6]
    #         item['pay_money'] = each[7]
    #         # item['store_name'] = get_name(item['order_num'])
    #         items.append(item)
    #         result = json.dumps(items,indent=4,ensure_ascii=False)
    #     print(items)
    #     return result
    # total_money
    #----------------------------------------------------------
    # try:
    #     url = 'https://mch.speedpos.cn/orders/index'
    #     params = {
    #         'start_time':start_time,
    #         'end_time':end_time,
    #         'trade_type':''
    #     }
    #
    #     html = session.get(url,params=params,headers=headers)
    #     html = html.text
    #     html = json.loads(html,encoding='utf-8')
    #     fee = html['data']['total_fee'] * 0.01
    #     print(fee)
    # except:
    #     result = '大侠请重新来过'
    #     return result
    # ----------------------------------------------------------
    url = 'https://mch.speedpos.cn/orders/single'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/orders/single',

        'Upgrade-Insecure-Requests': '1'
    }
    data = {
        'out_trade_no': '',
        'order_no': '81020180315091307353780241408502',
        'transaction_id': ''
    }
    #cookie = session['upSession']

    res = session.post('https://mch.speedpos.cn/orders/single', headers=headers, data=data)
    #print(res.text)
    selector = Selector(res)
    res_list = selector.xpath('//tr[@class="selectline"]')
    #print(res_list)
    items = []
    total_money = 0
    for each in res_list:
        item = {}
        each = each.xpath('./td/text()').extract()
        print(each)
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
        #if switch == 'true':
            # print('switch is true')
            #item['store_name'] = get_name(item['order_num'])
        print(item)
        items.append(item)
def get_name(order_num):
    url = 'https://mch.speedpos.cn/orders/info?_loadpage=1'
    dataa = {'order_no': order_num}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
    res = session.post(url,headers=headers,data=dataa)
    #print(res.text)
    selector = Selector(res)
    title = selector.xpath('//div[@class="margin_r20 fl"]/input/@value').extract()
    name1 = title[4]
    name2 = title[7]
    if name1 in name2:

        print(name1,name2)
    else:
        print('m')
    return '0'

@app.route('/search', methods=['GET'])
def search():
    if not request.args['start_time'] and request.args['end_time']:
        abort(400)
    else:
        start_time = request.args['start_time']
        end_time = request.args['end_time']

    time_by = request.args['time_by']
    trade_type = request.args['trade_type']
    order_status = request.args['order_status']

    result = speedpos(start_time,end_time,time_by,trade_type,order_status)

    return result

if __name__ == '__main__':
    # app.run(
    #     host='192.168.3.17',
    #     port= 8080,
    #     debug=True)
    speedpos('2018-03-01 00:00:00','2018-03-01 23:59:59','create_time','','1','2')
