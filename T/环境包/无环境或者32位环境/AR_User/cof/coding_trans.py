# coding=utf-8
__author__ = 'Administrator'

import types
import json


class CodingTransform(object):
    def __init__(self):
        pass

    def dict_by_utf(self, data_dec):
        """
        data_dec 是字典类型的
        """
        key = data_dec.keys()
        for i in range(len(data_dec)):
            b = data_dec[key[i]]
            if isinstance(b, str):
                try:        # 检查是否可以被转换为dict类型
                    b = json.loads(b)
                    self.dict_by_utf(b)
                except Exception as e:
                    continue
            elif isinstance(b, dict):   # 数据本身就是dict类型的
                self.dict_by_utf(b)
            if isinstance(b, unicode):
                b = b.encode('utf-8')
                data_dec[key[i]] = b

        return data_dec

if __name__ == "__main__":
    data_dec = {
        u'user_exinfo': u'{"work_info": "123456789"}',  # json
        u'expires_at': '2015-03-27T10:49:08.684+0800',  # string
        u'user_id': 2006121482,                         # int
        u'success': True,                               # boole
    }

    data_dec_1 = {
        'data': '{\n\t"fail_user":{\n\t\t"900109":"\xe7\x94\xa8\xe6\x88\xb7\xe5\xb7\xa5\xe5\x8f\xb7\xe5\xb7\xb2\xe5\xad\x98\xe5\x9c\xa8"\n\t},\n\t"success_user":[]\n}'
    }

    #o = CodingTransform()
    #data = o.dict_by_utf(data_dec_1)
    data = data_dec_1
    data = json.dumps(data, ensure_ascii=False)
    print data
