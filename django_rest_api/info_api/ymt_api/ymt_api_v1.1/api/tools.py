import requests, json
import time


# 爬虫
def get_cookies(ymt_name, ymt_pwd):
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
        'account': ymt_name,
        'pwd': ymt_pwd,
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


def get_order(cookies, trade_type=0, page=1):
    url = 'http://fzms.498.net/member.php/Flows/flowsList.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'fzms.498.net',
        'Origin': 'http://fzms.498.net',
        'Referer': 'http://fzms.498.net/member.php/User/login.html',
        'Cookie': cookies
    }
    data = {
        'trade_type': trade_type,
        'page': page,
    }
    html = requests.post(url, headers=headers, data=data)
    html = json.loads(html.text, encoding='utf-8')
    # print(html)

    content = html['data']
    # pprint(content)
    res = []
    result = []
    data = {}
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

    data['code'] = '000000'
    data['total_page'] = int(len(res) / 16 + 0.5) + 1
    data['data'] = res
    # return json.dumps(res, ensure_ascii=False)
    return data


def get_dayorder(cookies, trade_type=0):
    url = 'http://fzms.498.net/member.php/Flows/dayFlowsList.html'
    # cookies = get_cookies()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'fzms.498.net',
        'Origin': 'http://fzms.498.net',
        'Referer': 'http://fzms.498.net/member.php/User/login.html',
        'Cookie': cookies
    }
    data = {
        'trade_type': trade_type
    }
    html = requests.post(url, headers=headers, data=data)
    html = json.loads(html.text, encoding='utf-8')
    content = html['data']
    res = []
    data = {}
    for each in content:
        item = {}
        c_time = each['stat_date']
        time_local = time.localtime(int(c_time))
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d", time_local)
        item['c_time'] = dt
        trade_type = each['trade_type']
        if trade_type == '1':
            item['trade_type'] = '支付宝'
        elif trade_type == '2':
            item['trade_type'] = '微信支付'
        else:
            item['trade_type'] = '支付'
        item['trade_money'] = each['trade_money']
        item['real_money'] = each['real_money']
        item['trade_num'] = each['trade_num']
        res.append(item)

    data['code'] = '000000'
    data['data'] = res
    return data


def get_monthorder(cookies, trade_type=0):
    url = 'http://fzms.498.net/member.php/Flows/monthFlowsList.html'
    # cookies = get_cookies()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'fzms.498.net',
        'Origin': 'http://fzms.498.net',
        'Referer': 'http://fzms.498.net/member.php/User/login.html',
        'Cookie': cookies
    }
    data = {
        'trade_type': trade_type
    }
    html = requests.post(url, headers=headers, data=data)
    html = json.loads(html.text, encoding='utf-8')
    content = html['data']
    res = []
    data = {}
    for each in content:
        item = {}
        c_time = each['stat_date']
        time_local = time.localtime(int(c_time))
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d", time_local)
        item['c_time'] = dt
        trade_type = each['trade_type']
        if trade_type == '1':
            item['trade_type'] = '支付宝'
        elif trade_type == '2':
            item['trade_type'] = '微信支付'
        else:
            item['trade_type'] = '支付'
        item['trade_money'] = each['trade_money']
        item['real_money'] = each['real_money']
        item['trade_num'] = each['trade_num']
        res.append(item)

    data['code'] = '000000'
    data['data'] = res
    return data


if __name__ == '__main__':
    print(get_monthorder())
