from flask import Flask
from flask import request
from flask import jsonify,abort
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_cors import *

app = Flask(__name__)

CORS(app,supports_credentials=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

@app.route('/all',methods=['GET'])
@app.route('/all',methods=['GET'])
def data():
    data =[]
    beijing = {"turnNum":"660756","openNum":"07,06,04,01,08,02,10,09,03,05","openTime":"2018-01-09 17:27:34","gameId":50,"gamename":'北京赛车PK10'}
    ssc = {"turnNum":"20180109073","openNum":"0,5,3,3,4","openTime":"2018-01-09 18:10:43","gameId":1,"gamename":'重庆时时彩'}
    liuhecai = {"turnNum":"2018002","openNum":"01,36,31,49,12,21,23","openTime":"2018-01-06 21:34:41","gameId":70,"gamename":'香港六合彩'}
    guangxi115 = {"turnNum":"2018010958","openNum":"08,05,01,07,02","openTime":"2018-01-09 18:32:06","gameId":161,"gamename":'广东11选5'}
    xinjiangssc = {"turnNum":"20180109051","openNum":"2,4,9,9,6","openTime":"2018-01-09 18:30:45","gameId":168,'gamename':'新疆时时彩'}
    a = {"turnNum": "2018010958", "openNum": "08,05,01,07,02", "openTime": "2018-01-09 18:32:06","gameId": 161, "gamename": '广西11选5'}
    b = {"turnNum": "2018010958", "openNum": "08,05,01,07,02", "openTime": "2018-01-09 18:32:06","gameId": 161, "gamename": '江西11选5'}
    c = {"turnNum": "2018010958", "openNum": "08,05,01,07,02", "openTime": "2018-01-09 18:32:06","gameId": 161, "gamename": '上海11选5'}
    d = {"turnNum": "2018010958", "openNum": "08,05,01,07,02", "openTime": "2018-01-09 18:32:06","gameId": 161, "gamename": '山东11选5'}

    anhui3 = {"turnNum":"20180109060","openNum":"2,5,6","openTime":"2018-01-09 18:41:27","gameId":163,"gamename":'安徽快3'}
    guangxi3 = {"turnNum":"20180109060","openNum":"2,5,6","openTime":"2018-01-09 18:41:27","gameId":163,"gamename":'广西快3'}
    jiangsu3 = {"turnNum":"20180109060","openNum":"2,5,6","openTime":"2018-01-09 18:41:27","gameId":163,"gamename":'江苏快3'}

    data.append(beijing)
    data.append(ssc)
    data.append(liuhecai)
    data.append(guangxi115)
    data.append(xinjiangssc)
    data.append(a)
    data.append(b)
    data.append(c)
    data.append(d)
    data.append(anhui3)
    data.append(guangxi3)
    data.append(jiangsu3)
    data = json.dumps(data,ensure_ascii=False,indent=4)
    return data

if __name__ == '__main__':
    app.run(
        host='192.168.0.104',
        port=8080,
        debug=True)