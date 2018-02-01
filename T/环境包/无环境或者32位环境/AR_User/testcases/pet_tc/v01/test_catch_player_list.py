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
from api_call.SQL_modify.modify_SQL import ModifySql


class CatchPlayerListTest(unittest.TestCase):
    def setUp(self):
        print 'start run CatchPlayerList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "catchPlayerList"
        self.account_id = 100861

    def tearDown(self):
        print 'CatchPlayerList test complete.....close socket'

    def test_catch_player_list_catch_rich(self):
        """
        捕捉富豪--偷取单个富豪70%金币\
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
        #   获取玩家捕捉富豪前的金币数
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con.get_rich_player_list()
        res_data = json.loads(res)
        user_total_ids = []
        coins = []
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_total_ids.append(i["user_id"])
            res_info = self.ar_con.get_user_info(i["user_id"])
            res_info_data = json.loads(res_info)
            coins.append(res_info_data["coin"])
        #   获取富豪user_id和coin
        rich_user_index = coins.index(max(coins))
        rich_user_id = user_total_ids[rich_user_index]
        rich_coin_before = max(coins)
        user_ids = [rich_user_id]
        #   捕捉富豪
        res = self.ar_con.catch_player_list(user_ids)
        res_data = json.loads(res)
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            if i["user_id"] == rich_user_id:
                assert_that(i, has_key("steal_coin"), "no steal_coin response...")
                assert_that(i["steal_coin"], equal_to(int(rich_coin_before * 0.7)), "response steal_coin mismatch...")
                assert_that(i, has_key("coin"), "no coin response...")
                assert_that(i["coin"], equal_to(rich_coin_before), "response coin mismatch...")
            else:
                assert_that(i, has_key("steal_coin"), "no steal_coin response...")
                assert_that(i["steal_coin"], equal_to(-1), "response steal_coin mismatch...")
                assert_that(i, has_key("coin"), "no coin response...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        coin_after = res_data["coin"]
        assert_that(coin_after, equal_to(coin_before + int(rich_coin_before*0.7)), "user coin add num mismatch...")

    def test_catch_player_list_more_than_one(self):
        """
        捕捉富豪--玩家获取被捕捉所有玩家金币70%\
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
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con.get_rich_player_list()
        res_data = json.loads(res)
        user_ids = []
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])

        res = self.ar_con.catch_player_list(user_ids)
        res_data = json.loads(res)
        coin_add = 0
        for i in res_data:
            assert_that(i, has_key("coin"), "no coin response...")
            assert_that(i, has_key("steal_coin"), "no steal_coin response...")
            assert_that(i["steal_coin"], equal_to(int(i["coin"] * 0.7)), "response steal_coin mismatch...")
            coin_add += i["steal_coin"]
            assert_that(i, has_key("user_id"), "no user_id response...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        coin_after = res_data["coin"]
        assert_that(coin_after, equal_to(coin_before + coin_add), "user coin add num mismatch...")

    def test_catch_player_list_wrong_user(self):
        """
        捕捉富豪--偷取不是富豪列表里的玩家\
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
        self.ar_con.get_rich_player_list()
        steal_user_id = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        self.ar_con2.login(steal_user_id, "im")
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        user_ids = [steal_user_id]
        res = self.ar_con.catch_player_list(user_ids)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_DATA_NOT_IDENTICAL["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_DATA_NOT_IDENTICAL["err_msg"]), "response msg mismatching...")

    def test_catch_player_list_none(self):
        """
        捕捉富豪---未捕捉到任何宠物\
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
        self.ar_con.get_rich_player_list()
        user_ids = []
        res = self.ar_con.catch_player_list(user_ids)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_CATCH_ANY_ONE["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_CATCH_ANY_ONE["err_msg"]), "response msg mismatching...")

    # def test_catch_player_list_coin_change(self):
    #     """
    #     捕捉富豪---被捕捉富豪金币发生变化，捕捉获取当前金币数*0.7\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     account_id = CoRand.get_rand_int(100001)
    #     res = self.ar_con.login(account_id, "im")
    #     res_data = json.loads(res)
    #     user_id = res_data["user_id"]
    #     nick_name = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id, "guidance", 131071)
    #     self.ar_con.gm_reload_user_data(user_id)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id, "lottery_type", 105)
    #     self.ar_con.gm_reload_user_data(user_id)
    #     print "获取富豪列表："
    #     res = self.ar_con.get_rich_player_list()
    #     res_data = json.loads(res)
    #     assert_that(res_data[0], has_key("user_id"), "no user_id response...")
    #     user_id_catch = res_data[0]["user_id"]
    #     print "修改第一个玩家金币:"
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     self.ar_con2.login(user_id_catch, "im")
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_catch, "coin", 60000)
    #     self.ar_con2.gm_reload_user_data(user_id_catch)
    #     self.ar_con2.get_user_info(user_id_catch)
    #     print "捕捉第一个玩家，查看偷取金额："
    #     user_ids = []
    #     user_ids.append(user_id_catch)
    #     res = self.ar_con.catch_player_list(user_ids)
    #     res_data = json.loads(res)
    #     for i in res_data:
    #         assert_that(i, has_key("coin"), "no coin response...")
    #         assert_that(i, has_key("steal_coin"), "no steal_coin response...")
    #         assert_that(i, has_key("user_id"), "no user_id response...")
    #         if i["user_id"] == user_id_catch:
    #             assert i["steal_coin"] == 60000*0.7, "steal_coin mismatch..."


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(CatchPlayerListTest("test_catch_player_list_coin_change"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
