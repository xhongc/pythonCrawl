# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetAllApartmentTest(unittest.TestCase):
    """
    获取所有公寓列表
    """

    def setUp(self):
        print 'start run GetAllApartment test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetAllApartment test complete.....close socket'

    def test_get_all_apartment_success(self):
        """
        获取所有公寓列表成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")

        res = self.ar_con.get_all_apartment()
        res_data = json.loads(res)

        for apartment in res_data:
            assert_that(apartment, has_key("apartment_code"), "no apartment_code response...")
            assert_that(apartment, has_key("latitude"), "no latitude response...")
            assert_that(apartment, has_key("longitude"), "no longitude response...")
            assert_that(apartment, has_key("apartment_name"), "no apartment_name response...")
            assert_that(apartment, has_key("img"), "no img response...")
            assert_that(apartment, has_key("total_floor"), "no total_floor response...")
            assert_that(apartment, has_key("is_full"), "no total_floor response...")
            assert_that(apartment, has_key("current_num"), "no total_floor response...")

if __name__ == "__main__":
    unittest.main()
