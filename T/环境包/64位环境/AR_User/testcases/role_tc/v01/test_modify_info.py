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


class ModifyInfoTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run ModifyInfo test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "modifyInfo"
    
    def tearDown(self):
        print 'ModifyInfo test complete.....close socket'
    
    def test_modify_info_success(self):
        """
        修改角色信息成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        res = self.ar_con.login(100861, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        sign = CoRand.get_random_word_filter_sensitive(6)
        res = self.ar_con.modify_info(nick_name, sign)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("nick_name"), "no nike_name response...")
        assert_that(res_data["nick_name"], equal_to(nick_name), "response code mismatching...")
    
    def test_modify_info_exist(self):
        """
        修改成已存在角色\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        self.ar_con.connect_server()
        self.ar_con.login(791099, "im")
        res = self.ar_con.modify_info(nick_name)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_ROLE_ALREADY_EXIST["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_ROLE_ALREADY_EXIST["err_msg"]), "response msg mismatching...")
        
    def test_modify_info_without_params(self):
        """
        修改角色信息-不传参数，不修改\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_modify_info_nick_name_chinese(self):
        """
        修改角色信息成功，角色名称中文\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        nick_name = CoRand.get_rand_chinese(7)

        json_body = {
            "sex": 1,
            "icon": "https://www.baidu.com/",
            "nick_name": nick_name
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_modify_info_nick_name_combination(self):
        """
        修改角色信息成功，角色名称中文、英文、数字组合\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_rand_combination(4)
        res = self.ar_con.modify_info(nick_name)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_modify_info_nick_name_illegal(self):
        """
        修改角色信息失败，非法字符\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        nick_name = "c a o"
        res = self.ar_con.modify_info(nick_name)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_modify_info_nick_name_long(self):
        """
        修改角色信息失败，昵称超出字符限制\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        nick_name = CoRand.randomword(16)
        res = self.ar_con.modify_info(nick_name)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    # def test_modify_info_sex_illegal(self):
    #     """
    #     创建角色成功，性别值非法\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     self.ar_con.login(100861, "im")
    #     nick_name = CoRand.randomword(6)
    #
    #     json_body = {
    #         "sex": 111,
    #         "icon": "https://www.baidu.com/",
    #         "nick_name": nick_name
    #     }
    #     res = self.ar_con.get_res(self.api_name, json_body)
    #     res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(ModifyInfoTest("test_modify_info_nick_name_long"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
