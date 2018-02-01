# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *
from cof.rand import CoRand


class MatchFlowerTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run MatchFlower test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'MatchFlower test complete.....close socket'
    
    def test_match_flower_success(self):
        """
        扫描花朵匹配成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        url = "http://ndreadonly.oss-cn-hangzhou.aliyuncs.com/flower_image/large/t00003213/4577951499733050817.jpg"
        res = self.ar_con.match_flower(url)
        res_data = json.loads(res)
 
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("quality"), "no quality response...")
        assert_that(res_data, has_key("flowerelf"), "no flowerelf response...")
        assert_that(res_data, has_key("seed"), "no seed response...")
     
    def test_repeat_match_flower(self):
        """
        重复匹配花朵\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        url = "http://ndreadonly.oss-cn-hangzhou.aliyuncs.com/flower_image/large/t00003213/4577951499733050817.jpg"
        self.ar_con.match_flower(url)
        res = self.ar_con.match_flower(url)
        res_data = json.loads(res)
  
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_FLOWER_HAS_SCANED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_FLOWER_HAS_SCANED["err_msg"]), "response msg mismatching...")
        
    def test_match_flower_faild(self):
        """
        匹配花朵失败\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        user_id = 100861
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        url = "http://ndreadonly.oss-cn-hangzhou.aliyuncs.com/flower_image/test.jpg"
        res = self.ar_con.match_flower(url)
        res_data = json.loads(res)
 
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_FLOWER_INVALID_RESULT["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_FLOWER_INVALID_RESULT["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    unittest.main()
