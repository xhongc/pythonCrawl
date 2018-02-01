# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand


class GetSweepingPetInfoTest(unittest.TestCase):
    """
    查看玩家派出去打扫的宠物信息
    """

    def setUp(self):
        print 'start run GetSweepingPetInfo test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetSweepingPetInfo test complete.....close socket'

    def test_get_sweeping_pet_info_success(self):
        """
        查看玩家派出去打扫的宠物信息成功\
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

        pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.match_pet(pet_url)
        res_data = json.loads(res)
        pet_id = res_data["pet_id"]
        self.ar_con.capture_pet(pet_id)

        self.ar_con.sweep_apartment(apartment_code, user_id, floor)
        res = self.ar_con.get_sweeping_pet_info(apartment_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_info"), "no pet_info response...")
        assert_that(res_data, has_key("countdown"), "no countdown response...")

        assert_that(res_data["pet_info"], has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_info"], has_key("pet_code"), "no pet_code response...")
        assert_that(res_data["pet_info"], has_key("user_id"), "no user_id response...")
        assert_that(res_data["pet_info"], has_key("name"), "no name response...")
        assert_that(res_data["pet_info"], has_key("quality"), "no quality response...")

if __name__ == "__main__":
    unittest.main()
