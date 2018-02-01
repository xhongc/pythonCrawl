# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *
from cof.rand import CoRand


class ApplyApartmentTest(unittest.TestCase):
    """
    玩家申请入住公寓
    """

    def setUp(self):
        print 'start run ApplyApartment test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'ApplyApartment test complete.....close socket'

    def test_apply_apartment_success(self):
        """
        玩家申请入住公寓成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        apartment_code = 1
        res = self.ar_con.get_all_apartment()
        res_data = json.loads(res)
        for apartment in res_data:
            if apartment["is_full"] == 1:
                apartment_code = apartment["apartment_code"]
                break

        res = self.ar_con.apply_apartment(apartment_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("floor")), "no floor response..."

    def test_apply_apartment_repeat(self):
        """
        玩家申请入住公寓失败，重复入住\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        apartment_code = 1
        res = self.ar_con.get_all_apartment()
        res_data = json.loads(res)
        for apartment in res_data:
            if apartment["is_full"] == 1:
                apartment_code = apartment["apartment_code"]
                break

        self.ar_con.apply_apartment(apartment_code)
        res = self.ar_con.apply_apartment(apartment_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_PLAYER_HAS_IN_APARTMENT["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_PLAYER_HAS_IN_APARTMENT["err_msg"]), "response msg mismatching...")

    def test_apply_apartment_full(self):
        """
        玩家申请入住公寓失败，公寓已满\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        res = self.ar_con.get_all_apartment()
        res_data = json.loads(res)
        apartment_code = res_data[0]["apartment_code"]
        is_full = res_data[0]["is_full"]

        while is_full == 1:
            self.ar_con.connect_server()
            account_id = CoRand.get_rand_int(100001)
            res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
            self.ar_con.apply_apartment(apartment_code)
            res = self.ar_con.get_all_apartment()
            res_data = json.loads(res)
            is_full = res_data[0]["is_full"]
        else:
            self.ar_con.connect_server()
            account_id = CoRand.get_rand_int(100001)
            res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
            res = self.ar_con.apply_apartment(apartment_code)
            res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_APART_HAS_FULL["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_APART_HAS_FULL["err_msg"]), "response msg mismatching...")

    # def test_apply_apartment_notexist(self):
    #     """
    #     玩家申请入住公寓失败，不存在的公寓\
    #     开发：黄良江(900000)\
    #     测试：林冰晶（791099）
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     apartment_code = CoRand.get_rand_int()
    #     self.ar_con.login(user_id, "im")
    #
    #     res = self.ar_con.apply_apartment(apartment_code)
    #     res_data = json.loads(res)

if __name__ == "__main__":
    unittest.main()
