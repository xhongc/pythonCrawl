import requests
import json
from scrapy.selector import Selector

# url = 'https://mch.speedpos.cn/index/index'
#
# data = {
#     'login_name': '2100800007966',
#     'login_pwd': 'd976a22c'
# }
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
#     'Referer': 'https://mch.speedpos.cn/index',
#     'X-Requested-With': 'XMLHttpRequest'
# }
# session = requests.Session()
# html = session.post(url, headers=headers, data=data)
# html = json.loads(html.text,encoding='utf-8')
# cookies=requests.utils.dict_from_cookiejar(session.cookies)
#
# print(cookies)
cookies = {"authcookies": "lm2IPT9zmw9zCv%2FtbSmQib8hsBdha3VoQBsu8uAoxzwOvVh5aBtwiV6aTPafhg%2BkyvSYYKhMvkeIVhyAY36w7rENCllfk0MY%2FgHPfD7jhmUPRQaQm906vA2NiODU1kAI00JiMFWzfsLOev%2FB9DcoVzbIczkdSwtPQqYPQwceYXTxdgYW0bBS9ijglS0GnPwC"}

params = {
    'start_time':'2018-03-02 00:00:00',
    'end_time':'2018-03-02 23:59:59',
    'time_by':'create_time',
    'trade_type':'',
    'order_status':''
}
post_data = {
        '_loadpage':'1',
        'page':'1',
        'start_time':'2018-03-02 00:00:00',
        'end_time':'2018-03-02 23:59:59',
        'time_by':'create_time',
        'trade_type':'',
        'order_status':'',
    }
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
# html = requests.get('https://mch.speedpos.cn/orders/lists',cookies=cookies,params=params)
# print(html.text)
item = {}
items = []
res = requests.post('https://mch.speedpos.cn/orders/lists',data=post_data,cookies=cookies,headers=headers)
selector = Selector(res)
res_list = selector.xpath('//tr[@class="selectline"]')
print(res.text)
for each in res_list:
    each = each.xpath('./td/text()').extract()
    item['pay_time'] = each[0]
    item['order_time'] = each[1]
    item['order_num'] = each[3]
    item['pay_mode'] = each[5]
    item['pay_status'] = each[6]
    item['pay_money'] = each[7]
    items.append(item)
    result = json.dumps(items,indent=4,ensure_ascii=False)
    print(result)