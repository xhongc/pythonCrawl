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


class SweepApartmentTest(unittest.TestCase):
    """
    打扫公寓楼
    """

    def setUp(self):
        print 'start run SweepApartment test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'SweepApartment test complete.....close socket'

    def test_sweep_apartment_success(self):
        """
        打扫公寓楼成功\
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

        res = self.ar_con.sweep_apartment(apartment_code, user_id, floor)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_info"), "no pet_info response...")
        assert_that(res_data["pet_info"], has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_info"], has_key("pet_code"), "no pet_code response...")
        assert_that(res_data["pet_info"], has_key("user_id"), "no user_id response...")
        assert_that(res_data["pet_info"], has_key("name"), "no name response...")
        assert_that(res_data["pet_info"], has_key("quality"), "no quality response...")
        assert_that(res_data["pet_info"], has_key("evolution_type"), "no pet_code response...")
        assert_that(res_data["pet_info"], has_key("lookface"), "no user_id response...")
        assert_that(res_data["pet_info"], has_key("power"), "no name response...")
        assert_that(res_data["pet_info"], has_key("level"), "no quality response...")
        assert_that(res_data["pet_info"], has_key("exp"), "no exp response...")
        assert_that(res_data["pet_info"], has_key("hp"), "no hp response...")
        assert_that(res_data["pet_info"], has_key("is_capture"), "no is_capture response...")
        assert_that(res_data["pet_info"], has_key("atk"), "no atk response...")
        assert_that(res_data["pet_info"], has_key("hit_rate"), "no hit_rate response...")
        assert_that(res_data["pet_info"], has_key("dodge_rate"), "no dodge_rate response...")
        assert_that(res_data["pet_info"], has_key("crit_rate"), "no crit_rate response...")
        assert_that(res_data["pet_info"], has_key("anti_crit_rate"), "no anti_crit_rate response...")
        assert_that(res_data["pet_info"], has_key("skill1"), "no skill1 response...")
        assert_that(res_data["pet_info"], has_key("skill1_level"), "no skill1_level response...")
        assert_that(res_data["pet_info"], has_key("skill2"), "no skill2 response...")
        assert_that(res_data["pet_info"], has_key("skill2_level"), "no skill2_level response...")
        assert_that(res_data["pet_info"], has_key("skill3"), "no skill3 response...")
        assert_that(res_data["pet_info"], has_key("skill3_level"), "no skill3_level response...")
        assert_that(res_data["pet_info"], has_key("skill4"), "no skill4 response...")
        assert_that(res_data["pet_info"], has_key("skill4_level"), "no skill4_level response...")

    def test_sweep_apartment_others_success(self):
        """
        打扫其他玩家公寓楼成功\
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
        self.ar_con.login(account_id_2, "im")
        pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.match_pet(pet_url)
        res_data = json.loads(res)
        pet_id = res_data["pet_id"]
        self.ar_con.capture_pet(pet_id)
        res = self.ar_con.sweep_apartment(apartment_code_1, user_id_1, floor_1)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_info"), "no pet_info response...")
        assert_that(res_data["pet_info"], has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_info"], has_key("pet_code"), "no pet_code response...")
        assert_that(res_data["pet_info"], has_key("user_id"), "no user_id response...")
        assert_that(res_data["pet_info"], has_key("name"), "no name response...")

    def test_sweep_apartment_no_pet(self):
        """
        打扫公寓楼失败，无空闲宠物\
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

        res = self.ar_con.sweep_apartment(apartment_code, user_id, floor)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NO_FREEPET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NO_FREEPET["err_msg"]), "response msg mismatching...")

    def test_sweep_apartment_repeat(self):
        """
        打扫公寓楼失败，打扫中，不能重复打扫\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.match_pet(pet_url)
        res_data = json.loads(res)
        pet_id = res_data["pet_id"]
        self.ar_con.capture_pet(pet_id)
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

        self.ar_con.sweep_apartment(apartment_code, user_id, floor)
        res = self.ar_con.sweep_apartment(apartment_code, user_id, floor)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_APART_IS_IN_SWEEPING["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_APART_IS_IN_SWEEPING["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    unittest.main()
