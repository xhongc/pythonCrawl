# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class HarvestFlowerTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run HarvestFlower test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'HarvestFlower test complete.....close socket'
    
    def test_harvest_flower_success(self):
        """
        收花成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        soil_id = 1
        res = self.ar_con.get_soils()
        res_data = json.loads(res)
        for soil in res_data:
            if soil["seed"] > 0:
                soil_id = soil["soil_id"]

        res = self.ar_con.harvest_flower(soil_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("items"), "no items response...")
        assert_that(res_data, has_key("winning"), "no winning response...")

if __name__ == "__main__":
    unittest.main()
