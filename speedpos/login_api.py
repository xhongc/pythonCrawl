import requests
from scrapy.selector import Selector
import pymysql
import json
import time
from flask import Flask
from flask import request,session
from flask import jsonify,abort
from flask_cors import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

databaseurl = 'mysql://root:xhongc@localhost/info'
app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Water_user(db.Model):
    __tablename__ = 'water_user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login_name = db.Column(db.String(255), nullable=True)
    login_pwd = db.Column(db.String(255), nullable=True)
    cookies = db.Column(db.TEXT(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=True)
    user_pwd = db.Column(db.String(255), nullable=True)

    def __init__(self, login_name, login_pwd, cookies,user_name,user_pwd):
        self.login_name = login_name
        self.login_pwd = login_pwd
        self.cookies = cookies
        self.user_name = user_name
        self.user_pwd = user_pwd
db.create_all()

def speedpos(start_time,end_time,time_by='create_time',trade_type=None,order_status=None):

    post_data = {
        '_loadpage':'1',
        'page':'1',
        'start_time':start_time,
        'end_time':end_time,
        'time_by':time_by,
        'trade_type':trade_type,
        'order_status':order_status,
    }
    try:
        upSession = session['upSession']
        res = upSession.post('https://mch.speedpos.cn/orders/lists',headers=headers,data=post_data)
        selector = Selector(res)
        res_list = selector.xpath('//tr[@class="selectline"]')
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
        #print(post_data)
        return result
    except:
        result = '大侠请重新来过'
        return result


def login(login_name,login_pwd):
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
    Water_user.query.filter_by(login_name=login_name).update({'cookies': cookies})
    #session['upSession'] = upSession

@app.route('/login', methods=['POST'])
def login_api():
    code = {}
    login_name = request.form.get('login_name', 'none value')
    login_pwd = request.form.get('login_pwd','none value')
    try:
        get_login_name = Water_user.query.filter_by(login_name=login_name).first()
        if get_login_name.login_pwd == login_pwd:
            login(login_name,login_pwd)
            code['code'] = 1
            code['msg'] = u'管理者登陆'
            code = json.dumps(code,ensure_ascii=False)
            return code
    except AttributeError as e:
        get_user_name = Water_user.query.filter_by(user_name=login_name).first()
        if get_user_name is None:
            code['code'] = 3
            code['msg'] = u'账号或密码错误'
            code = json.dumps(code,ensure_ascii=False)
            return code
        else:
            if get_user_name.user_pwd == login_pwd:
                login_name = get_user_name.login_name
                login_pwd = get_user_name.login_pwd
                login(login_name,login_pwd)
                code['code'] = 2
                code['msg'] = u'客户登陆'
                code = json.dumps(code,ensure_ascii=False)
                return code
            else:
                code['code'] = 3
                code['msg'] = u'账号或密码错误'
                code = json.dumps(code,ensure_ascii=False)
                return code


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
    app.run(
        host='192.168.3.17',
        port=8080,
        debug=True)
