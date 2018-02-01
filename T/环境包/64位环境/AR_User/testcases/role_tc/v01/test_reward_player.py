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


class RewardPlayerTest(unittest.TestCase):
    def setUp(self):
        print 'start run RewardPlayer test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "rewardPlayer"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'RewardPlayer test complete.....close socket'

    def test_give_reward_when_first_login(self):
        """
        悬赏--获取途径：首次登陆获得一个普通悬赏令一个高级悬赏令\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("reward_normal"), "no reward_normal response...")
        assert_that(res_data["reward_normal"], equal_to(1), "reward_normal mismatching...")
        assert_that(res_data, has_key("reward_advance"), "no reward_advance response...")
        assert_that(res_data["reward_advance"], equal_to(1), "reward_advance mismatching...")

    def test_give_reward_when_pet_complete(self):
        """
        悬赏--获取途径：完成一只养成宠，获得一个普通悬赏令\
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
        self.sql.update_user(user_id, "coin", 100000000)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = 1
        while part != 6:
            for i in range(0, 5):
                if part == 5 and i == 4:
                    pass
                else:
                    self.ar_con.upgrade_pet_part(part)
            part += 1
        res = self.ar_con.upgrade_pet_part(5)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_normal"), "no reward_normal response...")
        assert_that(res_data["reward_normal"], equal_to(2), "reward_normal mismatching...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("reward_normal"), "no reward_normal response...")
        assert_that(res_data["reward_normal"], equal_to(2), "reward_normal mismatching...")
        assert_that(res_data, has_key("reward_advance"), "no reward_advance response...")
        assert_that(res_data["reward_advance"], equal_to(1), "reward_advance mismatching...")

    def test_reward_player_no_shield(self):
        """
        悬赏--被悬赏者无护盾，发布悬赏玩家好友攻击被悬赏者，验证攻击额外奖励\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "好友玩家收到消息："
        self.ar_con2.get_rev()

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.evil_rank_list(0)

        print "好友玩家收到消息："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con2.attack_pet(part_3, user_id_3, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before+600000), "response reward_coin mismatch...")

    def test_reward_player_has_shield(self):
        """
        悬赏--被悬赏者有护盾，发布悬赏玩家好友攻击被悬赏者，验证攻击额外奖励30w\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "好友玩家收到消息："
        self.ar_con2.get_rev()

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "shield", 1)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.evil_rank_list(0)

        print "好友玩家收到消息："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con2.attack_pet(part_3, user_id_3, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(100000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before + 400000), "response reward_coin mismatch...")

    def test_reward_player_friend_attack_more_than_one(self):
        """
        悬赏--悬赏者好友第二次攻击，获得额外奖励\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建悬赏令使用者："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "好友玩家收到消息："
        self.ar_con2.get_rev()

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.evil_rank_list(0)

        print "好友玩家第一次攻击被悬赏者："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con2.attack_pet(part_3, user_id_3, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before+600000), "response reward_coin mismatch...")

        print "好友玩家第二次攻击被悬赏者："
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con2.attack_pet(part_3, user_id_3, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before + 600000), "response reward_coin mismatch...")

    def test_reward_player_normal_5_friend(self):
        """
        悬赏--普通悬赏令，限制5个被悬赏玩家好友获得额外奖励\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        number = 1
        while number < 6:
            print "创建好友玩家"+str(number)+":"
            locals()['account_id_' + str(number)] = CoRand.get_rand_int(100001)
            locals()['uc_id_' + str(number)] = CoRand.get_rand_int()
            locals()['self.ar_con' + str(number)] = ARControl()
            locals()['self.ar_con' + str(number)].connect_server()
            res = locals()['self.ar_con' + str(number)].login(locals()['account_id_' + str(number)], "im",
                                                              locals()['uc_id_' + str(number)], )
            res_data = json.loads(res)
            locals()['user_id_' + str(number)] = res_data["user_id"]
            locals()['nick_name_' + str(number)] = CoRand.get_random_word_filter_sensitive(6)
            locals()['self.ar_con' + str(number)].modify_info(locals()['nick_name_' + str(number)])
            locals()['self.ar_con' + str(number)].add_friend(user_id)
            print "悬赏令使用者同意添加好友"+str(number)+":"
            self.ar_con.get_rev()
            self.ar_con.deal_add_friend(locals()['user_id_'+str(number)], 1)
            print "好友玩家"+str(number)+"收到消息："
            locals()['self.ar_con' + str(number)].get_rev()
            number += 1
        print "创建好友玩家6："
        account_id_6 = CoRand.get_rand_int(100001)
        uc_id_6 = CoRand.get_rand_int()
        self.ar_con6 = ARControl()
        self.ar_con6.connect_server()
        res = self.ar_con6.login(account_id_6, "im", uc_id_6)
        res_data = json.loads(res)
        user_id_6 = res_data["user_id"]
        nick_name_6 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con6.modify_info(nick_name_6)
        self.ar_con6.add_friend(user_id)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_6, 1)
        print "好友玩家6收到消息："
        self.ar_con6.get_rev()

        print "创建攻击者玩家："
        account_id_attack = CoRand.get_rand_int(100001)
        uc_id_attack = CoRand.get_rand_int()
        self.ar_con20 = ARControl()
        self.ar_con20.connect_server()
        res = self.ar_con20.login(account_id_attack, "im", uc_id_attack)
        res_data = json.loads(res)
        user_id_attack = res_data["user_id"]
        nick_name_20 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con20.modify_info(nick_name_20)
        res = self.ar_con20.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_attack_user = res_data["item_id"]
        self.ar_con20.capture_pet(item_id_attack_user)
        self.ar_con20.set_cultivate_pet(item_id_attack_user)
        part_1 = 1
        for i in range(1, 6):
            self.ar_con20.upgrade_pet_part(i)
            self.ar_con20.upgrade_pet_part(i)
            locals()['part_' + str(i)] = i
        self.sql = ModifySql()
        self.sql.update_user(user_id_attack, "guidance", 131071)
        self.ar_con20.gm_reload_user_data(user_id_attack)
        self.sql = ModifySql()
        self.sql.update_user(user_id_attack, "lottery_type", 104)
        self.ar_con20.gm_reload_user_data(user_id_attack)
        self.ar_con20.attack_pet(part, user_id)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        self.ar_con.evil_rank_list(1)
        self.ar_con.reward_player(0, user_id_attack)
        self.ar_con.evil_rank_list(0)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]

        number = 1
        while number < 6:
            print "好友玩家"+str(number)+"收到消息："
            locals()['self.ar_con' + str(number)].get_rev()
            self.sql = ModifySql()
            self.sql.update_user(locals()['user_id_' + str(number)], "guidance", 131071)
            locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_' + str(number)])
            self.sql = ModifySql()
            self.sql.update_user(locals()['user_id_'+str(number)], "lottery_type", 104)
            locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_'+str(number)])
            res = locals()['self.ar_con' + str(number)].attack_pet(locals()['part_'+str(number)], user_id_attack,
                                                                   reward_id)
            res_data = json.loads(res)
            assert_that(res_data, has_key("win_coin"), "no win_coin response...")
            assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
            assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
            assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
            number += 1
        print "好友玩家6收到消息："
        self.ar_con6.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_6, "guidance", 131071)
        self.ar_con6.gm_reload_user_data(user_id_6)
        self.sql = ModifySql()
        self.sql.update_user(user_id_6, "lottery_type", 104)
        self.ar_con6.gm_reload_user_data(user_id_6)
        res = self.ar_con6.attack_pet(part_1, user_id_attack, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(0), "response reward_coin mismatch...")

    def test_reward_player_advance_10_friend(self):
        """
        悬赏--高级悬赏令，限制10个被悬赏玩家好友获得额外奖励\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        number = 1
        while number < 11:
            print "创建好友玩家"+str(number)+":"
            locals()['account_id_' + str(number)] = CoRand.get_rand_int(100001)
            locals()['uc_id_' + str(number)] = CoRand.get_rand_int()
            locals()['self.ar_con' + str(number)] = ARControl()
            locals()['self.ar_con' + str(number)].connect_server()
            res = locals()['self.ar_con' + str(number)].login(locals()['account_id_' + str(number)], "im",
                                                              locals()['uc_id_' + str(number)], )
            res_data = json.loads(res)
            locals()['user_id_' + str(number)] = res_data["user_id"]
            locals()['nick_name_' + str(number)] = CoRand.get_random_word_filter_sensitive(6)
            locals()['self.ar_con' + str(number)].modify_info(locals()['nick_name_' + str(number)])
            locals()['self.ar_con' + str(number)].add_friend(user_id)
            print "悬赏令使用者同意添加好友"+str(number)+":"
            self.ar_con.get_rev()
            self.ar_con.deal_add_friend(locals()['user_id_'+str(number)], 1)
            print "好友玩家"+str(number)+"收到消息："
            locals()['self.ar_con' + str(number)].get_rev()
            number += 1
        print "创建好友玩家11："
        account_id_11 = CoRand.get_rand_int(100001)
        uc_id_11 = CoRand.get_rand_int()
        self.ar_con11 = ARControl()
        self.ar_con11.connect_server()
        res = self.ar_con11.login(account_id_11, "im", uc_id_11)
        res_data = json.loads(res)
        user_id_11 = res_data["user_id"]
        nick_name_11 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con11.modify_info(nick_name_11)
        self.ar_con11.add_friend(user_id)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_11, 1)
        print "好友玩家11收到消息："
        self.ar_con11.get_rev()

        print "创建攻击者玩家,攻击后离线："
        account_id_attack = CoRand.get_rand_int(100001)
        uc_id_attack = CoRand.get_rand_int()
        self.ar_con20 = ARControl()
        self.ar_con20.connect_server()
        res = self.ar_con20.login(account_id_attack, "im", uc_id_attack)
        res_data = json.loads(res)
        user_id_attack = res_data["user_id"]
        nick_name_20 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con20.modify_info(nick_name_20)
        res = self.ar_con20.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_attack_user = res_data["item_id"]
        self.ar_con20.capture_pet(item_id_attack_user)
        self.ar_con20.set_cultivate_pet(item_id_attack_user)
        part_1 = 1
        for i in range(1, 6):
            self.ar_con20.upgrade_pet_part(i)
            self.ar_con20.upgrade_pet_part(i)
            locals()['part_' + str(i)] = i
        self.sql = ModifySql()
        self.sql.update_user(user_id_attack, "guidance", 131071)
        self.ar_con20.gm_reload_user_data(user_id_attack)
        self.sql = ModifySql()
        self.sql.update_user(user_id_attack, "lottery_type", 104)
        self.ar_con20.gm_reload_user_data(user_id_attack)
        self.ar_con20.attack_pet(part, user_id)
        self.ar_con20.close()

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.reward_player(1, user_id_attack)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]

        number = 1
        while number < 11:
            if number < 6:
                print "好友玩家"+str(number)+"收到消息后攻击被悬赏者："
                locals()['self.ar_con' + str(number)].get_rev()
                self.sql = ModifySql()
                self.sql.update_user(locals()['user_id_' + str(number)], "guidance", 131071)
                locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_' + str(number)])
                self.sql = ModifySql()
                self.sql.update_user(locals()['user_id_'+str(number)], "lottery_type", 104)
                locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_'+str(number)])
                res = locals()['self.ar_con' + str(number)].attack_pet(locals()['part_'+str(number)], user_id_attack,
                                                                       reward_id)
                res_data = json.loads(res)
                assert_that(res_data, has_key("win_coin"), "no win_coin response...")
                assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
                assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
                assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
                number += 1
            else:
                print "好友玩家" + str(number) + "收到消息后攻击被悬赏者："
                locals()['self.ar_con' + str(number)].get_rev()
                self.sql = ModifySql()
                self.sql.update_user(locals()['user_id_' + str(number)], "guidance", 131071)
                locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_' + str(number)])
                self.sql = ModifySql()
                self.sql.update_user(locals()['user_id_' + str(number)], "lottery_type", 104)
                locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_' + str(number)])
                res = locals()['self.ar_con' + str(number)].attack_pet(locals()['part_' + str(number-5)],
                                                                       user_id_attack, reward_id)
                res_data = json.loads(res)
                assert_that(res_data, has_key("win_coin"), "no win_coin response...")
                assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
                assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
                assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
                number += 1
        print "攻击者玩家升级部件："
        self.ar_con20.connect_server()
        self.ar_con20.login(account_id_attack, "im", uc_id_attack)
        self.ar_con20.get_unread_msg()
        self.ar_con20.upgrade_pet_part(1)
        print "好友玩家11收到消息后攻击被悬赏者："
        self.ar_con11.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_11, "guidance", 131071)
        self.ar_con11.gm_reload_user_data(user_id_11)
        self.sql = ModifySql()
        self.sql.update_user(user_id_11, "lottery_type", 104)
        self.ar_con11.gm_reload_user_data(user_id_11)
        res = self.ar_con11.attack_pet(part_1, user_id_attack, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(0), "response reward_coin mismatch...")

    def test_reward_player_not_enough(self):
        """
        悬赏--悬赏令不足\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        self.ar_con.close()
        time.sleep(1)

        print "创建攻击者玩家1："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)
        print "创建攻击者玩家2："
        account_id_4 = CoRand.get_rand_int(100001)
        uc_id_4 = CoRand.get_rand_int()
        self.ar_con4 = ARControl()
        self.ar_con4.connect_server()
        res = self.ar_con4.login(account_id_4, "im", uc_id_4)
        res_data = json.loads(res)
        user_id_4 = res_data["user_id"]
        nick_name_4 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con4.modify_info(nick_name_4)
        res = self.ar_con4.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_4 = res_data["item_id"]
        self.ar_con4.capture_pet(item_id_4)
        self.ar_con4.set_cultivate_pet(item_id_4)
        part_4 = CoRand.get_rand_int(1, 5)
        self.ar_con4.upgrade_pet_part(part_4)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "guidance", 131071)
        self.ar_con4.gm_reload_user_data(user_id_4)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "lottery_type", 104)
        self.ar_con4.gm_reload_user_data(user_id_4)
        self.ar_con4.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.connect_server()
        self.ar_con.login(account_id_1, "im", uc_id_1)
        self.ar_con.get_unread_msg()
        self.ar_con.get_enemy_list()
        self.ar_con.evil_rank_list(0)
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.reward_player(0, user_id_4)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ENOUGH_REWARD["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ENOUGH_REWARD["err_msg"]), "response msg mismatching...")

    def test_reward_player_repeat_same(self):
        """
        悬赏--对同一个玩家追加悬赏（追加同种悬赏令)\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        self.ar_con.get_enemy_list()
        print "追加悬赏："
        self.ar_con.pm_set_role_data("rewardNormal", 1)
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        self.ar_con.get_enemy_list()
        res = self.ar_con.get_user_info(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_advance"), "no reward_advance response...")
        assert_that(res_data["reward_advance"], equal_to(1), "response reward_advance mismatch...")
        assert_that(res_data, has_key("reward_normal"), "no reward_advance response...")
        assert_that(res_data["reward_normal"], equal_to(0), "response reward_advance mismatch...")

    def test_reward_player_repeat(self):
        """
        悬赏--对同一个玩家追加悬赏（追加不同种）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        self.ar_con.get_enemy_list()
        print "追加悬赏："
        res = self.ar_con.reward_player(1, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        self.ar_con.get_enemy_list()
        res = self.ar_con.get_user_info(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_advance"), "no reward_advance response...")
        assert_that(res_data["reward_advance"], equal_to(0), "response reward_advance mismatch...")
        assert_that(res_data, has_key("reward_normal"), "no reward_advance response...")
        assert_that(res_data["reward_normal"], equal_to(0), "response reward_advance mismatch...")

    def test_reward_player_failed_reward_num_not_change(self):
        """
        悬赏--悬赏已被其他玩家通缉的玩家，悬赏成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者1登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)

        print "悬赏令使用者2登陆："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        res = self.ar_con2.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_2 = res_data["item_id"]
        self.ar_con2.capture_pet(item_id_2)
        self.ar_con2.set_cultivate_pet(item_id_2)
        part_2 = CoRand.get_rand_int(1, 5)
        self.ar_con2.upgrade_pet_part(part_2)

        print "创建攻击者玩家，攻击玩家1和2："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_2, user_id_2)

        print "悬赏令使用者1通缉攻击者："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        print "悬赏令使用者2通缉攻击者："
        self.ar_con2.get_rev()
        res = self.ar_con2.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_reward_player_not_attacked(self):
        """
        悬赏--悬赏未攻击过自己的玩家\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.reward_player(0, self.account_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_USER_ENEMY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_USER_ENEMY["err_msg"]), "response msg mismatching...")

    def test_reward_player_self(self):
        """
        悬赏--悬赏自己\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.reward_player(0, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_USER_ENEMY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_USER_ENEMY["err_msg"]),
                    "response msg mismatching...")

    def test_reward_player_user_not_exist(self):
        """
        悬赏--悬赏不存在的玩家\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        user_id_not_exist = CoRand.get_rand_int(100001)
        res = self.ar_con.reward_player(0, user_id_not_exist)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_USER_ENEMY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_USER_ENEMY["err_msg"]),
                    "response msg mismatching...")

    def test_reward_player_without_params(self):
        """
        悬赏--请求参数未传\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_reward_player_without_reward_type(self):
        """
        悬赏--reward_type未传\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        json_body = {
            "user_id": self.account_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_reward_player_without_user_id(self):
        """
        悬赏--user_id未传\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        json_body = {
            "reward_type": 0
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]),
                    "response msg mismatching...")

    def test_reward_player_error_reward_type(self):
        """
        悬赏--reward_type值错误\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(791099, "im")
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        reward_type = CoRand.get_rand_int()
        res = self.ar_con.reward_player(reward_type, self.account_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]),
                    "response msg mismatching...")

    def test_reward_player_attack_self(self):
        """
        悬赏--悬赏者自己攻击被悬赏者\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.evil_rank_list(0)

        print "悬赏令使用者自己攻击被悬赏者："
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        res = self.ar_con.get_user_info(user_id_1)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before + 600000), "response reward_coin mismatch...")

    def test_reward_player_reward_friend(self):
        """
        悬赏--悬赏好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建悬赏令使用者A："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家B："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "好友B攻击A："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part_1, user_id_1)

        print "悬赏令使用者A通缉攻击者B："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        res = self.ar_con.reward_player(0, user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["reward_list"][0]["be_reward_user_id"], equal_to(user_id_2),
                    "response be_reward_user_id mismatch...")
        assert_that(res_data["reward_list"][0], has_key("user_id"), "no user_id response...")
        assert_that(res_data["reward_list"][0]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data["reward_list"][0], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_list"][0]["reward_type"], equal_to(0), "response reward_type mismatch...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")

        print "好友玩家查看自己的仇人列表："
        self.ar_con2.get_rev()
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["reward_list"][0]["be_reward_user_id"], equal_to(user_id_2),
                    "response be_reward_user_id mismatch...")
        assert_that(res_data["reward_list"][0], has_key("user_id"), "no user_id response...")
        assert_that(res_data["reward_list"][0]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data["reward_list"][0], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_list"][0]["reward_type"], equal_to(0), "response reward_type mismatch...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")

    def test_reward_player_friend_attack_error_reward_id(self):
        """
        悬赏--悬赏者好友攻击传错误的悬赏令id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "好友玩家收到消息："
        self.ar_con2.get_rev()

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        self.ar_con3.upgrade_pet_part(part_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        self.ar_con.get_enemy_list()

        print "好友玩家收到消息："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        error_reward_id = CoRand.get_rand_int()
        res = self.ar_con2.attack_pet(part_3, user_id_3, error_reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(0), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before+300000), "response reward_coin mismatch...")

    def test_reward_player_many_people(self):
        """
        悬赏--ABC好友关系，A悬赏DE，验证悬赏正确性\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建悬赏令使用者A："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家B："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友B："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        print "好友玩家B收到消息："
        self.ar_con2.get_rev()

        print "创建好友玩家C："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        self.ar_con3.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友C："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_3, 1)
        print "好友玩家C收到消息："
        self.ar_con3.get_rev()

        print "创建攻击者玩家D："
        account_id_4 = CoRand.get_rand_int(100001)
        uc_id_4 = CoRand.get_rand_int()
        self.ar_con4 = ARControl()
        self.ar_con4.connect_server()
        res = self.ar_con4.login(account_id_4, "im", uc_id_4)
        res_data = json.loads(res)
        user_id_4 = res_data["user_id"]
        nick_name_4 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con4.modify_info(nick_name_4)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "guidance", 131071)
        self.ar_con4.gm_reload_user_data(user_id_4)
        res = self.ar_con4.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_4 = res_data["item_id"]
        self.ar_con4.capture_pet(item_id_4)
        self.ar_con4.set_cultivate_pet(item_id_4)
        self.ar_con4.upgrade_pet_part(1)
        self.ar_con4.upgrade_pet_part(2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "lottery_type", 104)
        self.ar_con4.gm_reload_user_data(user_id_4)
        self.ar_con4.attack_pet(part_1, user_id_1)
        print "创建攻击者玩家E："
        account_id_5 = CoRand.get_rand_int(100001)
        uc_id_5 = CoRand.get_rand_int()
        self.ar_con5 = ARControl()
        self.ar_con5.connect_server()
        res = self.ar_con5.login(account_id_5, "im", uc_id_5)
        res_data = json.loads(res)
        user_id_5 = res_data["user_id"]
        nick_name_5 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con5.modify_info(nick_name_5)
        self.sql = ModifySql()
        self.sql.update_user(user_id_5, "guidance", 131071)
        self.ar_con5.gm_reload_user_data(user_id_5)
        res = self.ar_con5.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_5 = res_data["item_id"]
        self.ar_con5.capture_pet(item_id_5)
        self.ar_con5.set_cultivate_pet(item_id_5)
        part_5 = CoRand.get_rand_int(1, 5)
        self.ar_con5.upgrade_pet_part(part_5)
        self.sql = ModifySql()
        self.sql.update_user(user_id_5, "lottery_type", 104)
        self.ar_con5.gm_reload_user_data(user_id_5)
        self.ar_con5.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者D、E："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_4)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.reward_player(1, user_id_5)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        be_reward_user_ids = []
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        for i in res_data["reward_list"]:
            assert_that(i, has_key("be_reward_user_id"), "no be_reward_user_id response...")
            be_reward_user_ids.append(i["be_reward_user_id"])
        assert user_id_4 in be_reward_user_ids, "攻击玩家D不在悬赏列表"
        d_index = be_reward_user_ids.index(user_id_4)
        reward_id_d = res_data["reward_list"][d_index]["reward_id"]
        assert user_id_5 in be_reward_user_ids, "攻击玩家E不在悬赏列表"
        e_index = be_reward_user_ids.index(user_id_5)
        reward_id_e = res_data["reward_list"][e_index]["reward_id"]

        print "A、B、C攻击D:"
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        res = self.ar_con.attack_pet(1, user_id_4, reward_id_d)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")

        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(1, user_id_4, reward_id_d)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")

        self.ar_con3.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        res = self.ar_con3.attack_pet(2, user_id_4, reward_id_d)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")

        print "B、C攻击E："
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part_5, user_id_5, reward_id_e)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")

        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        res = self.ar_con3.attack_pet(part_5, user_id_5, reward_id_e)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")

    # def test_reward_player_normal_time_limit(self):
    #     """
    #     悬赏--普通悬赏令，第二天晚上00:00后失效\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     print "悬赏令使用者登陆："
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     uc_id_1 = CoRand.get_rand_int()
    #     res = self.ar_con.login(account_id_1, "im", uc_id_1)
    #     res_data = json.loads(res)
    #     user_id_1 = res_data["user_id"]
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     res = self.ar_con.match_pet(self.pet_url)
    #     res_data = json.loads(res)
    #     item_id_1 = res_data["item_id"]
    #     self.ar_con.capture_pet(item_id_1)
    #     self.ar_con.set_cultivate_pet(item_id_1)
    #     part_1 = CoRand.get_rand_int(1, 5)
    #     self.ar_con.upgrade_pet_part(part_1)
    #     print "创建好友玩家："
    #     account_id_2 = CoRand.get_rand_int(100001)
    #     uc_id_2 = CoRand.get_rand_int()
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     res = self.ar_con2.login(account_id_2, "im", uc_id_2)
    #     res_data = json.loads(res)
    #     user_id_2 = res_data["user_id"]
    #     nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con2.modify_info(nick_name_2)
    #     self.ar_con2.add_friend(user_id_1)
    #     print "悬赏令使用者同意添加好友："
    #     self.ar_con.get_rev()
    #     self.ar_con.deal_add_friend(user_id_2, 1)
    #
    #     print "好友玩家收到消息："
    #     self.ar_con2.get_rev()
    #
    #     print "创建攻击者玩家："
    #     account_id_3 = CoRand.get_rand_int(100001)
    #     uc_id_3 = CoRand.get_rand_int()
    #     self.ar_con3 = ARControl()
    #     self.ar_con3.connect_server()
    #     res = self.ar_con3.login(account_id_3, "im", uc_id_3)
    #     res_data = json.loads(res)
    #     user_id_3 = res_data["user_id"]
    #     nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con3.modify_info(nick_name_3)
    #     res = self.ar_con3.match_pet(self.pet_url)
    #     res_data = json.loads(res)
    #     item_id_3 = res_data["item_id"]
    #     self.ar_con3.capture_pet(item_id_3)
    #     self.ar_con3.set_cultivate_pet(item_id_3)
    #     part_3 = CoRand.get_rand_int(1, 5)
    #     self.ar_con3.upgrade_pet_part(part_3)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_3, "guidance", 131071)
    #     self.ar_con3.gm_reload_user_data(user_id_3)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_3, "lottery_type", 104)
    #     self.ar_con3.gm_reload_user_data(user_id_3)
    #     self.ar_con3.attack_pet(part_1, user_id_1)
    #
    #     print "悬赏令使用者通缉攻击者："
    #     self.ar_con.get_rev()
    #     self.ar_con.get_enemy_list()
    #     res = self.ar_con.reward_player(0, user_id_3)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
    #
    #     res = self.ar_con.get_enemy_list()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("reward_list"), "no reward_list response...")
    #     assert_that(res_data["reward_list"][0], has_key("id"), "no id response...")
    #     reward_id = res_data["reward_list"][0]["id"]
    #     self.ar_con.evil_rank_list(0)
    #
    #     print "好友玩家收到消息："
    #     self.ar_con2.get_rev()
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_2, "guidance", 131071)
    #     self.ar_con2.gm_reload_user_data(user_id_2)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_2, "lottery_type", 104)
    #     self.ar_con2.gm_reload_user_data(user_id_2)
    #     # time.sleep(17280)
    #     # res = self.ar_con2.get_user_info(user_id_2)
    #     # res_data = json.loads(res)
    #     # coin_before = res_data["coin"]
    #     # res = self.ar_con2.attack_pet(part_3, user_id_3, reward_id)
    #     # res_data = json.loads(res)
    #     # assert_that(res_data, has_key("win_coin"), "no win_coin response...")
    #     # assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
    #     # assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
    #     # assert_that(res_data["reward_coin"], equal_to(0), "response reward_coin mismatch...")
    #     # assert_that(res_data, has_key("coin"), "no coin response...")
    #     # assert_that(res_data["coin"], equal_to(coin_before + 300000), "response reward_coin mismatch...")
    #
    # def test_reward_player_advance_time_limit(self):
    #     """
    #     悬赏--高级悬赏令，第二天晚上00:00后失效\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     print "悬赏令使用者登陆："
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     uc_id_1 = CoRand.get_rand_int()
    #     res = self.ar_con.login(account_id_1, "im", uc_id_1)
    #     res_data = json.loads(res)
    #     user_id_1 = res_data["user_id"]
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     res = self.ar_con.match_pet(self.pet_url)
    #     res_data = json.loads(res)
    #     item_id_1 = res_data["item_id"]
    #     self.ar_con.capture_pet(item_id_1)
    #     self.ar_con.set_cultivate_pet(item_id_1)
    #     part_1 = CoRand.get_rand_int(1, 5)
    #     self.ar_con.upgrade_pet_part(part_1)
    #     print "创建好友玩家："
    #     account_id_2 = CoRand.get_rand_int(100001)
    #     uc_id_2 = CoRand.get_rand_int()
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     res = self.ar_con2.login(account_id_2, "im", uc_id_2)
    #     res_data = json.loads(res)
    #     user_id_2 = res_data["user_id"]
    #     nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con2.modify_info(nick_name_2)
    #     self.ar_con2.add_friend(user_id_1)
    #     print "悬赏令使用者同意添加好友："
    #     self.ar_con.get_rev()
    #     self.ar_con.deal_add_friend(user_id_2, 1)
    #
    #     print "好友玩家收到消息："
    #     self.ar_con2.get_rev()
    #
    #     print "创建攻击者玩家："
    #     account_id_3 = CoRand.get_rand_int(100001)
    #     uc_id_3 = CoRand.get_rand_int()
    #     self.ar_con3 = ARControl()
    #     self.ar_con3.connect_server()
    #     res = self.ar_con3.login(account_id_3, "im", uc_id_3)
    #     res_data = json.loads(res)
    #     user_id_3 = res_data["user_id"]
    #     nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con3.modify_info(nick_name_3)
    #     res = self.ar_con3.match_pet(self.pet_url)
    #     res_data = json.loads(res)
    #     item_id_3 = res_data["item_id"]
    #     self.ar_con3.capture_pet(item_id_3)
    #     self.ar_con3.set_cultivate_pet(item_id_3)
    #     part_3 = CoRand.get_rand_int(1, 5)
    #     self.ar_con3.upgrade_pet_part(part_3)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_3, "guidance", 131071)
    #     self.ar_con3.gm_reload_user_data(user_id_3)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_3, "lottery_type", 104)
    #     self.ar_con3.gm_reload_user_data(user_id_3)
    #     self.ar_con3.attack_pet(part_1, user_id_1)
    #
    #     print "悬赏令使用者通缉攻击者："
    #     self.ar_con.get_rev()
    #     self.ar_con.get_enemy_list()
    #     res = self.ar_con.reward_player(1, user_id_3)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
    #
    #     res = self.ar_con.get_enemy_list()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("reward_list"), "no reward_list response...")
    #     assert_that(res_data["reward_list"][0], has_key("id"), "no id response...")
    #     reward_id = res_data["reward_list"][0]["id"]
    #     self.ar_con.evil_rank_list(0)
    #
    #     print "好友玩家收到消息："
    #     self.ar_con2.get_rev()
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_2, "guidance", 131071)
    #     self.ar_con2.gm_reload_user_data(user_id_2)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_2, "lottery_type", 104)
    #     self.ar_con2.gm_reload_user_data(user_id_2)
    #     # time.sleep(17280)
    #     # res = self.ar_con2.get_user_info(user_id_2)
    #     # res_data = json.loads(res)
    #     # coin_before = res_data["coin"]
    #     # res = self.ar_con2.attack_pet(part_3, user_id_3, reward_id)
    #     # res_data = json.loads(res)
    #     # assert_that(res_data, has_key("win_coin"), "no win_coin response...")
    #     # assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
    #     # assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
    #     # assert_that(res_data["reward_coin"], equal_to(0), "response reward_coin mismatch...")
    #     # assert_that(res_data, has_key("coin"), "no coin response...")
    #     # assert_that(res_data["coin"], equal_to(coin_before + 300000), "response reward_coin mismatch...")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(RewardPlayerTest("test_reward_player_many_people"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
