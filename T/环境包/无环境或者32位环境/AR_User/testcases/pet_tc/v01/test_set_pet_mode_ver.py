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


class SetPetModeVerTest(unittest.TestCase):
    """
    设置人脸宠属性
    """
    
    def setUp(self):
        print 'start run setPetModelVer test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "setPetModelVer"
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
    
    def tearDown(self):
        print 'setPetModelVer test complete.....close socket'

    def test_set_pet_mode_ver_success(self):
        """
        设置人脸宠属性成功\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        ver = 123
        res = self.ar_con.set_pet_mode_ver(item_id, ver)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_set_pet_mode_ver_other_user(self):
        """
        设置人脸宠属性--设置其他玩家宠物\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        print"玩家A获取人脸宠："
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)

        print"玩家B设置玩A的人脸宠属性："
        self.ar_con.connect_server()
        self.ar_con.login(100861, "im")
        res = self.ar_con.set_pet_mode_ver(item_id, 123)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_set_pet_mode_ver_other_pet(self):
        """
        设置人脸宠属性--设置原生宠/灵魂宠属性\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la")
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        item_type = res_data["item_type"]
        if item_type != 2:
            res = self.ar_con.set_pet_mode_ver(item_id, 123)
            res_data = json.loads(res)
            assert_that(res_data, has_key("code"), "no code response...")
            assert_that(res_data, has_key("err_msg"), "no err_msg response...")
            assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
            assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_set_pet_mode_ver_cultivate(self):
        """
        设置人脸宠属性--设置养成宠属性\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        res = self.ar_con.set_pet_mode_ver(item_id, 123)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_set_pet_mode_ver_error_pet_id(self):
        """
        设置人脸宠属性失败--错误的宠物id\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        pet_id = CoRand.get_rand_int(1, 1000)
        ver = 123
        res = self.ar_con.set_pet_mode_ver(pet_id, ver)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_set_pet_mode_ver_error_ver(self):
        """
        设置人脸宠属性失败--无效的版本\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)

        ver = CoRand.get_random_word_filter_sensitive(6)
        res = self.ar_con.set_pet_mode_ver(item_id, ver)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_set_pet_mode_ver_no_param(self):
        """
        设置人脸宠属性失败--请求未带参数\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(SetPetModeVerTest("test_set_pet_mode_ver_cultivate"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
