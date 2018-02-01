# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *


class PlantSeedTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run PlantSeed test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'PlantSeed test complete.....close socket'
    
    def test_plant_seed_success(self):
        """
        种植花朵成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        
        res = self.ar_con.get_seeds()
        res_data = json.loads(res)
        
        seed = res_data[0]["seed"]
        res = self.ar_con.plant_seed(2, seed)
        res_data = json.loads(res)  
        
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    unittest.main()
