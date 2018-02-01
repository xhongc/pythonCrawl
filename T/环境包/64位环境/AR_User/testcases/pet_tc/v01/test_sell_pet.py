# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
import time
from api_call.message.err_code import *
from cof.rand import CoRand


class SellPetTest(unittest.TestCase):
    """
    出售宠物
    """

    def setUp(self):
        print 'start run SellPet test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'SellPet test complete.....close socket'

    def test_sell_pet_success(self):
        """
        出售单只宠物成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        pet_ids = []
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["pet_id"]
        self.ar_con.capture_pet(pet_id)

        pet_ids.append(res_data["pet_id"])
        res = self.ar_con.sell_pet(pet_ids)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_pet_info(pet_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_sell_pet_batch_success(self):
        """
        批量出售宠物成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        pet_ids = []
        for x in range(0, 5):
            res = self.ar_con.scan_face(self.pet_url, "la", 1)
            res_data = json.loads(res)
            pet_id = res_data["pet_id"]
            self.ar_con.capture_pet(pet_id)
            pet_ids.append(res_data["pet_id"])

        res = self.ar_con.sell_pet(pet_ids)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_sell_pet_notexist(self):
        """
        出售不存在的宠物\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        目前提示参数错误，建议修改
        """
        self.ar_con.login(100861, "im")
        pet_ids = []
        pet_id = CoRand.get_rand_int()
        pet_ids.append(pet_id)

        res = self.ar_con.sell_pet(pet_ids)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    unittest.main()
