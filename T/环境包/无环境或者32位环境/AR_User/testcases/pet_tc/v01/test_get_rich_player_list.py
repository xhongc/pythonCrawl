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


class GetRichPlayerListTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetRichPlayerList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getRichPlayerList"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'GetRichPlayerList test complete.....close socket'

    def test_get_rich_player_list_no_steal(self):
        """
        获取富豪列表--未抽中偷袭\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_rich_player_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ALLOW_STEAL["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ALLOW_STEAL["err_msg"]), "response msg mismatching...")

    def test_get_rich_player_list_success(self):
        """
        获取富豪列表--获取8位玩家，富豪金币>=10w,富豪金币>其余玩家金币>=1w，排除玩家本人\
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
        user_ids = []
        coins = []
        for i in res_data:
            assert_that(i, has_key("nick_name"), "no nick_name response...")
            assert_that(i, has_key("name"), "no name response...")
            assert_that(i, has_key("icon"), "no icon response...")
            assert_that(i, has_key("has_glass"), "no has_glass response...")
            assert_that(i, has_key("head_status"), "no head_status response...")
            assert_that(i, has_key("head_level"), "no head_level response...")
            assert_that(i, has_key("arm_status"), "no arm_status response...")
            assert_that(i, has_key("arm_level"), "no arm_level response...")
            assert_that(i, has_key("clothes_status"), "no clothes_status response...")
            assert_that(i, has_key("clothes_level"), "no clothes_level response...")
            assert_that(i, has_key("skirt_status"), "no skirt_status response...")
            assert_that(i, has_key("skirt_level"), "no skirt_level response...")
            assert_that(i, has_key("shoes_status"), "no shoes_status response...")
            assert_that(i, has_key("shoes_level"), "no shoes_level response...")
            assert_that(i, has_key("pet_code"), "no pet_code response...")
            assert_that(i, has_key("pet_id"), "no pet_id response...")
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
            res_info = self.ar_con.get_user_info(i["user_id"])
            res_info_data = json.loads(res_info)
            coins.append(res_info_data["coin"])
            assert_that(res_info_data, has_key("pet_idx"), "no pet_idx response...")
            assert_that(res_info_data["pet_idx"], not_(0), "response pet_idx mismatch...")
        coin_max = max(coins)
        coin_min = min(coins)
        assert_that(coin_max, greater_than(100000), "response coin less than 10w...")
        assert_that(coin_min, greater_than_or_equal_to(10000), "response coin less than 1w...")
        assert user_id not in user_ids
        assert_that(res_data, has_length(4), "response length mismatch...")

    def test_get_rich_player_list_friend_rich(self):
        """
        获取富豪列表--有好友金币>10w,抽取概率好友50%、陌生人50%\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        res = self.ar_con2.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con2.capture_pet(pet_id)
        self.ar_con2.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con2.upgrade_pet_part(part)
        print "创建好友玩家B："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.add_friend(user_id_2)
        print "A同意添加好友："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, 1)
        print "B执行50次获取富豪操作："
        self.ar_con.get_rev()
        friend_num = 0
        rand_num = 0
        for i in range(0, 50):
            user_total_ids = []
            coins = []
            self.sql = ModifySql()
            self.sql.update_user(user_id_1, "lottery_type", 105)
            self.ar_con.gm_reload_user_data(user_id_1)
            res = self.ar_con.get_rich_player_list()
            res_data = json.loads(res)
            for j in res_data:
                assert_that(j, has_key("user_id"), "no user_id response...")
                user_total_ids.append(j["user_id"])
                res_info = self.ar_con.get_user_info(j["user_id"])
                res_info_data = json.loads(res_info)
                coins.append(res_info_data["coin"])
            print user_total_ids
            if user_id_2 in user_total_ids:
                friend_num += 1
            else:
                rand_num += 1
            rich_user_index = coins.index(max(coins))
            rich_user_id = user_total_ids[rich_user_index]
            user_ids = [rich_user_id]
            self.ar_con.catch_player_list(user_ids)
            self.sql = ModifySql()
            self.sql.update_user(user_id_2, "coin", 1000000)
            self.ar_con2.gm_reload_user_data(user_id_2)
        print "转盘50次，抽中好友次数：" + str(friend_num)
        print "转盘50次，抽中随机玩家次数：" + str(rand_num)
        # assert_that(abs(friend_num-rand_num), less_than(10), "draw probability mismatch")

    def test_get_rich_player_list_friend_poor(self):
        """
        获取富豪列表--好友金币<10w,从陌生人中随机抽取\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "coin", 100)
        self.ar_con2.gm_reload_user_data(user_id_2)
        print "创建好友玩家B："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.add_friend(user_id_2)
        print "A同意添加好友："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, 1)
        print "B获取富豪列表："
        self.ar_con.get_rev()
        user_ids = []
        for i in range(0, 10):
            self.sql = ModifySql()
            self.sql.update_user(user_id_1, "lottery_type", 105)
            self.ar_con.gm_reload_user_data(user_id_1)
            res = self.ar_con.get_rich_player_list()
            res_data = json.loads(res)
            for j in res_data:
                assert_that(j, has_key("user_id"), "no user_id response...")
                user_ids.append(j["user_id"])
        print user_ids
        assert user_id_2 not in user_ids

    def test_get_rich_player_list_not_catch_rich_third(self):
        """
        捕捉富豪--第一次未捕捉到富豪，第二三次获取富豪列表仍是同一个富豪，第四次重新获取富豪\
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
        print "第一次获取富豪列表"
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
        #   获取富豪和非富豪的user_id和coin
        rich_user_index_1 = coins.index(max(coins))
        rich_user_id_1 = user_total_ids[rich_user_index_1]
        poor_user_index_1 = coins.index(min(coins))
        poor_user_id_1 = user_total_ids[poor_user_index_1]
        user_ids_1 = [poor_user_id_1]
        if poor_user_id_1 != rich_user_id_1:
            print "第一次获取富豪id是：" + str(rich_user_id_1)
            print "第一次捕捉非富豪:"
            self.ar_con.catch_player_list(user_ids_1)
            print "第二次获取富豪列表："
            self.sql = ModifySql()
            self.sql.update_user(user_id, "lottery_type", 105)
            self.ar_con.gm_reload_user_data(user_id)
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
            # 获取富豪和非富豪的user_id和coin
            rich_user_index_2 = coins.index(max(coins))
            rich_user_id_2 = user_total_ids[rich_user_index_2]
            poor_user_index_2 = coins.index(min(coins))
            poor_user_id_2 = user_total_ids[poor_user_index_2]
            user_ids_2 = [poor_user_id_2]
            res = self.ar_con.get_user_info(rich_user_id_1)
            res_data = json.loads(res)
            assert_that(res_data, has_key("coin"), "no coin response...")
            if res_data["coin"] >= 100000:
                assert_that(rich_user_id_2, equal_to(rich_user_id_1), "rich user changed...")
                if poor_user_id_2 != rich_user_id_2:
                    print "第二次获取富豪id是：" + str(rich_user_id_2)
                    print "第二次捕捉非富豪:"
                    self.ar_con.catch_player_list(user_ids_2)
                    print "第三次获取富豪列表："
                    self.sql = ModifySql()
                    self.sql.update_user(user_id, "lottery_type", 105)
                    self.ar_con.gm_reload_user_data(user_id)
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
                    rich_user_index_3 = coins.index(max(coins))
                    rich_user_id_3 = user_total_ids[rich_user_index_3]
                    poor_user_index_3 = coins.index(min(coins))
                    poor_user_id_3 = user_total_ids[poor_user_index_3]
                    user_ids_3 = [poor_user_id_3]
                    res = self.ar_con.get_user_info(rich_user_id_1)
                    res_data = json.loads(res)
                    assert_that(res_data, has_key("coin"), "no coin response...")
                    if res_data["coin"] >= 100000:
                        assert_that(rich_user_id_3, equal_to(rich_user_id_1), "rich user changed...")
                        if poor_user_id_3 != rich_user_id_3:
                            print "第三次获取富豪id是：" + str(rich_user_id_3)
                            print "第三次捕捉非富豪:"
                            self.ar_con.catch_player_list(user_ids_3)
                            print "第四次获取富豪列表："
                            self.sql = ModifySql()
                            self.sql.update_user(user_id, "lottery_type", 105)
                            self.ar_con.gm_reload_user_data(user_id)
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
                            rich_user_index_4 = coins.index(max(coins))
                            rich_user_id_4 = user_total_ids[rich_user_index_4]
                            print "第四次获取富豪id是：" + str(rich_user_id_4)
                            assert_that(rich_user_id_4, not_(rich_user_id_1), "rich user not change...")

    # def test_get_rich_player_list_catch_by_one_user_at_the_same_time(self):
    #     """
    #     获取富豪列表,一个玩家同时只能被一个人抓捕\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     account_id_2 = CoRand.get_rand_int(100001)
    #     account_id_3 = CoRand.get_rand_int(100001)
    #
    #     uc_id_1 = CoRand.get_rand_int()
    #     uc_id_2 = CoRand.get_rand_int()
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     print "玩家2执行操作："
    #     self.ar_con2.login(user_id_2, "im", uc_id_2)
    #     nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con2.modify_info(nick_name_2)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_2, "coin", 100)
    #     self.ar_con2.gm_reload_user_data(user_id_2)
    #     print "玩家1执行操作："
    #     self.ar_con.login(user_id_1, "im", uc_id_1)
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     self.ar_con.add_friend(user_id_2)
    #     print "玩家2执行操作："
    #     self.ar_con2.get_rev()
    #     self.ar_con2.deal_add_friend(user_id_1, 1)
    #     print "玩家1执行操作："
    #     self.ar_con.get_rev()
    #     user_ids = []
    #     for i in range(0, 10):
    #         self.sql = ModifySql()
    #         self.sql.update_user(user_id_1, "lottery_type", 105)
    #         self.ar_con.gm_reload_user_data(user_id_1)
    #         res = self.ar_con.get_rich_player_list()
    #         res_data = json.loads(res)
    #         for j in res_data:
    #             assert_that(j, has_key("user_id"), "no user_id response...")
    #             user_ids.append(j["user_id"])
    #     print user_ids
    #     assert user_id_2 not in user_ids


if __name__ == "__main__":
    unittest.main()
    # # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(GetRichPlayerListTest("test_get_rich_player_list_friend_rich"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
