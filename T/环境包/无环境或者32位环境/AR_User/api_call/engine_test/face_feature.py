# -*- coding: utf8 -*-
import requests
import json
import time, sys
import hashlib


def do_req(url, method, params):
    mytime = int(time.time())
    sysobj = {'version': '1.0', 'jsonrpc': '2.0', 'key': appKey, 'time': mytime}
    print 'mytime:' + str(mytime)
    reqobj = {'user_id': user_id, 'token': token}
    print(appKey + str(mytime) + str(user_id) + token + secret)
    m0 = hashlib.md5()
    m0.update(appKey + str(mytime) + str(user_id) + token + secret)
    print(m0.hexdigest())
    sysobj['sign'] = m0.hexdigest()
    print(reqobj)
    obj = {
        'id': 1,
        'method': method,
        'request': reqobj,
        'system': sysobj,
        'params': params
    }
    data = json.dumps(obj)
    r = requests.post(url, data=data)
    jdata = json.loads(r.content)
    print(jdata)
    if jdata['result']['code'] == 0:
        return jdata['result']['data']
    else:
        print('request error', jdata['result']['code'], jdata['result']['message'])
        sys.exit()

if __name__ == '__main__':
    token = ''
    user_id = ''
    appKey = 'bc348c97cb509adf8c2d714e0c0c4ff5'
    secret = '8e04182092c72f571c6cc6fafc85d635'

    hm_url = 'http://smart.99.com/v2/homer'
    ac_url = 'http://smart.99.com/v1/account'

    user_name = '13559209035'  # username
    m0 = hashlib.md5()
    m0.update('11514844')  # password
    password = m0.hexdigest()
    # login request, to get token and user_id
    login = do_req(ac_url, 'login', {'user_name': user_name, 'password': password})
    user_id = login['user_id']
    token = login['token']
    # person_feature request
    time = int(time.time())
    sysobj = {'version': '1.0', 'jsonrpc': '2.0', 'key': appKey, 'time': time}
    reqobj = {'user_id': user_id, 'token': token}
    params = {'img_url': 'http://192.168.239.119:807/000011.jpg'}
    m0 = hashlib.md5()
    m0.update(appKey + str(time) + str(user_id) + token + secret)
    sysobj['sign'] = m0.hexdigest()
    obj = {
        'id': 1,
        'method': 'face/person_feature',
        'request': reqobj,
        'system': sysobj,
        'params': params
    }
    data = json.dumps(obj)
    r = requests.post(hm_url, data=data)
    print r.content