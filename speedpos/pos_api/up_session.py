import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import time
import random

app = Flask(__name__)
databaseurl = 'mysql://root:xhongc@localhost/info'
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#创建数据库
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

    def __init__(self, login_name, login_pwd,login_chinesename,user_name,user_pwd,wx_session,reqmid):
        self.login_name = login_name
        self.login_pwd = login_pwd
        self.login_chinesename = login_chinesename
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.wx_session = wx_session
        self.reqmid = reqmid
db.create_all()

def fflash():
    while 1:
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
            'Cookie': 'SESSION=%s; route=ff7ccc9ac07719e8e706ebafb1588dfa; JSESSIONID=0doJ-707FwJx2fGA7Fbf8Fse3cQTQYth1_NpUDuVlw_teeQf_cnj!-1058374088' %(wx_session)

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
        #print(html.text)
        sleep_time = random.uniform(55,65)
        time.sleep(sleep_time)

fflash()