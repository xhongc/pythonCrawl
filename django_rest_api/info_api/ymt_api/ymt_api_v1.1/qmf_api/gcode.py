import requests
import json
from scrapy.selector import Selector
import random
import time
from datetime import datetime
import re

agents = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]


def random_agent():
    agent = random.choice(agents)
    return agent


class LFOrder(object):
    def __init__(self, username, password):
        self.session = requests.session()
        self.session.keep_alive = False
        self.username = username
        self.password = password
        self.PHPSESSID, self.SERVERID = self.login()

    def login(self):
        try:
            print('loging------%s---------' % self.username)
            url = 'http://daili.lfwin.com/Vendor/Public/login'
            headers = {
                'User-Agent': random_agent()
            }
            html = self.session.get(url=url, headers=headers)
            cookies = html.cookies.get_dict()
            # print('1111', cookies)
            PHPSESSID = cookies['PHPSESSID']
            SERVERID = cookies['SERVERID']
            login_headers = {
                'User-Agent': random_agent(),
                'Cookie': 'PHPSESSID=%s; updateInfo=1; SERVERID=%s' % (PHPSESSID, SERVERID)
            }
            data = {
                'username': self.username,
                'password': self.password
            }

            html = self.session.post(url=url, headers=login_headers, data=data, timeout=100)
            html = json.loads(html.text, encoding='utf-8')
            return PHPSESSID, SERVERID
        except BaseException as e:
            return '1', '1'

    def get_data(self):
        try:
            PHPSESSID = self.PHPSESSID
            SERVERID = self.SERVERID
            list_headers = {
                'Connection': 'close',
                'User-Agent': random_agent(),
                'Cookie': 'PHPSESSID=%s; updateInfo=1; SERVERID=%s' % (PHPSESSID, SERVERID)
            }
            dt = datetime.now().strftime('%Y-%m-%d')
            stime = dt + ' 00:00:00'
            etime = dt + ' 23:59:59'
            # print(stime, etime)
            params = {
                'stime': stime,
                'etime': etime
            }
            data_url = 'http://daili.lfwin.com/Vendor/Qrcode/lists?orderid=&m_paytype=alipay&sku_\
            id=&sid=&paystatus=&is_refund=&smoney=&emoney=&stime=&etime=&submit=1'
            data_url2 = 'http://daili.lfwin.com/Vendor/Qrcode/lists?orderid=&m_paytype=wxpay&sku_\
                        id=&sid=&paystatus=&is_refund=&smoney=&emoney=&submit=1'
            html = self.session.get(url=data_url, headers=list_headers, params=params)
            html2 = self.session.get(url=data_url2, headers=list_headers, params=params)
            # print(html.text)
            selector = Selector(html)
            selector2 = Selector(html2)
            res = selector.xpath('//tr')
            res2 = selector2.xpath('//tr')
            resp = res + res2
            items = []
            data = {}
            for each in resp:
                item = {}
                result = each.xpath('.//td/text()').extract()
                # print(result)
                if result:
                    item['order_no'] = result[0]
                    item['pay_money'] = result[3]
                    item['beizhu'] = result[8]
                    payType = result[7].replace('微信支付', '微信')
                    item['trade_type'] = payType
                    item['trade_status'] = '成功'
                    dt = result[6]
                    if dt != '---':
                        dt = dt + ':00'
                        item['c_time'] = dt
                        items.append(item)
            # print(items)
            data['code']='000000'
            data['data'] = items
            return data
        except BaseException as e:
            data = {'code': '1', 'msg': '未登录ku'}
            return data

    def get_free_data(self):
        try:
            PHPSESSID = self.PHPSESSID
            SERVERID = self.SERVERID
            list_headers = {
                'Connection': 'close',
                'User-Agent': random_agent(),
                'Cookie': 'PHPSESSID=%s; updateInfo=1; SERVERID=%s' % (PHPSESSID, SERVERID)
            }
            dt = datetime.now().strftime('%Y-%m-%d')
            stime = dt + ' 00:00:00'
            etime = dt + ' 23:59:59'
            # print(stime, etime)
            params = {

                'stime': stime,
                'etime': etime,

            }

            data_url = 'http://daili.lfwin.com/Vendor/Bill/lists?orderid=&m_paytype=allmobile&bank_type=-1&sid=&mid=0&cdid=0&smoney=&emoney=&paystatus=1&is_refund=-1&paytype=0&fix_qrcode=1&stime=2018-07-26+00%3A00%3A00&etime=2018-07-27+00%3A00%3A00&mch_orderid=&submit=1'
            html = self.session.get(url=data_url, headers=list_headers, params=params)
            # print(html.text)
            selector = Selector(html)
            res = selector.xpath('//tr')

            res_list = []

            for each in res:
                each = each.xpath('./td/a/@href').extract_first()
                if each:
                    each = 'http://daili.lfwin.com' + each
                    res_list.append(each)
            items = []
            for every in res_list:
                item = {}
                html = self.session.get(url=every, headers=list_headers)
                selector = Selector(html)
                li_label = selector.xpath('//li').extract()
                # print(li_label)
                resp = ''.join(li_label).replace('\n', '').replace('\t', '').replace('\r', '')
                # print(resp)

                item['trade_type'] = re.search('支付通道</label>(.*?)</li>', resp).group(1)
                item['order_no'] = re.search('支付流水号</label>(.*?)</li>', resp).group(1)
                item['pay_money'] = re.search('消费金额</label>(.*?)元 </li>', resp).group(1)
                item['c_time'] = re.search('支付时间</label>(.*?)</li>', resp).group(1)
                item['trade_status'] = re.search('付款状态</label>(.*?)<span', resp).group(1)
                item['beizhu'] = re.search('订单备注</label>(.*?)</li>', resp).group(1)
                items.append(item)
            # print(items)
            data = {}
            data['code'] = '000000'
            data['data'] = items
            return data
        except BaseException as e:
            data = {'code': '1', 'msg': '未登录ku'}
            return data

    def gcode(self, beizhu, money, sid, apikey):
        PHPSESSID = self.PHPSESSID
        SERVERID = self.SERVERID
        code_headers = {
            'Connection': 'close',
            'User-Agent': random_agent(),
            'Cookie': 'PHPSESSID=%s; updateInfo=1; SERVERID=%s' % (PHPSESSID, SERVERID)
        }
        data = {
            'pname': beizhu,
            'pnum': '',
            'picurl': '',
            'sid': sid,
            'apikey': apikey,
            'fixed': '1',
            'remarks': '0',
            'money': money,
            'mark': '',
            'sku_id': '0',
            'status': '1',
            'id': '0'
        }
        url = 'http://daili.lfwin.com/Vendor/Qrcode/qrpost'
        html = self.session.post(url=url, headers=code_headers, data=data)
        print(html.text)

    def get_code_url(self):
        PHPSESSID = self.PHPSESSID
        SERVERID = self.SERVERID
        url = 'http://daili.lfwin.com/Vendor/Qrcode/index?kw=&stime=&etime='
        code_headers = {
            'Connection': 'close',
            'User-Agent': random_agent(),
            'Cookie': 'PHPSESSID=%s; updateInfo=1; SERVERID=%s' % (PHPSESSID, SERVERID)
        }
        html = self.session.get(url=url, headers=code_headers)
        selector = Selector(html)
        res = selector.xpath('//tr')[1]
        res = res.xpath('./td/img/@src').extract_first()
        # final_url = 'http://daili.lfwin.com' + res
        res = res.split('/')[-1]
        res = res.split('_')[0]
        result_url = 'https://daili.lfwin.com/Home/Qrcode/qimg/id/' + res
        print(result_url)
        return result_url


