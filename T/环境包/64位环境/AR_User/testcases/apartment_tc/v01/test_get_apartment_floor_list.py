# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand


class GetApartmentFloorListTest(unittest.TestCase):
    """
    获取公寓所有楼层信息
    """

    def setUp(self):
        print 'start run GetApartmentFloorList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetApartmentFloorList test complete.....close socket'

    def test_get_apartment_floor_list_success(self):
        """
        获取公寓所有楼层信息成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.get_all_apartment()
        res_data = json.loads(res)
        apartment_code = res_data[0]["apartment_code"]
        self.ar_con.apply_apartment(apartment_code)  # 有用户入住

        res = self.ar_con.get_apartment_floor_list(apartment_code)
        res_data = json.loads(res)

        for floor in res_data:
            assert_that(floor, has_key("user_id"), "no user_id response...")
            assert_that(floor, has_key("sex"), "no sex response...")
            assert_that(floor, has_key("apartment_code"), "no apartment_code response...")
            assert_that(floor["apartment_code"], equal_to(apartment_code), "apartment_code not match...")
            assert_that(floor, has_key("floor"), "no floor response...")
            assert_that(floor, has_key("floor_name"), "no floor_name response...")
            assert_that(floor, has_key("nick_name"), "no nick_name response...")
            assert_that(floor, has_key("icon_code"), "no icon_code response...")

    def test_get_apartment_floor_list_notexist(self):
        """
        获取公寓所有楼层信息失败，不存在的公寓\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        apartment_code = CoRand.get_rand_int()

        res = self.ar_con.get_apartment_floor_list(apartment_code)
        res_data = json.loads(res)

        assert res_data == []

if __name__ == "__main__":
    unittest.main()
