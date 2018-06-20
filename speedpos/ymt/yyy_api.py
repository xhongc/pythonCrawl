import requests
import json
import time
from pprint import pprint
from flask import Flask
from flask import request, session
from flask import jsonify, abort
from flask_restplus import Resource, Api, fields
from flask_cors import *
import threading
from tools import get_order, get_cookies
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
databaseurl = 'mysql://root:xhongc@localhost/ymt'

# flask 解决跨域问题
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'xhc195023123sda'
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 数据修改自动提交
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

api = Api(app, prefix='/api', title='一码通', description='Powered By Superman')
search_api = api.namespace('search', description='查询')
login_api = api.namespace('login', description='登录')


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    login_name = db.Column(db.String(255), nullable=True)
    login_pwd = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=True)
    user_pwd = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.String(255), nullable=True, default=0)

    def __init__(self, login_name, login_pwd, user_name, user_pwd, is_admin):
        self.login_name = login_name
        self.login_pwd = login_pwd
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.is_admin = is_admin


db.create_all()


@search_api.route('/')
class Search_order(Resource):
    def get(self):
        try:
            if not session['cookies']:
                cookies = get_cookies()
                session['cookies'] = cookies
            cookies = session['cookies']
            data = get_order(cookies)
        except KeyError:
            cookies = get_cookies()
            session['cookies'] = cookies
            try:
                data = get_order(cookies)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·'}
                # data = json.dumps(data, ensure_ascii=False)
            except KeyError:
                data = {'code': '2', 'msg': u'出现未知问题'}
                data = json.dumps(data, ensure_ascii=False)
        except TypeError:
            data = {'code': '111111', 'msg': u'无数据·'}
            # data = json.dumps(data, ensure_ascii=False)
        return data


login_model = api.model('login_model', {
    'username': fields.String,
    'passwd': fields.String
})


@login_api.route('/')
class Login(Resource):
    @login_api.expect(login_model)
    def post(self):
        try:
            username = request.json.get('username', None)
            passwd = request.json.get('passwd', None)
        except:
            username = request.values.get('username', None)
            passwd = request.values.get('passwd', None)
        print(username, passwd)
        user = Users.query.filter_by(user_name=username).first()
        if user and user.user_pwd == passwd:
            session['login'] = True
            session['username'] = username
            if user.is_admin == '1':
                return {"code": '101', "msg": u'管理登陆成功'}
            elif user.is_admin == '0':
                return {"code": '102', "msg": u'登陆成功'}

        return {"code": '000', "msg": u'登陆不成功', "isadmin": '0'}


class Mima(Resource):
    def post(self):
        if session['login']:
            username = session['username']
            user = Users.query.filter_by('username').first()
            passwd = user.user_pwd


if __name__ == '__main__':
    # t = threading.Thread(target=flash)
    # t.start()
    # app.run(
    #     host='127.0.0.1',
    #     port=8080,
    #     debug=True,
    # )
    get_order()
