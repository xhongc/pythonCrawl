# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *
from cof.rand import CoRand
import time
from api_call.SQL_modify.modify_SQL import ModifySql


class GetRichestPlayerTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetRichestPlayer test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getRichestPlayer"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'GetRichestPlayer test complete.....close socket'

    def test_get_richest_player_no_steal(self):
        """
        获取最富富豪--未抽中偷袭\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.ar_con.get_rich_player_list()
        res = self.ar_con.get_richest_player()
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("nick_name"), "no nick_name response...")
        assert_that(res_data, has_key("icon"), "no icon response...")

    def test_get_richest_player(self):
        """
        获取最富富豪\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "lottery_type", 105)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_rich_player_list()
        res_data = json.loads(res)
        assert res_data != []
        user_total_ids = []
        coins = []
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_total_ids.append(i["user_id"])
            res_info = self.ar_con.get_user_info(i["user_id"])
            res_info_data = json.loads(res_info)
            coins.append(res_info_data["coin"])
        rich_user_index = coins.index(max(coins))
        rich_user_nick_name = res_data[rich_user_index]["nick_name"]
        rich_user_icon = res_data[rich_user_index]["icon"]

        res = self.ar_con.get_richest_player()
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(max(coins)), "response coin mismatch...")
        assert_that(res_data, has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["nick_name"], equal_to(rich_user_nick_name), "response nick_name mismatch...")
        assert_that(res_data, has_key("icon"), "no icon response...")
        assert_that(res_data["icon"], equal_to(rich_user_icon), "response icon mismatch...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetRichestPlayerTest("test_get_richest_player"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)