class ForYizhufuApi(object):
    def __init__(self):
        self.session = requests.session()
        self.login_url = 'http://192.168.3.88:8080/auth/login'
        self.login_data = {
            'username': 'superAdmin',
            'password': '4fb292b6558eb0d7d299cceea64c4316'
        }
        self.get_url = 'http://192.168.3.88:8088/lamtsing/api/order-verifies'
        self.html, self.cookie = self.login()

    def login(self):
        self.session.get(url='http://192.168.3.88:8080')
        cookie = self.session.cookies.get_dict()
        print(cookie)
        cookies = cookie['XSRF-TOKEN']
        login_data = json.dumps(self.login_data)
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-XSRF-TOKEN': cookies,
        }
        html = self.session.post(url=self.login_url, data=login_data, headers=headers)
        print(html.text)
        html = json.loads(html.text)
        try:
            if html['status'] == 400:
                time.sleep(3.3)
                self.login()
        except:
            pass
        return html, cookies

    def post_data(self, data):
        html, cookie = self.html, self.cookie
        csrf = cookie
        token = html['access_token']
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-XSRF-TOKEN': csrf,
            'Cookie': f'access_token={token}; XSRF-TOKEN={csrf}'
        }

        data = json.dumps(data)
        try:
            html = self.session.post(url=self.get_url, headers=headers, data=data)
            print(html.text)
        except:
            pass

# a = LFOrder(username='tingting', password='tingting123')
# a.get_code_url()
