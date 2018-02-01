# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetSupplyTest(unittest.TestCase):
    """
    获取神仙居
    """

    def setUp(self):
        print 'start run GetSupply test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetSupply test complete.....close socket'

    def test_get_supply_success(self):
        """
        获取神仙居成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        latitude = 26.092
        longitude = 119.314
        res = self.ar_con.get_supply(latitude, longitude)
        res_data = json.loads(res)

        for supply in res_data:
            assert_that(supply, has_key("id"), "no id response...")
            assert_that(supply, has_key("latitude"), "no latitude response...")
            assert_that(supply, has_key("longitude"), "no longitude response...")
            assert_that(supply, has_key("name"), "no name response...")
            assert_that(supply, has_key("image"), "no image response...")
            assert_that(supply, has_key("cd_time"), "no cd_time response...")

    def test_get_supply_error(self):
        """
        获取神仙居失败，错误的定位数据\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        latitude = 120.092
        longitude = 220.314
        res = self.ar_con.get_supply(latitude, longitude)
        res_data = json.loads(res)

        assert res_data == []


if __name__ == "__main__":
    unittest.main()
