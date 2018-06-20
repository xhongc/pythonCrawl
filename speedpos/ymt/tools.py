import requests
import json
import time

def get_cookies():
    url = 'http://fzms.498.net/member.php/User/login.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    }
    html = requests.get(url, headers=headers)
    cookies = html.cookies
    cookie_one = '; '.join(['='.join(item) for item in cookies.items()])

    # print('aaaaaaaaa', cookie_one)
    url = 'http://fzms.498.net/member.php/User/loginCheck.html'
    data = {
        'account': '1001465123',
        'pwd': '888888',
        'verify': '',
        'operator': '0'
    }
    # cookie_one = 'PHPSESSID=n3appli2bpc0dv6865pop8iki4; SERVERID=17664eb733bc7a580c0226ebf503a84b|1528682884|1528682884; __tins__19094318=%7B%22sid%22%3A%201528682897362%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201528684697362%7D; __51cke__=; __51laig__=1'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '50',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie_one,
        'Host': 'fzms.498.net',
        'Origin': 'http://fzms.498.net',
        'Referer': 'http://fzms.498.net/member.php/User/login.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    # session = requests.session()
    html = requests.post(url, data=data, headers=headers)
    cookies = html.cookies
    cookies = '; '.join(['='.join(item) for item in cookies.items()])
    # print(cookies)

    all_Cookie = cookie_one + cookies
    return all_Cookie


def get_order(cookies):
    url = 'http://fzms.498.net/member.php/Flows/flowsList.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'fzms.498.net',
        'Origin': 'http://fzms.498.net',
        'Referer': 'http://fzms.498.net/member.php/User/login.html',
        'Cookie': cookies
    }
    html = requests.post(url, headers=headers)
    html = json.loads(html.text, encoding='utf-8')
    # print(html)

    content = html['data']
    # pprint(content)
    res = []
    result = []
    for each in content:
        item = {}
        c_time = each['c_time']
        time_local = time.localtime(int(c_time))
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        item['c_time'] = dt
        item['order_no'] = each['order_no']
        trade_type = each['trade_type']
        if trade_type == '1':
            item['trade_type'] = '支付宝'
        elif trade_type == '2':
            item['trade_type'] = '微信支付'
        else:
            item['trade_type'] = '支付'
        item['trade_money'] = each['trade_money']
        item['trade_status'] = '成功'
        item['real_money'] = each['real_money']
        item['beizhu'] = each['memo']
        res.append(item)

    return json.dumps(res, ensure_ascii=False)
