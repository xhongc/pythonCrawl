# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.SQL_modify.modify_SQL import ModifySql
from api_call.message.err_code import *
from cof.rand import CoRand


class GetUsersTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetUsers test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getUsers"
        self.account_id = 100861

    def tearDown(self):
        print 'GetUsers test complete.....close socket'

    def test_get_users_success(self):
        """
        获取多玩家简要信息--50位玩家\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        user_ids = self.sql.query_user_ids(50)
        res = self.ar_con.get_users(user_ids)
        res_data = json.loads(res)
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            assert_that(i, has_key("nick_name"), "no nick_name response...")
            assert_that(i, has_key("icon"), "no icon response...")
            assert_that(i, has_key("sex"), "no sex response...")

    def test_get_users_one_date(self):
        """
        获取一位玩家简要信息--验证获取信息正确性\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        sex = CoRand.get_rand_int(0, 1)
        icon = CoRand.get_random_word_filter_sensitive(10)
        self.ar_con.modify_info(nick_name, icon, sex)
        user_ids = [user_id]

        self.ar_con.connect_server()
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.get_users(user_ids)
        res_data = json.loads(res)
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            assert_that(i["user_id"], equal_to(user_id), "user_id mismatch...")
            assert_that(i, has_key("nick_name"), "no nick_name response...")
            assert_that(i["nick_name"], equal_to(nick_name), "nick_name mismatch...")
            assert_that(i, has_key("icon"), "no icon response...")
            assert_that(i["icon"], equal_to(icon), "icon mismatch...")
            assert_that(i, has_key("sex"), "no sex response...")
            assert_that(i["sex"], equal_to(sex), "sex mismatch...")

    def test_get_users_more_than_50(self):
        """
        获取多玩家简要信息--超过50位玩家\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        user_ids = self.sql.query_user_ids(60)
        res = self.ar_con.get_users(user_ids)
        res_data = json.loads(res)
        assert_that(res_data, has_length(50), "response length mismatch...")
        j = 0
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            assert_that(i["user_id"], equal_to(int(user_ids[j])), "response user_id mismatch...")
            j += 1

    def test_get_users_none(self):
        """
        获取多玩家简要信息--user_ids列表为空\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        user_ids = []
        res = self.ar_con.get_users(user_ids)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetUsersTest("test_get_users_more_than_50"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
