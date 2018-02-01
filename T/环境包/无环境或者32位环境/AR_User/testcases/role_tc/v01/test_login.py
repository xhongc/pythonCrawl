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


class LoginTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run Login test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "login"
    
    def tearDown(self):
        print 'Login test complete.....close socket'
    
    def test_login_success(self):
        """
        登录成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        user_type = "im"
        self.ar_con.login(account_id, user_type, uc_id)
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        self.ar_con.connect_server()
        res = self.ar_con.login(account_id, user_type, uc_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")

    def test_login_not_create_role(self):
        """
        登录成功,未创建角色\
        开发：黄良江(900000)\
        测试：林冰晶(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        user_type = "im"

        res = self.ar_con.login(account_id, user_type)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NO_CREATE_ROLE["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NO_CREATE_ROLE["err_msg"]), "response msg mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
    
    def test_repeat_login(self):
        """
        重复登录\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = 100861
        user_type = "im"
        
        self.ar_con.login(account_id, user_type)
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.login(account_id, user_type)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NO_FOUND_HANDLER["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NO_FOUND_HANDLER["err_msg"]), "response msg mismatching...")
    
    def test_login_without_token(self):
        """
        登录失败，缺少token\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = 100861
        user_type = "im"
        
        json_body = {
            "user_type": user_type,
            "user_id": account_id
        } 
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")
    
    def test_login_without_user_id(self):
        """
        登录失败，缺少userId\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        token = "0000"
        user_type = "im"
        
        json_body = {
            "user_type": user_type,
            "token": token
        } 
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_login_error_user_id(self):
        """
        登录失败，错误的userId\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.uuid(16)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    unittest.main()
    # # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(LoginTest("test_login_success"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
