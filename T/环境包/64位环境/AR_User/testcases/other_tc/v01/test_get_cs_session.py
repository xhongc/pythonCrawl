# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetCSSessionTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run GetCSSession test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'GetCSSession test complete.....close socket'
    
    def test_get_cs_session_success(self):
        """
        获取CS的Session成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")

        res = self.ar_con.get_cs_session()
        res_data = json.loads(res)

        assert_that(res_data, has_key("session"), "no session response...")
        assert_that(res_data, has_key("expire_at"), "no expire_at response...")


if __name__ == "__main__":
    unittest.main()
