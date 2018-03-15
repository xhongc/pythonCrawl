#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from scrapy.selector import Selector
import json
import time
import random
import re
from flask import Flask
from flask import request, session
from flask import jsonify, abort
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
import threading

# 数据库地址
databaseurl = 'mysql://root:xhongc@localhost/info'
app = Flask(__name__)
# flask 解决跨域问题
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 数据修改自动提交
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'xhc1950'
db = SQLAlchemy(app)


# 创建数据库
class Fire_user(db.Model):
    __tablename__ = 'fire_user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login_name = db.Column(db.String(255), nullable=True)
    login_pwd = db.Column(db.String(255), nullable=True)
    login_chinesename = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=True)
    user_pwd = db.Column(db.String(255), nullable=True)
    wx_session = db.Column(db.String(255), nullable=True)
    reqmid = db.Column(db.String(255), nullable=True)

    def __init__(self, login_name, login_pwd, login_chinesename, user_name, user_pwd, wx_session, reqmid):
        self.login_name = login_name
        self.login_pwd = login_pwd
        self.login_chinesename = login_chinesename
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.wx_session = wx_session
        self.reqmid = reqmid


db.create_all()


class Water_user(db.Model):
    __tablename__ = 'water_user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login_name = db.Column(db.String(255), nullable=True)
    login_pwd = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=True)
    user_pwd = db.Column(db.String(255), nullable=True)

    def __init__(self, login_name, login_pwd, user_name, user_pwd):
        self.login_name = login_name
        self.login_pwd = login_pwd
        self.user_name = user_name
        self.user_pwd = user_pwd


db.create_all()


# 获取商品备注
def get_name(order_num):
    url = 'https://mch.speedpos.cn/orders/info?_loadpage=1'
    dataa = {'order_no': order_num}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
    cookie = session['upSession']

    res = requests.post(url, headers=headers, data=dataa, cookies=cookie)
    # print(res.text)
    selector = Selector(res)
    title = selector.xpath('//div[@class="margin_r20 fl"]/input/@value').extract()
    name1 = title[4]
    name2 = title[7]
    # print(name1,name2)
    if name1 in name2:
        # print(name1, name2)
        return '无'
    else:
        return name1


# 获取总金额
def get_total_money(start_time, end_time, trade_type):
    try:
        url = 'https://mch.speedpos.cn/orders/index'
        params = {
            'start_time': start_time,
            'end_time': end_time,
            'trade_type': trade_type
        }
        cookie = session['upSession']
        headers = session['headers']
        html = requests.get(url, params=params, headers=headers, cookies=cookie)
        html = html.text
        html = json.loads(html, encoding='utf-8')
        fee = html['data']['total_fee'] * 0.01
        # print(fee)
        return fee
    except:
        result = '00'
        return result


# sp 查询
def speedpos(start_time, end_time, trade_type, page='1', switch='false'):
    # print('switch:',switch)
    code = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
    post_data = {
        '_loadpage': '1',
        'page': page,
        'start_time': start_time,
        'end_time': end_time,
        'time_by': 'pay_time',
        'trade_type': trade_type,
        'order_status': '2',
    }
    # 将cookie 存在session中全局调用
    cookie = session['upSession']
    session['headers'] = headers
    # print('new',cookie)
    # upSession = requests.Session()
    # 获取数据
    try:
        res = requests.post('https://mch.speedpos.cn/orders/lists', headers=headers, data=post_data, cookies=cookie)
        # 　print(res.text)
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
        # 获取总金额
        total_dict = {}
        total_money = get_total_money(start_time, end_time, trade_type)
        total_money = round(total_money, 2)
        total_dict['total_money'] = str(total_money)
        items.append(total_dict)
        result = json.dumps(items, indent=4, ensure_ascii=False)
        # print(items)
        return result
    except:
        code['code'] = 0
        code['msg'] = 'cuowu'
        code = json.dumps(code, ensure_ascii=False)
        return code


