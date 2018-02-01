# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *
from cof.rand import CoRand


class GetPetInfoTest(unittest.TestCase):

    def setUp(self):
        print 'start run GetPetInfo test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getPetInfo"
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'GetPetInfo test complete.....close socket'
    
    def test_get_pet_info_success(self):
        """
        获取宠物信息成功,查看自己的宠物信息\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        res = self.ar_con.get_pet_list(user_id)
        res_data = json.loads(res)
        
        pet_id = res_data[0]["pet_id"]
        json_body = {
            "pet_id": pet_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_id"], equal_to(pet_id), "response pet_id mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "response user_id mismatching...")
        assert_that(res_data, has_key("pet_code"), "no pet_code response...")
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("is_capture"), "no is_capture response...")
        assert_that(res_data["is_capture"], equal_to(1), "response is_capture mismatching...")
        assert_that(res_data, has_key("head_status"), "no head_status response...")
        assert_that(res_data, has_key("head_level"), "no head_level response...")
        assert_that(res_data, has_key("arm_status"), "no arm_status response...")
        assert_that(res_data, has_key("arm_level"), "no arm_level response...")
        assert_that(res_data, has_key("clothes_status"), "no clothes_status response...")
        assert_that(res_data, has_key("clothes_level"), "no clothes_level response...")
        assert_that(res_data, has_key("shoes_status"), "no shoes_status response...")
        assert_that(res_data, has_key("shoes_level"), "no shoes_level response...")
        assert_that(res_data, has_key("skirt_status"), "no skirt_status response...")
        assert_that(res_data, has_key("skirt_level"), "no skirt_level response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")

    def test_get_pet_info_has_glass(self):
        """
        获取宠物信息,宠物带眼镜\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.239.119:807/ARTest/glass_true/1.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        json_body = {
            "pet_id": pet_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_id"], equal_to(pet_id), "response pet_id mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "response user_id mismatching...")
        assert_that(res_data, has_key("pet_code"), "no pet_code response...")
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("is_capture"), "no is_capture response...")
        assert_that(res_data["is_capture"], equal_to(1), "response is_capture mismatching...")
        assert_that(res_data, has_key("has_glass"), "no has_glass response...")
        assert_that(res_data["has_glass"], equal_to(1), "response has_glass mismatching...")
        assert_that(res_data, has_key("head_status"), "no head_status response...")
        assert_that(res_data, has_key("head_level"), "no head_level response...")
        assert_that(res_data, has_key("arm_status"), "no arm_status response...")
        assert_that(res_data, has_key("arm_level"), "no arm_level response...")
        assert_that(res_data, has_key("clothes_status"), "no clothes_status response...")
        assert_that(res_data, has_key("clothes_level"), "no clothes_level response...")
        assert_that(res_data, has_key("shoes_status"), "no shoes_status response...")
        assert_that(res_data, has_key("shoes_level"), "no shoes_level response...")
        assert_that(res_data, has_key("skirt_status"), "no skirt_status response...")
        assert_that(res_data, has_key("skirt_level"), "no skirt_level response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")

    def test_get_pet_info_not_has_glass(self):
        """
        获取宠物信息,宠物不带眼镜\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.239.119:807/ARTest/glass_false/1.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        json_body = {
            "pet_id": pet_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_id"], equal_to(pet_id), "response pet_id mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "response user_id mismatching...")
        assert_that(res_data, has_key("pet_code"), "no pet_code response...")
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("is_capture"), "no is_capture response...")
        assert_that(res_data["is_capture"], equal_to(1), "response is_capture mismatching...")
        assert_that(res_data, has_key("has_glass"), "no has_glass response...")
        assert_that(res_data["has_glass"], equal_to(0), "response has_glass mismatching...")
        assert_that(res_data, has_key("head_status"), "no head_status response...")
        assert_that(res_data, has_key("head_level"), "no head_level response...")
        assert_that(res_data, has_key("arm_status"), "no arm_status response...")
        assert_that(res_data, has_key("arm_level"), "no arm_level response...")
        assert_that(res_data, has_key("clothes_status"), "no clothes_status response...")
        assert_that(res_data, has_key("clothes_level"), "no clothes_level response...")
        assert_that(res_data, has_key("shoes_status"), "no shoes_status response...")
        assert_that(res_data, has_key("shoes_level"), "no shoes_level response...")
        assert_that(res_data, has_key("skirt_status"), "no skirt_status response...")
        assert_that(res_data, has_key("skirt_level"), "no skirt_level response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")

    def test_get_pet_info_no_exist(self):
        """
        获取不存在宠物信息\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        res = self.ar_con.login(100861, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]

        pet_id = 100861
        res = self.ar_con.get_pet_info(pet_id, user_id)
        res_data = json.loads(res)        

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_get_pet_info_others_success(self):
        """
        获取宠物信息成功,查看其他玩家的宠物信息\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)

        self.ar_con.connect_server()
        self.ar_con.login(100861, "im")
        res = self.ar_con.get_pet_info(pet_id, user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_id"], equal_to(pet_id), "response pet_id mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "response user_id mismatching...")
        assert_that(res_data, has_key("pet_code"), "no pet_code response...")
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("is_capture"), "no is_capture response...")
        assert_that(res_data["is_capture"], equal_to(1), "response is_capture mismatching...")

    def test_get_pet_info_no_cultivate_pet(self):
        """
        获取宠物信息:未传item_id和user_id,查看玩家当前养成宠信息（玩家未设置养成宠）\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_get_pet_info_without_item_id_and_user_id(self):
        """
        获取宠物信息,未传item_id和user_id,查看玩家当前养成宠信息\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)

        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_id"], equal_to(pet_id), "response pet_id mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "response user_id mismatching...")
        assert_that(res_data, has_key("pet_code"), "no pet_code response...")
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("is_capture"), "no is_capture response...")
        assert_that(res_data["is_capture"], equal_to(1), "response is_capture mismatching...")
        assert_that(res_data, has_key("has_glass"), "no has_glass response...")
        assert_that(res_data["has_glass"], equal_to(0), "response has_glass mismatching...")
        assert_that(res_data, has_key("head_status"), "no head_status response...")
        assert_that(res_data, has_key("head_level"), "no head_level response...")
        assert_that(res_data, has_key("arm_status"), "no arm_status response...")
        assert_that(res_data, has_key("arm_level"), "no arm_level response...")
        assert_that(res_data, has_key("clothes_status"), "no clothes_status response...")
        assert_that(res_data, has_key("clothes_level"), "no clothes_level response...")
        assert_that(res_data, has_key("shoes_status"), "no shoes_status response...")
        assert_that(res_data, has_key("shoes_level"), "no shoes_level response...")
        assert_that(res_data, has_key("skirt_status"), "no skirt_status response...")
        assert_that(res_data, has_key("skirt_level"), "no skirt_level response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")

    def test_get_pet_info_without_user_id(self):
        """
        获取宠物信息,未传user_id,查看玩家自己的宠物信息\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)

        json_body = {
                "pet_id": pet_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data["pet_id"], equal_to(pet_id), "response pet_id mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "response user_id mismatching...")
        assert_that(res_data, has_key("pet_code"), "no pet_code response...")
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("is_capture"), "no is_capture response...")
        assert_that(res_data["is_capture"], equal_to(1), "response is_capture mismatching...")
        assert_that(res_data, has_key("has_glass"), "no has_glass response...")
        assert_that(res_data["has_glass"], equal_to(0), "response has_glass mismatching...")
        assert_that(res_data, has_key("head_status"), "no head_status response...")
        assert_that(res_data, has_key("head_level"), "no head_level response...")
        assert_that(res_data, has_key("arm_status"), "no arm_status response...")
        assert_that(res_data, has_key("arm_level"), "no arm_level response...")
        assert_that(res_data, has_key("clothes_status"), "no clothes_status response...")
        assert_that(res_data, has_key("clothes_level"), "no clothes_level response...")
        assert_that(res_data, has_key("shoes_status"), "no shoes_status response...")
        assert_that(res_data, has_key("shoes_level"), "no shoes_level response...")
        assert_that(res_data, has_key("skirt_status"), "no skirt_status response...")
        assert_that(res_data, has_key("skirt_level"), "no skirt_level response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")

if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(GetPetInfoTest("test_get_pet_info_has_glass"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
