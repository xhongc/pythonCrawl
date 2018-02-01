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


class UpdateFloorNameTest(unittest.TestCase):
    """
    重命名玩家楼层名称
    """

    def setUp(self):
        print 'start run UpdateFloorName test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()

    def tearDown(self):
        print 'UpdateFloorName test complete.....close socket'

    def test_update_floor_name_success(self):
        """
        重命名玩家楼层名称成功\
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

        floor_name = u"重命名"
        res = self.ar_con.update_floor_name(apartment_code, floor_name, floor)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_apartment_floor_list(apartment_code)
        res_data = json.loads(res)
        for user in res_data:
            if user["user_id"] == user_id:
                assert_that(user, has_key("floor_name"), "no floor_name response...")
                assert user["floor_name"] == floor_name, "response floor_name mismatching..."
                break


if __name__ == "__main__":
    unittest.main()
