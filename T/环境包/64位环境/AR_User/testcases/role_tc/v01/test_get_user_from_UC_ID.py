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


class GetUserFromUCIDTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetUserFromUCID test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getUserFromUcID"
        self.account_id = 100861

    def tearDown(self):
        print 'GetUserFromUCID test complete.....close socket'

    def test_get_user_from_uc_id_success(self):
        """
        获取用户信息--根据UC_ID获取用户信息成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        icon = CoRand.get_random_word_filter_sensitive(16)
        sex = CoRand.get_rand_int(0, 1)
        self.ar_con.modify_info(nick_name, icon, sex, sign="API测试")

        res = self.ar_con.get_user_from_uc_id(uc_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "user_id mismatching...")
        assert_that(res_data, has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["nick_name"], equal_to(nick_name), "nick_name mismatching...")
        assert_that(res_data, has_key("icon"), "no icon response...")
        assert_that(res_data["icon"], equal_to(icon), "icon mismatching...")
        assert_that(res_data, has_key("sex"), "no sex response...")
        assert_that(res_data["sex"], equal_to(sex), "sex mismatching...")

    def test_get_user_from_uc_id__login_without_uc_id(self):
        """
        获取用户信息--未带uc_id登陆用户查询\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        self.ar_con.connect_server()
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.get_user_from_uc_id(uc_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "user_id mismatching...")
        assert_that(res_data, has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["nick_name"], equal_to(nick_name), "nick_name mismatching...")
        assert_that(res_data, has_key("icon"), "no icon response...")
        assert_that(res_data["icon"], equal_to("https://www.baidu.com/"), "nick_name mismatching...")

    def test_get_user_from_uc_id_error_uc_id(self):
        """
        获取用户信息--不存在的uc_id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        uc_id = CoRand.get_rand_int()

        res = self.ar_con.get_user_from_uc_id(uc_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_FRIEND_INFO["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_FRIEND_INFO["err_msg"]), "response msg mismatching...")

    def test_get_user_from_uc_id_without_params(self):
        """
        获取用户信息--未传参数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")

        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetUserFromUCIDTest("test_get_user_from_uc_id_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
