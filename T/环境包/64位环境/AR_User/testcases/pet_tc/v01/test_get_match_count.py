# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand


class GetMatchCountTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run GetMatchCount test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'GetMatchCount test complete.....close socket'
    
    def test_get_match_count_success(self):
        """
        获取剩余的捕获次数成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        
        res = self.ar_con.get_match_count()
        res_data = json.loads(res)
        
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")

    def test_get_match_count_after_capture(self):
        """
        捕获宠物后次数减一\   【暂时去除次数限制，后期待更新】
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        res = self.ar_con.get_match_count()
        res_data = json.loads(res)
        before_count = res_data["scan_advance"]
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        self.ar_con.capture_pet(res_data["item_id"])
        res = self.ar_con.get_match_count()
        res_data = json.loads(res)
        after_count = res_data["scan_advance"]

        assert_that(before_count - after_count, equal_to(1), "get_match_count result error...")

if __name__ == "__main__":
    unittest.main()
