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


class SetGuidanceTest(unittest.TestCase):
    def setUp(self):
        print 'start run SetGuidance test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "setGuidance"
        self.account_id = 100861

    def tearDown(self):
        print 'SetGuidance test complete.....close socket'

    def test_set_newer_code_success(self):
        """
        设置新手引导数据--验证数值设置成功\
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
        newer_code = CoRand.get_rand_int(1, 10000)
        res = self.ar_con.set_newer_code(newer_code)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("newer_code"), "no newer_code response...")
        assert_that(res_data["newer_code"], equal_to(newer_code), "response newer_code mismatching...")

    def test_set_newer_code_data_0(self):
        """
        设置新手引导数据--设置newer_code为0\
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
        newer_code = 0
        res = self.ar_con.set_newer_code(newer_code)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("newer_code"), "no newer_code response...")
        assert_that(res_data["newer_code"], equal_to(newer_code), "response newer_code mismatching...")

    def test_set_newer_code_data_negative(self):
        """
        设置新手引导数据--设置newer_code为负数\
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
        newer_code = -5
        res = self.ar_con.set_newer_code(newer_code)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("newer_code"), "no newer_code response...")
        assert_that(res_data["newer_code"], equal_to(newer_code), "response newer_code mismatching...")

    # def test_guidance_match_pet_first_cultivate_pet(self):
    #     """
    #     新手引导--首次扫描必出养成宠/
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     account_id = CoRand.get_rand_int(100001)
    #     uc_id = CoRand.get_rand_int()
    #     res = self.ar_con.login(account_id, "im", uc_id)
    #     res_data = json.loads(res)
    #     user_id = res_data["user_id"]
    #     nick_name = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name)
    #     url = "http://192.168.239.119:807/ARTest/glass_true/1.jpg"
    #     res = self.ar_con.match_pet(url)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("type"), "no type response...")
    #     assert res_data["type"] <= 200

    # def test_guidance_draw_lottery(self):
    #     """
    #     新手引导--抽奖/
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     account_id = CoRand.get_rand_int(100001)
    #     uc_id = CoRand.get_rand_int()
    #     res = self.ar_con.login(account_id, "im", uc_id)
    #     res_data = json.loads(res)
    #     user_id = res_data["user_id"]
    #     nick_name = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name)
    #     print "第1次抽奖获得攻击："
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 104
    #     res = self.ar_con.get_rand_friend_info()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("user_id"), "no user_id response...")
    #     assert res_data["user_id"] <= 100000
    #     user_id_attacked = res_data["user_id"]
    #     res = self.ar_con.attack_pet(1, user_id_attacked)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("win_coin"), "no win_coin response...")
    #     assert_that(res_data["win_coin"], equal_to(300000))
    #     print "第2次抽奖获得护盾："
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 103
    #     print "第3-6次抽奖获得不同金额金币："
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 101
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 101
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 101
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 101
    #     print "第7次抽奖获得最高额度金币："
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 101
    #     assert_that(res_data, has_key("count"), "no count response...")
    #     assert res_data["count"] == 100000
    #     print "第8次抽奖获得偷窃卡,必抽中富豪："
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 105
    #     res = self.ar_con.get_rich_player_list()
    #     res_data = json.loads(res)
    #     for i in res_data:
    #         assert_that(i, has_key("user_id"), "no user_id response...")
    #
    #     print "随机抓取一个玩家："
    #     j = CoRand.get_rand_int(0, 3)
    #     print j
    #     user_id_rand = res_data[j]["user_id"]
    #     res = self.ar_con.get_user_info(user_id_rand)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("coin"), "no coin response...")
    #     coin_before = res_data["coin"]
    #     user_ids = [user_id_rand]
    #     self.ar_con.catch_player_list(user_ids)
    #     res = self.ar_con.get_user_info(user_id_rand)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("coin"), "no coin response...")
    #     coin_after = res_data["coin"]
    #     assert coin_before == coin_after
    #
    #     print "第9次抽奖获得扫描卡："
    #     res = self.ar_con.draw_lottery()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("item"), "no item response...")
    #     assert res_data["item"] == 106
    #
    #     for i in range(0, 50):
    #         res = self.ar_con.draw_lottery()
    #         res_data = json.loads(res)
    #         assert_that(res_data, has_key("pp"), "no pp response...")
    #         pp = res_data["pp"]
    #         if pp <= 26:
    #             print "玩家首次体力值小于25,抽奖获得体力："
    #             res = self.ar_con.draw_lottery()
    #             res_data = json.loads(res)
    #             assert_that(res_data, has_key("item"), "no item response...")
    #             assert res_data["item"] == 102
    #             break
    #

if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(SetGuidanceTest("test_guidance_match_pet_first_cultivate_pet"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
