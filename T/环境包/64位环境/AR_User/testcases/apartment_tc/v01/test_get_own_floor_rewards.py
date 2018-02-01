# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
import time
from cof.rand import CoRand


class GetOwnFloorRewardsTest(unittest.TestCase):
    """
    获取其他人打扫自己房间的奖励
    """

    def setUp(self):
        print 'start run GetOwnFloorRewards test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetOwnFloorRewards test complete.....close socket'

    def test_get_own_floor_rewards_success(self):
        """
        获取其他人打扫自己房间的奖励成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id_1 = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        apartment_code_1 = 1
        res = self.ar_con.get_all_apartment()
        res_data = json.loads(res)
        for apartment in res_data:
            if apartment["is_full"] == 1:
                apartment_code_1 = apartment["apartment_code"]
                break
        res = self.ar_con.apply_apartment(apartment_code_1)
        res_data = json.loads(res)
        floor_1 = res_data["floor"]

        self.ar_con.connect_server()

        account_id_2 = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.match_pet(pet_url)
        res_data = json.loads(res)
        pet_id = res_data["pet_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.sweep_apartment(apartment_code_1, user_id_1, floor_1)

        time.sleep(901)
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        res = self.ar_con.get_own_floor_rewards()
        res_data = json.loads(res)

        for rewards in res_data:
            assert_that(rewards, has_key("pet_id"), "no pet_id response...")
            assert_that(rewards, has_key("time"), "no time response...")
            assert_that(rewards, has_key("coin"), "no coin response...")
            assert_that(rewards, has_key("contribute_value"), "no contribute_value response...")
            assert_that(rewards, has_key("construct_value"), "no construct_value response...")
            assert_that(rewards, has_key("user_id"), "no user_id response...")
            assert_that(rewards["user_id"], equal_to(user_id_2), "response user_id mismatching...")

if __name__ == "__main__":
    unittest.main()
