# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetRandomEventTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run GetRandomEvent test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'GetRandomEvent test complete.....close socket'
    
    def test_get_random_event_sucess(self):
        """
        获取随机事件成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        latitude = 26.092
        longitude = 119.314
        
        res = self.ar_con.get_random_event(latitude, longitude)
        res_data = json.loads(res)
        
        assert_that(res_data, has_key("events"), "no events response...")
        assert_that(res_data, has_key("valid_time"), "no valid_time response...")
        
        for events in res_data["events"]:
            assert_that(events, has_key("event_id"), "no event_id response...")
            assert_that(events, has_key("latitude"), "no latitude response...")
            assert_that(events, has_key("longitude"), "no latitude response...")
            assert_that(events, has_key("event_type"), "no event_type response...")
            assert_that(events, has_key("status"), "no status response...")

if __name__ == "__main__":
    unittest.main()
