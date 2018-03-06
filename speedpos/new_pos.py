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
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)

#创建数据库
class Water_user(db.Model):
    __tablename__ = 'water_user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login_name = db.Column(db.String(255), nullable=True)
    login_pwd = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=True)
    user_pwd = db.Column(db.String(255), nullable=True)

    def __init__(self, login_name, login_pwd,user_name,user_pwd):
        self.login_name = login_name
        self.login_pwd = login_pwd
        self.user_name = user_name
        self.user_pwd = user_pwd
db.create_all()


def get_name(order_num):

    url = 'https://mch.speedpos.cn/orders/info?_loadpage=1'
    dataa = {'order_no': order_num}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
    cookie = session['upSession']

    res = requests.post(url, headers=headers, data=dataa,cookies=cookie)
    # print(res.text)
    selector = Selector(res)
    title = selector.xpath('//div[@class="margin_r20 fl"]/input/@value').extract()
    name1 = title[4]
    name2 = title[7]
    #print(name1,name2)
    if name1 in name2:
        #print(name1, name2)
        return '无'
    else:
        return name1



# 调用speedpos。con 获取数据
def speedpos(start_time,end_time,trade_type,page='1',switch='false'):
    #print('switch:',switch)
    code ={}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400',
        'Referer': 'https://mch.speedpos.cn/index',
        'X-Requested-With': 'XMLHttpRequest'
    }
    post_data = {
        '_loadpage':'1',
        'page':page,
        'start_time':start_time,
        'end_time':end_time,
        'time_by':'pay_time',
        'trade_type':trade_type,
        'order_status':'2',
    }
    # 将cookie 存在session中全局调用
    cookie = session['upSession']

    #print('new',cookie)
    #upSession = requests.Session()
    # 获取数据
    try:
        res = requests.post('https://mch.speedpos.cn/orders/lists',headers=headers,data=post_data,cookies=cookie)
        # print(res.text)
        selector = Selector(res)
        res_list = selector.xpath('//tr[@class="selectline"]')
        items = []
        for each in res_list:
            item = {}
            each = each.xpath('./td/text()').extract()
            item['pay_time'] = each[0]
            item['order_time'] = each[1]
            item['order_num'] = each[3]
            item['pay_mode'] = each[5]
            item['pay_status'] = each[6]
            item['pay_money'] = each[7]
            if switch == 'true':
                # print('switch is true')
                item['store_name'] = get_name(item['order_num'])

            #print(item)
            items.append(item)
            result = json.dumps(items,indent=4,ensure_ascii=False)
        #print(items)
        return result
    except:
        code['code'] = 0
        code['msg'] = u'无数据返回'
        code = json.dumps(code, ensure_ascii=False)
        return code

# 登陆POST
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
    # Water_user.query.filter_by(login_name=login_name).update({'cookies': cookies})
    session['upSession'] = cookies
    # print(cookies)

# 登陆接口
@app.route('/login', methods=['POST'])
def login_api():
    code = {}
    login_name = request.form.get('login_name', 'none value')
    login_pwd = request.form.get('login_pwd','none value')

    # 验证密码
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

# 查询接口
@app.route('/search', methods=['GET'])
def search():
    if not request.args['start_time'] and request.args['end_time']:
        print('aa',request.args['start_time'])
        abort(400)
    else:
        start_time = request.args['start_time']
        end_time = request.args['end_time']

    # time_by = request.args['time_by']
    trade_type = request.args['trade_type']
    # order_status = request.args['order_status']
    page = request.args['page']
    switch = request.args['switch']
    #调用查询函数
    result = speedpos(start_time,end_time,trade_type,page,switch)

    return result

# 数据库增 接口
@app.route('/zeng', methods=['POST'])
def insert():
    code = {}
    #判断增加用户是否存在
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


#数据库 删接口
@app.route('/shan', methods=['GET','DELETE'])
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
            return json.dumps(code,ensure_ascii=False)
        except:
            code['code'] = 0
            code['msg'] = u'删除失败'
            return json.dumps(code,ensure_ascii=False)
    if request.method == 'GET':
        try:
            id = request.args['id']
            Water_user.query.filter_by(id=id).delete()
            code['code'] = 1
            code['msg'] = u'删除成功'
            return json.dumps(code,ensure_ascii=False)
        except:
            code['code'] = 0
            code['msg'] = u'删除失败'
            return json.dumps(code,ensure_ascii=False)

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
        code['code'] = 1
        code['msg'] = u'修改成功'
        return json.dumps(code, ensure_ascii=False)

# 查api
@app.route('/cha', methods=['GET'])
def cha():
    item ={}
    items=[]
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
if __name__ == '__main__':
    app.run(
        host='192.168.3.17',
        port=8080,
        debug=True)
