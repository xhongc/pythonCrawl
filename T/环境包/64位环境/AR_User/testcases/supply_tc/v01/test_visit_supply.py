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


class VisitSupplyTest(unittest.TestCase):
    """
    膜拜神仙居
    """

    def setUp(self):
        print 'start run VisitSupply test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'VisitSupply test complete.....close socket'

    def test_visit_supply(self):
        """
        膜拜神仙居成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        latitude = 26.092
        longitude = 119.314
        res = self.ar_con.get_supply(latitude, longitude)
        res_data = json.loads(res)
        _id = res_data[0]["id"]

        res = self.ar_con.visit_supply(latitude, longitude, _id)
        res_data = json.loads(res)

        for item in res_data:
            assert_that(item, has_key("supply_id"), "no supply_id response...")
            assert item["supply_id"] == _id
            assert_that(item, has_key("id"), "no id response...")
            assert_that(item, has_key("item_code"), "no item_code response...")
            assert_that(item, has_key("count"), "no count response...")

        res = self.ar_con.get_supply(latitude, longitude)
        res_data = json.loads(res)
        assert_that(res_data[0], has_key("cd_time"), "no cd_time response...")
        assert res_data[0]["cd_time"] != 0

    def test_visit_supply_repeat(self):
        """
        膜拜神仙居失败，重复膜拜\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        latitude = 26.092
        longitude = 119.314
        res = self.ar_con.get_supply(latitude, longitude)
        res_data = json.loads(res)
        _id = res_data[0]["id"]

        self.ar_con.visit_supply(latitude, longitude, _id)
        res = self.ar_con.visit_supply(latitude, longitude, _id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_HAS_VISIT_SUPPLY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_HAS_VISIT_SUPPLY["err_msg"]), "response msg mismatching...")

    def test_visit_supply_notexist(self):
        """
        膜拜神仙居失败，不存在的神仙居\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        latitude = 26.092
        longitude = 119.314
        _id = CoRand.get_rand_int()
        res = self.ar_con.visit_supply(latitude, longitude, _id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_SUPPLY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_SUPPLY["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    unittest.main()
