# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetSeedsTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run GetSeeds test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'GetSeeds test complete.....close socket'
    
    def test_get_seeds_success(self):
        """
        获取种子信息成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        res = self.ar_con.get_seeds()
        res_data = json.loads(res)
        for seed in res_data:
            assert_that(seed, has_key("seed"), "no seed response...")
            assert_that(seed, has_key("count"), "no count response...")

if __name__ == "__main__":
    unittest.main()
