# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand
from api_call.message.err_code import *


class GetPetListTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run GetPetList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861
        self.api_name = "getPetList"
    
    def tearDown(self):
        print 'GetPetList test complete.....close socket'
    
    def test_get_pet_list_success(self):
        """
        获取其他玩家宠物列表成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)

        self.ar_con.connect_server()
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.get_pet_list(user_id_1)
        res_data = json.loads(res)
        for petinfo in res_data:
            assert_that(petinfo, has_key("pet_id"), "no item_id response...")
            assert_that(petinfo, has_key("user_id"), "no user_id response...")
            assert_that(petinfo["user_id"], equal_to(user_id_1), "response user_id mismatching...")
            assert_that(petinfo, has_key("pet_code"), "no pet_code response...")
            assert_that(petinfo, has_key("name"), "no name response...")
            assert_that(petinfo, has_key("is_capture"), "no is_capture response...")
            assert_that(petinfo, has_key("head_status"), "no head_status response...")
            assert_that(petinfo, has_key("head_level"), "no head_level response...")
            assert_that(petinfo, has_key("arm_status"), "no arm_status response...")
            assert_that(petinfo, has_key("arm_level"), "no arm_level response...")
            assert_that(petinfo, has_key("clothes_status"), "no clothes_status response...")
            assert_that(petinfo, has_key("clothes_level"), "no clothes_level response...")
            assert_that(petinfo, has_key("shoes_status"), "no shoes_status response...")
            assert_that(petinfo, has_key("shoes_level"), "no shoes_level response...")
            assert_that(petinfo, has_key("skirt_status"), "no skirt_status response...")
            assert_that(petinfo, has_key("skirt_level"), "no skirt_level response...")
            assert_that(petinfo, has_key("pet_idx"), "no item_idx response...")
            assert_that(petinfo, has_key("is_complete"), "no is_complete response...")

    def test_get_pet_list_without_params(self):
        """
        获取宠物列表，未传参数获取玩家自己的宠物列表\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        for petinfo in res_data:
            assert_that(petinfo, has_key("pet_id"), "no item_id response...")
            assert_that(petinfo, has_key("user_id"), "no user_id response...")
            assert_that(petinfo["user_id"], equal_to(user_id), "response user_id mismatching...")
            assert_that(petinfo, has_key("pet_code"), "no pet_code response...")
            assert_that(petinfo, has_key("name"), "no name response...")

    def test_get_pet_list_user_id_error(self):
        """
        获取宠物列表失败，用户id错误\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        user_id = CoRand.randomword(8)
        json_body = {
            "user_id": user_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetPetListTest("test_get_pet_list_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