# qmf查询
def get_data(billDate, page='1', switch='false', trade_type=''):
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBills.do'
    wx_session = session['wx_session']
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
    year = billDate.split('-')[0]
    month = billDate.split('-')[1]
    day = billDate.split('-')[2]
    reqmid = session['reqmid']
    # print('1a1a',reqmid)
    data = {
        'reqMid': reqmid,
        'pageSize': '15',
        'curPage': page,
        'billDate': '%s年%s月%s日' % (year, month, day)
    }
    # print(data)

    html = requests.post(url, headers=headers, data=data)
    # print(trade_type)
    # print(json.loads(html.text))
    html = json.loads(html.text, encoding='utf-8')

    total_money = html['sumAmount'] * 0.01
    total_money = round(total_money, 2)
    total_dict = {'total_money': str(total_money)}
    list_all = html['paymentList']['content']
    items = []
    for each in list_all:
        item = {}
        if each['targetSys'] == trade_type and trade_type == 'Alipay 2.0':
            pay_time = each['payTime'] * 0.001
            pay_time = time.localtime(pay_time)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", pay_time)
            item['pay_time'] = dt
            item['order_num'] = each['merOrderId']
            item['pay_money'] = round(each['totalAmount'] * 0.01, 2)
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
            item['pay_money'] = round(each['totalAmount'] * 0.01, 2)
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
            item['pay_money'] = round(each['totalAmount'] * 0.01, 2)
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
    return items


# 获取备注
def get_beizhu(params):
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBill.do'
    params = params
    wx_session = session['wx_session']

    # print(params)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Host': 'qr.chinaums.com',
        'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=GMMdB5gvvcQjvhVv0NyJdy1CwtZrcQBSHj21-Q3cdpgu73bmjFZV!-1058374088' % (
            wx_session)
    }
    html = requests.get(url, params=params, headers=headers)
    selector = Selector(html)
    detail = \
        selector.xpath('//div[@class ="ums_text"]/span[@class="ums_text_value ums_margin_right8"]/text()').extract()[
            4].replace(' ', '').replace('\n', '')
    # print(detail)

    return detail


