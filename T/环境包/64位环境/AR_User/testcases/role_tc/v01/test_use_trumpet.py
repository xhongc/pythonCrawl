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
from api_call.SQL_modify.modify_SQL import ModifySql


class UseTrumpetTest(unittest.TestCase):
    def setUp(self):
        print 'start run UseTrumpet test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'UseTrumpet test complete.....close socket'

    def test_use_trumpet_enough(self):
        """
        使用喇叭：喇叭数足够\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("trumpets"), "no trumpets response...")
        trumpet_before = res_data["trumpets"]
        res = self.ar_con.use_trumpet()
        res_data = json.loads(res)
        assert_that(res_data, has_key("trumpets"), "no trumpets response...")
        assert_that(res_data["trumpets"], equal_to(trumpet_before-1), "response trumpet mismatch")

    def test_use_trumpet_not_enough(self):
        """
        使用喇叭：喇叭数不足\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        self.ar_con.get_user_info(user_id)
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "trumpets", 0)
        self.ar_con.gm_reload_user_data(user_id)

        res = self.ar_con.use_trumpet()
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ENOUGH_TRUMPETS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ENOUGH_TRUMPETS["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(UseTrumpetTest("test_use_trumpet_not_enough"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
