from flask import Flask
from flask import request
from flask import jsonify,abort
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_cors import *


databaseurl = 'mysql://root:xhongc@localhost/info'
app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class DateEncoder(json.JSONEncoder ):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)

# 创建表格
class Beijingpk10(db.Model):
    __tablename__ = 'beijingpk10'
    turnNum = db.Column(db.Integer, primary_key=True, nullable=False)
    openNum = db.Column(db.String(60), nullable=False)
    gameId = db.Column(db.Integer, nullable=False)
    openTime = db.Column(db.String(20), nullable=False)
    def __init__(self, turnNum, openNum, gameId,openTime):
        self.turnNum = turnNum
        self.openNum = openNum
        self.gameId = gameId
        self.openTime = openTime

    # def __repr__(self):
    #     return '%s,%s' % (self.turnNum, self.openNum)

#
db.create_all()


# @app.route('/', methods=['POST'])
# def hello():
#     if not request.json:
#         return "failed!", 400
#     student = {
#         'id': request.json['id'],
#         'name': request.json['name'],
#         'age': request.json['age']
#     }
#     # 初始化student对象
#     stu = mytable(int(student['id']), student['name'], int(student['age']))
#     # 将新增项目插入数据库
#     db.session.add(stu)
#     # 提交修改
#     db.session.commit()
#     return "Hello World!"


@app.route('/beijingpk10', methods=['GET'])
def get_one():
    if not request.args['turnNum']:
        abort(400)
    get_id = request.args['turnNum']
    # print(get_id)
    # 得到表中所有的数据
    ids = Beijingpk10.query.all()
    # print(ids)
    # 使用filter找到指定项目
    get = Beijingpk10.query.filter_by(turnNum=get_id).first()
    #print(get)
    # 获取表成员属性
    #ret = 'turnNum=%d,openNum=%s,gameId=%d,openTime=%s' % (get.turnNum, get.openNum, get.gameId,get.openTime)
    # print(ret)
    item ={}
    item['turnNum'] = get.turnNum
    item['openNum'] = get.openNum
    item['gameId'] = get.gameId
    item['openTime'] = get.openTime
    item['gamename'] = u'北京赛车PK10'
    item = json.dumps(item,cls =DateEncoder,ensure_ascii=False)
    return item

@app.route('/beijingpk10/all',methods=['GET'])
def get_double():

    get = Beijingpk10.query.order_by('openTime desc').limit(100).all()


    items =[]

    for each in get:
        # print(each.turnNum)
        item = {}
        item['turnNum'] = each.turnNum
        item['openNum'] = each.openNum
        item['gameId'] = each.gameId
        item['openTime'] = each.openTime
        item['gamename'] = '北京赛车PK10'
        # print(item)
        items.append(item)

    items = json.dumps(items, cls=DateEncoder, ensure_ascii=False,indent=4)

    return items




app.run(
    host='192.168.0.112',
    port= 8080,
    debug=True)