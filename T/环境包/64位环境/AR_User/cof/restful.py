# coding=utf-8
__author__ = 'Administrator'

"""
restful规范接口的返回值处理方法
"""
import sys
sys.path.insert(0, '..')
import json
from hamcrest import *      # 断言库
from AR_User.cof.coding_trans import CodingTransform


class Restful(object):
    def __init__(self):
        """

        """
        pass

    def parse_response(self, response, code, message):
        """
        解析请求接口返回的数据。
        若与期望相符，则返回data_dec；否则直接就断言失败，跳出case。
        response: 返回的数据;
        code：[整型]该次请求所期望返回的code;
        message：错误时需要的指明的信息
        ret：data_dec，转换为json格式之后的data字段
        """
        data = response['data']
        data_dec = dict()
        if response['code'] != code:    # 状态码错误
            if len(data) == 0:            # 判断data有没有内容
                error = message + "，\n状态码：" + str(response['code']) + "，\n请求为：" + str(response['request'])
                assert_that(response['code'], equal_to(code), error)
            else:                       # 判断状态码
                try:
                    data_dec = json.loads(data)
                except Exception as e:
                    error = message + "，\n状态码：" + str(response['code']) + "，数据不是json格式的，\n请求为：" + str(response['request'])
                    assert_that(response['code'], equal_to(code), error)
                # 如果返回的data里面没有message字段，直接输出data
                if 'message' in data_dec:
                    error = ""
                    if data_dec['message']:
                        error = message + "，\n状态码：" + str(response['code']) + "，\n错误信息：" + data_dec['message'].encode('utf-8')+"\n详细信息:"+str(data_dec['detail'])
                    else:
                        error = message + "，\n状态码：" + str(response['code']) + "，\n错误信息为空，\n请求为：" + str(response['request'])
                    print response['code'],code,error
                    assert_that(response['code'], equal_to(code), error)
                else:
                    error = message + ",\n返回的数据是： " +  str(json.dumps(data_dec, ensure_ascii=False))
                    print response['code'],code,error
                    assert_that(response['code'], equal_to(code), error)
        else:                           # 状态码正确
            if len(data) == 0:          # 判断data有没有内容
                #data_dec = CodingTransform().dict_by_utf(data_dec)
                return data_dec
            else:
                try:
                    data_dec = json.loads(data)
                except Exception as e:
                    error = message + "，\n状态码：" + str(response['code']) + "，数据不是json格式的，\n响应数据为：" + \
                            str(json.dumps(data_dec, ensure_ascii=False))
                    assert_that(error, equal_to(""), error)
                return data_dec

    def parse_error_info(self, data_dec, error_code, error_message=""):
        """
        使用于restful逆向用例；
        当状态码符合期望时，再进一步判断返回值是否为指定的格式，如下：
        {
            "code":"UC/ORG_NOT_EXIST",               // 表示错误信息
            "message":"{error message}",             // 错误信息的文字说明
            "request_id":"1234567",                  // 请求id
            "host_id":"{server identity}",           // 主机id
            "server_time":"2014-01-01T12:00:00Z"     // 服务器时间
        }
        """
        assert_that(data_dec, has_key('code'))
        assert_that(
            data_dec['code'].encode('utf-8'),
            equal_to(error_code),
            "错误码与期望不符，期望值为：" + error_code + "，实际值为：" + data_dec['code'].encode('utf-8'))

        assert_that(data_dec, has_key('message'))
        if error_message != "":
            assert_that(
                data_dec['message'].encode('utf-8'),
                equal_to(error_message),
                "错误信息与期望不符，期望值为：" + error_message + "，实际值为：" + data_dec['message'].encode('utf-8')
            )

        if "request_id" not in data_dec:
            print "there's no request_id in data: " + str(data_dec)

        assert_that(data_dec, has_key('host_id'))

        assert_that(data_dec, has_key('server_time'))


def main():
    pass