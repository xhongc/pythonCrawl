# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *
from api_call.SQL_modify.modify_SQL import ModifySql
import time
from cof.rand import CoRand


class GetRandFriendInfoTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetRandFriendInfo test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetRandFriendInfo test complete.....close socket'

    def test_get_rand_friend_info_success(self):
        """
        获取随机玩家--抽中攻击卡\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id)

        res = self.ar_con.get_rand_friend_info()
        res_data = json.loads(res)

        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data, has_key("nick_name"), "no nick_name response...")
        assert_that(res_data, has_key("sex"), "no sex response...")
        assert_that(res_data, has_key("icon"), "no icon response...")
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data, has_key("can_attack"), "no can_attack response...")

    def test_get_rand_friend_info_without_attack(self):
        """
        获取随机玩家--无攻击卡\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(791099, "im")

        res = self.ar_con.get_rand_friend_info()
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ALLOW_ATTACK["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ALLOW_ATTACK["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetRandFriendInfoTest("test_get_rand_friend_info_without_attack"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)