# 登陆POST
def login(login_name, login_pwd):
    global upSession
    item = {}
    items = []
    url = 'https://mch.speedpos.cn/index/index'

    data = {
        'login_name': login_name,
        'login_pwd': login_pwd
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
    upSession = requests.Session()
    html = upSession.post(url, headers=headers, data=data)
    cookies = requests.utils.dict_from_cookiejar(upSession.cookies)
    # Water_user.query.filter_by(login_name=login_name).update({'cookies': cookies})
    session['upSession'] = cookies
    # print(cookies)


def login_qmf(login_name, login_pwd, login_chinesename):
    global session, code
    code = {}
    url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do'

    user1 = Fire_user.query.filter_by(login_name='fa4418').first()
    user = Fire_user.query.filter_by(login_name=login_name).first()
    wx_session = user1.wx_session
    # if user.wx_session is None:
    #     user = Fire_user.query.filter_by(login_name='fa4418').first()
    #     wx_session = user.wx_session
    # print(wx_session)
    session['wx_session'] = wx_session
    headers = {
        'Host': 'qr.chinaums.com',
        'Connection': 'keep-alive',
        'Content-Length': '114',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://qr.chinaums.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
        'Referer': 'https://qr.chinaums.com/netpay-mer-portal/merchant/merAuth.do?instMid=QMFDEFAULT&bizType=bills&appId=9&category=BILLS&wxAppId=wx3220f3baaad5ed30',
        # 'Cookie': 'SESSION=c9f5243a-4c3c-4825-ac4b-8236f717762c; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088',
        'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088' % (
            wx_session)
    }

    data = {
        'bizType': 'bills',
        'appId': '9',
        'instMid': 'QMFDEFAULT',
        'category': 'BILLS',
        'userId': login_name,
        'userPwd': login_pwd,
        'nickName': login_chinesename
    }
    # print(data)
    try:
        html = requests.post(url, headers=headers, data=data)
        # print(html.text)
    except:
        code['code'] = 0
        code['msg'] = u'登录失败！'
        code = json.dumps(code, ensure_ascii=False)
        return code

    if user.reqmid == 'none':
        html = html.text
        reqmid = re.search('var reqMid = "(.*?)";', html)
        if reqmid is None:
            code['code'] = 0
            code['msg'] = u'账户已登录！请在微信上退出'
            code = json.dumps(code, ensure_ascii=False)
            return code
        else:
            result = reqmid.group(1)
            user = Fire_user.query.filter_by(login_name=login_name).update({'reqmid': result})
            db.session.commit()
            session['reqmid'] = result
            # print(result)
            return result
    else:
        code['code'] = 3
        code['msg'] = u'账户已登录！'
        code = json.dumps(code, ensure_ascii=False)
        user = Fire_user.query.filter_by(login_name=login_name).first()
        session['reqmid'] = user.reqmid
        return code


# 登陆接口
@app.route('/login', methods=['POST'])
def login_api():
    global code
    code = {}
    login_name = request.form.get('login_name', 'none value')
    login_pwd = request.form.get('login_pwd', 'none value')
    print(login_name, login_pwd)
    # 验证密码
    try:
        get_login_name = Water_user.query.filter_by(login_name=login_name).first()
        if get_login_name is not None:
            if get_login_name.login_pwd == login_pwd:
                login(login_name, login_pwd)
                code['code'] = 1
                code['msg'] = u'管理者登陆'
                code = json.dumps(code, ensure_ascii=False)
                return code
    except BaseException as e:
        print('1', e)
    try:

        get_user_name = Water_user.query.filter_by(user_name=login_name).first()
        if get_user_name is not None:
            if get_user_name.user_pwd == login_pwd:
                login_name = get_user_name.login_name
                login_pwd = get_user_name.login_pwd
                login(login_name, login_pwd)
                code['code'] = 2
                code['msg'] = u'sp用户登陆'
                session['code'] = '2'
                code = json.dumps(code, ensure_ascii=False)
                return code
    except BaseException as e:
        print('2', e)

    try:
        # print('3')
        get_user_name = Fire_user.query.filter_by(user_name=login_name).first()
        if get_user_name is not None:
            if get_user_name.user_pwd == login_pwd:
                login_name = get_user_name.login_name
                login_pwd = get_user_name.login_pwd
                login_chinesename = get_user_name.login_chinesename

                code = login_qmf(login_name, login_pwd, login_chinesename)
                session['code'] = '3'
                # code = json.dumps(code, ensure_ascii=False)
                return code
    except BaseException as e:
        print('3', e)
        return '000'

    code['code'] = 4
    code['msg'] = u'密码错误'
    code = json.dumps(code, ensure_ascii=False)
    return code


@app.route('/search', methods=['GET'])
def search():
    # print(session['code'])
    if session['code'] == '2':

        if not request.args['start_time'] and request.args['end_time']:
            print('aa', request.args['start_time'])
            abort(400)
        else:
            start_time = request.args['start_time']
            end_time = request.args['end_time']

        # time_by = request.args['time_by']
        trade_type = request.args['trade_type']
        # order_status = request.args['order_status']
        page = request.args['page']
        switch = request.args['switch']
        # 调用查询函数

        result = speedpos(start_time, end_time, trade_type, page, switch)
        return result
    if session['code'] == '3':
        billDate = request.args['billDate']
        billDate = billDate.split(' ')[0]
        page = request.args['page']
        switch = request.args['switch']
        # print(billDate,page)
        trade_type = request.args['trade_type']
        result = get_data(billDate, page, switch, trade_type)

        return result


# 数据库增 接口
@app.route('/zeng', methods=['POST'])
def insert():
    code = {}
    # 判断增加用户是否存在
    user = Water_user.query.filter_by(login_name=request.form['login_name']).first()
    if user is None:
        login_name = request.form['login_name']
        login_pwd = request.form['login_pwd']
        user_name = request.form['user_name']
        user_pwd = request.form['user_pwd']
        db.session.add(Water_user(login_name, login_pwd, user_name, user_pwd))
        db.session.commit()
        code['code'] = 1
        code['msg'] = u'添加成功'
        return json.dumps(code, ensure_ascii=False)
    else:
        code['code'] = 0
        code['msg'] = u'用户名已存在'
        return json.dumps(code, ensure_ascii=False)


# 数据库 删接口
@app.route('/shan', methods=['GET', 'DELETE'])
def delete():
    code = {}
    if request.method == 'DELETE':
        if not request.form['id']:
            abort(400)
        try:
            id = request.form['id']
            Water_user.query.filter_by(id=id).delete()
            code['code'] = 1
            code['msg'] = u'删除成功'
            return json.dumps(code, ensure_ascii=False)
        except:
            code['code'] = 0
            code['msg'] = u'删除失败'
            return json.dumps(code, ensure_ascii=False)
    if request.method == 'GET':
        try:
            id = request.args['id']
            Water_user.query.filter_by(id=id).delete()
            code['code'] = 1
            code['msg'] = u'删除成功'
            return json.dumps(code, ensure_ascii=False)
        except:
            code['code'] = 0
            code['msg'] = u'删除失败'
            return json.dumps(code, ensure_ascii=False)


# 改api
@app.route('/gai', methods=['POST'])
def gai():
    if not request.form['id']:
        abort(400)
    update_data = {}
    code = {}
    try:
        if request.form['login_name']:
            update_data['login_name'] = request.form['login_name']
    except:
        pass
    try:
        if request.form['login_pwd']:
            update_data['login_pwd'] = request.form['login_pwd']
    except:
        pass
    try:
        if request.form['user_name']:
            update_data['user_name'] = request.form['user_name']
    except:
        pass
    try:
        if request.form['user_pwd']:
            update_data['user_pwd'] = request.form['user_pwd']
    except:
        pass

    user = Water_user.query.filter_by(id=request.form['id']).first()

    if user is None:
        code['code'] = 0
        code['msg'] = u'修改失败'
        return json.dumps(code, ensure_ascii=False)
    else:
        Water_user.query.filter_by(id=request.form['id']).update(update_data)
        db.session.commit()
        code['code'] = 1
        code['msg'] = u'修改成功'
        return json.dumps(code, ensure_ascii=False)


# 查api
@app.route('/cha', methods=['GET'])
def cha():
    item = {}
    items = []
    list_all = Water_user.query.all()
    for each in list_all:
        item = {}
        item['id'] = each.id
        item['login_name'] = each.login_name
        item['login_pwd'] = each.login_pwd
        item['user_name'] = each.user_name
        item['user_pwd'] = each.user_pwd
        # print(item)
        items.append(item)
        # print(items)
    items = json.dumps(items)
    return items


################
# 数据库增 接口
@app.route('/zeng1', methods=['POST'])
def insert1():
    code = {}
    # 判断增加用户是否存在
    user = Fire_user.query.filter_by(login_name=request.form['login_name']).first()
    if user is None:
        login_name = request.form['login_name']
        login_pwd = request.form['login_pwd']
        login_chinesename = request.form['login_chinesename']
        user_name = request.form['user_name']
        user_pwd = request.form['user_pwd']
        wx_session = request.form['wx_session']
        reqmid = 'none'
        db.session.add(Fire_user(login_name, login_pwd, login_chinesename, user_name, user_pwd, wx_session, reqmid))
        db.session.commit()
        code['code'] = 1
        code['msg'] = u'添加成功'
        return json.dumps(code, ensure_ascii=False)
    else:
        code['code'] = 0
        code['msg'] = u'用户名已存在'
        return json.dumps(code, ensure_ascii=False)


# 数据库 删接口
@app.route('/shan1', methods=['GET', 'DELETE'])
def delete1():
    code = {}
    if request.method == 'DELETE':
        if not request.form['id']:
            abort(400)
        try:
            id = request.form['id']
            Fire_user.query.filter_by(id=id).delete()
            code['code'] = 1
            code['msg'] = u'删除成功'
            return json.dumps(code, ensure_ascii=False)
        except:
            code['code'] = 0
            code['msg'] = u'删除失败'
            return json.dumps(code, ensure_ascii=False)
    if request.method == 'GET':
        try:
            id = request.args['id']
            Fire_user.query.filter_by(id=id).delete()
            code['code'] = 1
            code['msg'] = u'删除成功'
            return json.dumps(code, ensure_ascii=False)
        except:
            code['code'] = 0
            code['msg'] = u'删除失败'
            return json.dumps(code, ensure_ascii=False)


# 改api
@app.route('/gai1', methods=['POST'])
def gai1():
    if not request.form['id']:
        abort(400)
    update_data = {}
    code = {}
    try:
        if request.form['login_name']:
            update_data['login_name'] = request.form['login_name']
    except:
        pass
    try:
        if request.form['login_pwd']:
            update_data['login_pwd'] = request.form['login_pwd']
    except:
        pass
    try:
        if request.form['login_chinesename']:
            update_data['login_chinesename'] = request.form['login_chinesename']
    except:
        pass
    try:
        if request.form['user_name']:
            update_data['user_name'] = request.form['user_name']
    except:
        pass
    try:
        if request.form['user_pwd']:
            update_data['user_pwd'] = request.form['user_pwd']
    except:
        pass
    try:
        if request.form['wx_session']:
            update_data['wx_session'] = request.form['wx_session']
    except:
        pass
    user = Fire_user.query.filter_by(id=request.form['id']).first()
    # print(update_data)
    if user is None:
        code['code'] = 0
        code['msg'] = u'修改失败'
        return json.dumps(code, ensure_ascii=False)
    else:
        Fire_user.query.filter_by(id=request.form['id']).update(update_data)
        db.session.commit()
        code['code'] = 1
        code['msg'] = u'修改成功'
        return json.dumps(code, ensure_ascii=False)


# 查api
@app.route('/cha1', methods=['GET'])
def cha1():
    item = {}
    items = []
    list_all = Fire_user.query.all()
    for each in list_all:
        item = {}
        item['id'] = each.id
        item['login_name'] = each.login_name
        item['login_pwd'] = each.login_pwd
        item['login_chinesename'] = each.login_chinesename
        item['user_name'] = each.user_name
        item['user_pwd'] = each.user_pwd
        item['wx_session'] = each.wx_session
        item['reqmid'] = each.reqmid
        # print(item)
        items.append(item)
        # print(items)
    items = json.dumps(items)
    return items


def fflash():
    while 1:
        try:
            url = 'https://qr.chinaums.com/netpay-mer-portal/merchant/queryBills.do'
            user = Fire_user.query.filter_by(login_name='fa4418').first()
            wx_session = user.wx_session
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
            # year = billDate.split('-')[0]
            # month = billDate.split('-')[1]
            # day = billDate.split('-')[2]
            # reqmid = session['reqmid']
            # print('1a1a', reqmid)
            data = {
                'reqMid': '898393058120502',
                'pageSize': '15',
                'curPage': '1',
                'billDate': '2018年03月10日'
            }
            # print(data)

            html = requests.post(url, headers=headers, data=data)

            sleep_time = random.uniform(30, 65)
            # print(sleep_time)
            time.sleep(sleep_time)
        except:
            return '0000'


if __name__ == '__main__':
    t = threading.Thread(target=fflash)
    t.start()

    app.run(
        host='192.168.3.17',
        port=8080,
        debug=True,
        threaded=True)
