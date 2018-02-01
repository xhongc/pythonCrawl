# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand


class GetApartmentListTest(unittest.TestCase):
    """
    获取玩家所入住的公寓列表
    """

    def setUp(self):
        print 'start run GetApartmentList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetApartmentList test complete.....close socket'

    def test_get_apartment_list_success(self):
        """
        获取所有公寓列表成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        apartment_code = 1
        res = self.ar_con.get_all_apartment()
        res_data = json.loads(res)
        for apartment in res_data:
            if apartment["is_full"] == 1:
                apartment_code = apartment["apartment_code"]
                break
        res = self.ar_con.apply_apartment(apartment_code)
        res_data = json.loads(res)
        floor = res_data["floor"]

        res = self.ar_con.get_apartment_list(user_id)
        res_data = json.loads(res)

        for apartment in res_data:
            assert_that(apartment, has_key("user_id"), "no user_id response...")
            assert_that(apartment["user_id"], equal_to(user_id), "response user_id mismatching...")
            assert_that(apartment, has_key("apartment_code"), "no apartment_code response...")
            assert_that(apartment["apartment_code"], equal_to(apartment_code), "response apartment_code mismatching...")
            assert_that(apartment, has_key("floor"), "no floor response...")
            assert_that(apartment["floor"], equal_to(floor), "response floor mismatching...")

    def test_get_apartment_list_no_join_apartment(self):
        """
        获取所有公寓列表,未入住任何公寓\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]

        res = self.ar_con.get_apartment_list(user_id)
        res_data = json.loads(res)

        assert res_data == []

if __name__ == "__main__":
    unittest.main()
