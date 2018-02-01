# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetSoilsTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run GetSoils test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'GetSoils test complete.....close socket'
    
    def test_get_soils_success(self):
        """
        获取地块信息成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        res = self.ar_con.get_soils()
        res_data = json.loads(res)
        
        for soil in res_data:
            assert_that(soil, has_key("soil_id"), "no soil_id response...")
            assert_that(soil, has_key("time"), "no time response...")
            assert_that(soil, has_key("seed"), "no seed response...")

if __name__ == "__main__":
    unittest.main()
