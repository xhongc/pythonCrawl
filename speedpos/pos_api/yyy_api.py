import requests
import json
import time
from pprint import pprint
from flask import Flask
from flask import request, session
from flask import jsonify, abort
from flask_cors import *

app = Flask(__name__)
# flask 解决跨域问题
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'xhc195023123sda'


def get_order():
    url = 'http://fzms.498.net/member.php/Flows/flowsList.html'
    # data = {
    #     'method': 'getData',
    #     'day': '7'
    # }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'fzms.498.net',
        'Origin': 'http://fzms.498.net',
        'Referer': 'http://fzms.498.net/member.php/User/login.html',
        'cookie': 'PHPSESSID=i4t84eqfcq4rti22am27cetg02; __51cke__=; a_m_info=%7B%22name%22%3A%22%5Cu53ef%5Cu5fc3%5Cu660e%5Cu5546%5Cu8d38%5Cu90e8%22%2C%22ls_date%22%3A%222018-06-06+17%3A40%3A02%22%2C%22business_no%22%3A%221001465123%22%2C%22parent_type%22%3A%221%22%2C%22co_name_dis%22%3A%22%5Cu798f%5Cu5efa%5Cu7f51%5Cu878d%5Cu4fe1%5Cu606f%5Cu79d1%5Cu6280%5Cu6709%5Cu9650%5Cu516c%5Cu53f8%22%2C%22contact_man%22%3A%22%5Cu90d1%5Cu5b88%5Cu745e%22%2C%22contact_man_tel%22%3A%2215880108018%22%7D; SERVERID=b360c3ff3cbf93b705b3356d46a1190b|1528278718|1528278294; __tins__19094318=%7B%22sid%22%3A%201528278303568%2C%20%22vd%22%3A%208%2C%20%22expires%22%3A%201528280528305%7D; __51laig__=8'
    }
    html = requests.post(url, headers=headers)
    html = json.loads(html.text, encoding='utf-8')
    content = html['data']
    # pprint(content)
    res = []
    result = {

    }
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
        res.append(item)

    result['code'] = '000000'
    result['data'] =res

    return json.dumps(result, ensure_ascii=False)


@app.route('/order', methods=['GET', 'POST'])
def order_serach():
    try:
        data = get_order()


    except:
        data = {'code':'111111'}
    return data


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=False,
    )
