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


class GetRewardAttackTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetRewardAttack test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getRewardAttack"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'GetRewardAttack test complete.....close socket'

    def test_get_reward_attack_be_rewarded_user_not_be_attacked(self):
        """
        获取悬赏令攻击信息:被悬赏者未被攻击\
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
        self.ar_con.reward_player(0, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)
        assert res_data == []

    def test_get_reward_attack_be_rewarded_user_no_shield(self):
        """
        获取悬赏令攻击信息:被悬赏者无护盾,造成被悬赏者部件破损\
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
        res = self.ar_con3.get_user_info(user_id_3)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        res = self.ar_con3.upgrade_pet_part(part_3)
        res_data = json.loads(res)
        coin_after = res_data["coin"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.reward_player(0, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)
        assert res_data == []
        print "悬赏令使用者自己攻击被悬赏者："
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        self.ar_con.get_rev()
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)

        assert_that(res_data[0], has_key("attack_time"), "no attack_time response...")

        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data[0], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[0]["nick_name"], equal_to(nick_name_1), "response nick_name mismatch...")
        assert_that(res_data[0], has_key("toll"), "no toll response...")
        assert_that(res_data[0]["toll"], equal_to(int((coin_before-coin_after)*0.5)), "response toll mismatch...")

    def test_get_reward_attack_be_rewarded_user_no_shield_destroy(self):
        """
        获取悬赏令攻击信息:被悬赏者无护盾,造成被悬赏者部件损毁\
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
        res = self.ar_con3.get_user_info(user_id_3)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        res = self.ar_con3.upgrade_pet_part(part_3)
        res_data = json.loads(res)
        coin_level_1 = coin_before - res_data["coin"]
        res = self.ar_con3.upgrade_pet_part(part_3)
        res_data = json.loads(res)
        coin_level_2 = coin_before - res_data["coin"] - coin_level_1
        print coin_level_1, coin_level_2
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.reward_player(0, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)
        assert res_data == []
        print "悬赏令使用者自己摧毁被悬赏者部件，查看悬赏令攻击信息："
        self.ar_con.pm_set_role_data("lotteryType", 104)
        self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        self.ar_con.get_rev()
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)

        assert_that(res_data[0], has_key("attack_time"), "no attack_time response...")
        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data[0], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[0]["nick_name"], equal_to(nick_name_1), "response nick_name mismatch...")
        assert_that(res_data[0], has_key("toll"), "no toll response...")
        assert_that(res_data[0]["toll"], equal_to(int(coin_level_2*0.5)), "response toll mismatch...")

        self.ar_con.pm_set_role_data("lotteryType", 104)
        self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        self.ar_con.get_rev()
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)

        assert_that(res_data[1], has_key("attack_time"), "no attack_time response...")
        assert_that(res_data[1], has_key("user_id"), "no user_id response...")
        assert_that(res_data[1]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data[1], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[1]["nick_name"], equal_to(nick_name_1), "response nick_name mismatch...")
        assert_that(res_data[1], has_key("toll"), "no toll response...")
        assert_that(res_data[1]["toll"], equal_to(int(coin_level_2 * 0.5)+coin_level_1), "response toll mismatch...")

    def test_get_reward_attack_be_rewarded_user_has_shield(self):
        """
        获取悬赏令攻击信息:被悬赏者有护盾\
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

        print "创建攻击者玩家，升级部件，获得攻击卡和护盾卡："
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
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "shield", 1)
        self.ar_con3.gm_reload_user_data(user_id_3)

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.reward_player(0, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)
        assert res_data == []
        print "悬赏令使用者自己攻击被悬赏者："
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        self.ar_con.get_rev()
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)

        assert_that(res_data[0], has_key("attack_time"), "no attack_time response...")
        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data[0], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[0]["nick_name"], equal_to(nick_name_1), "response nick_name mismatch...")
        assert_that(res_data[0], has_key("toll"), "no toll response...")
        assert_that(res_data[0]["toll"], equal_to(0), "response toll mismatch...")

    def test_get_reward_attack_normal_5_friend(self):
        """
        获取悬赏令攻击信息:普通悬赏令，超过5个玩家攻击，验证攻击信息列表\
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
        self.ar_con.close()

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
        print "悬赏令发布者获取悬赏令攻击信息："
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        self.ar_con.get_unread_msg()
        res = self.ar_con.get_reward_attack(reward_id, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_length(5), "response length mismatch...")
        res = self.ar_con.get_reward_attack(reward_id, 2)
        res_data = json.loads(res)
        assert res_data == [], "response mismatch..."

    def test_get_reward_attack_others(self):
        """
        获取悬赏令攻击信息:获取其他玩家悬赏令攻击信息\
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

        print "悬赏令使用者通缉攻击者,并攻击："
        self.ar_con.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.reward_player(1, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        self.ar_con.get_rev()

        print "创建其他玩家："
        account_id_4 = CoRand.get_rand_int(100001)
        uc_id_4 = CoRand.get_rand_int()
        self.ar_con4 = ARControl()
        self.ar_con4.connect_server()
        res = self.ar_con4.login(account_id_4, "im", uc_id_4)
        res_data = json.loads(res)
        user_id_4 = res_data["user_id"]
        nick_name_4 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con4.modify_info(nick_name_4)
        res = self.ar_con4.get_reward_attack(reward_id)
        res_data = json.loads(res)
        assert_that(res_data[0], has_key("attack_time"), "no attack_time response...")
        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data[0], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[0]["nick_name"], equal_to(nick_name_1), "response nick_name mismatch...")
        assert_that(res_data[0], has_key("toll"), "no toll response...")

    def test_get_reward_attack_error_reward_id(self):
        """
        获取悬赏令攻击信息:错误的reward_id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        reward_id = CoRand.get_rand_int()
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)
        assert res_data == []

    def test_get_reward_attack_without_params(self):
        """
        获取悬赏令攻击信息:未传参数\
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

    def test_get_reward_attack_add_reward(self):
        """
        获取追加悬赏令攻击信息,超过五个好友攻击\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        number = 1
        while number < 6:
            print "创建好友玩家" + str(number) + ":"
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
            print "悬赏令使用者同意添加好友" + str(number) + ":"
            self.ar_con.get_rev()
            self.ar_con.deal_add_friend(locals()['user_id_' + str(number)], 1)
            print "好友玩家" + str(number) + "收到消息："
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
        nick_name_attack = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con20.modify_info(nick_name_attack)
        res = self.ar_con20.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_attack = res_data["item_id"]
        self.ar_con20.capture_pet(item_id_attack)
        self.ar_con20.set_cultivate_pet(item_id_attack)
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

        print "悬赏令使用者使用普通通缉令通缉攻击者："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_attack)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        self.ar_con.get_enemy_list()
        print "追加高级悬赏令："
        self.ar_con.reward_player(1, user_id_attack)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.close()

        number = 1
        while number < 6:
            print "好友玩家" + str(number) + "收到消息："
            locals()['self.ar_con' + str(number)].get_rev()
            self.sql = ModifySql()
            self.sql.update_user(locals()['user_id_' + str(number)], "guidance", 131071)
            locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_' + str(number)])
            self.sql = ModifySql()
            self.sql.update_user(locals()['user_id_' + str(number)], "lottery_type", 104)
            locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_' + str(number)])
            res = locals()['self.ar_con' + str(number)].attack_pet(locals()['part_' + str(number)], user_id_attack,
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
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        print "悬赏令发布者获取悬赏令攻击信息："
        self.ar_con.connect_server()
        self.ar_con.login(account_id, "im", uc_id)
        self.ar_con.get_unread_msg()
        res = self.ar_con.get_reward_attack(reward_id, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_length(6), "response length mismatch...")
        res = self.ar_con.get_reward_attack(reward_id, 2)
        res_data = json.loads(res)
        assert res_data == [], "response mismatch..."

    def test_get_reward_attack_add_reward_attack(self):
        """
        获取追加悬赏令攻击信息,包含追加前和追加后的攻击信息\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者A登陆："
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
        print "A同意添加好友B："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "B收到消息："
        self.ar_con2.get_rev()
        print "创建好友玩家D："
        account_id_4 = CoRand.get_rand_int(100001)
        uc_id_4 = CoRand.get_rand_int()
        self.ar_con4 = ARControl()
        self.ar_con4.connect_server()
        res = self.ar_con4.login(account_id_4, "im", uc_id_4)
        res_data = json.loads(res)
        user_id_4 = res_data["user_id"]
        nick_name_4 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con4.modify_info(nick_name_4)
        self.ar_con4.add_friend(user_id_1)
        print "A同意添加好友D："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_4, 1)

        print "D收到消息："
        self.ar_con4.get_rev()

        print "创建攻击者玩家C："
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

        print "A使用普通通缉令通缉C："
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
        print "好友玩家B收到消息，攻击被悬赏者C："
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
        assert_that(res_data["coin"], equal_to(coin_before + 600000), "response reward_coin mismatch...")
        print"A获取悬赏令信息："
        time.sleep(1)
        self.ar_con.get_rev()
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)

        assert_that(res_data[0], has_key("attack_time"), "no attack_time response...")
        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data[0], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[0]["nick_name"], equal_to(nick_name_2), "response nick_name mismatch...")
        assert_that(res_data[0], has_key("toll"), "no toll response...")

        print "A追加高级悬赏令："
        self.ar_con.reward_player(1, user_id_3)
        print "好友玩家D收到消息，攻击被悬赏者C："
        self.ar_con4.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "guidance", 131071)
        self.ar_con4.gm_reload_user_data(user_id_4)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "lottery_type", 104)
        self.ar_con4.gm_reload_user_data(user_id_4)
        res = self.ar_con4.attack_pet(part_3, user_id_3, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")

        self.ar_con.get_rev()
        print"获取悬赏令信息："
        time.sleep(1)
        res = self.ar_con.get_reward_attack(reward_id)
        res_data = json.loads(res)

        assert_that(res_data[0], has_key("attack_time"), "no attack_time response...")
        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data[0], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[0]["nick_name"], equal_to(nick_name_2), "response nick_name mismatch...")
        assert_that(res_data[0], has_key("toll"), "no toll response...")
        assert_that(res_data[1], has_key("attack_time"), "no attack_time response...")
        assert_that(res_data[1], has_key("user_id"), "no user_id response...")
        assert_that(res_data[1]["user_id"], equal_to(user_id_4), "response user_id mismatch...")
        assert_that(res_data[1], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[1]["nick_name"], equal_to(nick_name_4), "response nick_name mismatch...")
        assert_that(res_data[1], has_key("toll"), "no toll response...")

    # def test_get_reward_attack_more_than_50_date(self):
    #     """
    #     获取悬赏令攻击信息--超过50条数据，验证page功能\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     print "悬赏令使用者登陆："
    #     account_id = CoRand.get_rand_int(100001)
    #     uc_id = CoRand.get_rand_int()
    #     res = self.ar_con.login(account_id, "im", uc_id)
    #     res_data = json.loads(res)
    #     user_id = res_data["user_id"]
    #     nick_name = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name)
    #     res = self.ar_con.match_pet(self.pet_url)
    #     res_data = json.loads(res)
    #     item_id = res_data["item_id"]
    #     self.ar_con.capture_pet(item_id)
    #     self.ar_con.set_cultivate_pet(item_id)
    #     part = CoRand.get_rand_int(1, 5)
    #     self.ar_con.upgrade_pet_part(part)
    #     number = 1
    #     while number < 26:
    #         print "创建好友玩家" + str(number) + ":"
    #         locals()['account_id_' + str(number)] = CoRand.get_rand_int(100001)
    #         locals()['uc_id_' + str(number)] = CoRand.get_rand_int()
    #         locals()['self.ar_con' + str(number)] = ARControl()
    #         locals()['self.ar_con' + str(number)].connect_server()
    #         res = locals()['self.ar_con' + str(number)].login(locals()['account_id_' + str(number)], "im",
    #                                                           locals()['uc_id_' + str(number)], )
    #         res_data = json.loads(res)
    #         locals()['user_id_' + str(number)] = res_data["user_id"]
    #         locals()['nick_name_' + str(number)] = CoRand.get_random_word_filter_sensitive(6)
    #         locals()['self.ar_con' + str(number)].modify_info(locals()['nick_name_' + str(number)])
    #         locals()['self.ar_con' + str(number)].add_friend(user_id)
    #         print "悬赏令使用者同意添加好友" + str(number) + ":"
    #         self.ar_con.get_rev()
    #         self.ar_con.deal_add_friend(locals()['user_id_' + str(number)], 1)
    #         print "好友玩家" + str(number) + "收到消息："
    #         locals()['self.ar_con' + str(number)].get_rev()
    #         number += 1
    #     print "创建好友玩家26："
    #     account_id_26 = CoRand.get_rand_int(100001)
    #     uc_id_26 = CoRand.get_rand_int()
    #     self.ar_con26 = ARControl()
    #     self.ar_con26.connect_server()
    #     res = self.ar_con26.login(account_id_26, "im", uc_id_26)
    #     res_data = json.loads(res)
    #     user_id_26 = res_data["user_id"]
    #     nick_name_26 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con26.modify_info(nick_name_26)
    #     self.ar_con26.add_friend(user_id)
    #     print "悬赏令使用者同意添加好友："
    #     self.ar_con.get_rev()
    #     self.ar_con.deal_add_friend(user_id_26, 1)
    #     print "好友玩家26收到消息："
    #     self.ar_con26.get_rev()
    #
    #     print "创建攻击者玩家："
    #     account_id_attack = CoRand.get_rand_int(100001)
    #     uc_id_attack = CoRand.get_rand_int()
    #     self.ar_con100 = ARControl()
    #     self.ar_con100.connect_server()
    #     res = self.ar_con100.login(account_id_attack, "im", uc_id_attack)
    #     res_data = json.loads(res)
    #     user_id_attack = res_data["user_id"]
    #     nick_name_attack = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con100.modify_info(nick_name_attack)
    #     res = self.ar_con100.match_pet(self.pet_url)
    #     res_data = json.loads(res)
    #     item_id_attack = res_data["item_id"]
    #     self.ar_con100.capture_pet(item_id_attack)
    #     self.ar_con100.set_cultivate_pet(item_id_attack)
    #     part_1 = 1
    #     for i in range(1, 6):
    #         self.ar_con100.upgrade_pet_part(i)
    #         locals()['part_' + str(i)] = i
    #
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_attack, "guidance", 131071)
    #     self.ar_con100.gm_reload_user_data(user_id_attack)
    #     self.ar_con100.pm_set_role_data("lotteryType", 104)
    #     self.ar_con100.attack_pet(part, user_id)
    #     self.ar_con100.close()
    #
    #     print "悬赏令使用者使用6次高级通缉令通缉攻击者："
    #     self.ar_con.get_rev()
    #     self.ar_con.pm_set_role_data("rewardAdvance", 6)
    #     for i in range(0, 6):
    #         res = self.ar_con.reward_player(1, user_id_attack)
    #         res_data = json.loads(res)
    #         assert_that(res_data, has_key("code"), "no code response...")
    #         assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #         assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
    #         assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
    #     res = self.ar_con.get_enemy_list()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("reward_list"), "no reward_list response...")
    #     assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
    #     reward_id = res_data["reward_list"][0]["reward_id"]
    #     res = self.ar_con.get_reward(reward_id)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("left_times"), "no left_times response...")
    #     assert_that(res_data["left_times"], equal_to(60), "left_times mismatch...")
    #     self.ar_con.close()
    #
    #     number = 1
    #     attack_part = 1
    #     while number < 26:
    #         print number, attack_part
    #         if attack_part < 6:
    #             print "好友玩家" + str(number) + "收到消息，攻击被悬赏者："
    #             locals()['self.ar_con' + str(number)].get_rev()
    #             self.sql = ModifySql()
    #             self.sql.update_user(locals()['user_id_' + str(number)], "guidance", 131071)
    #             locals()['self.ar_con' + str(number)].gm_reload_user_data(locals()['user_id_' + str(number)])
    #             locals()['self.ar_con' + str(number)].pm_set_role_data("lotteryType", 104)
    #             locals()['self.ar_con' + str(number)].attack_pet(locals()['part_' + str(attack_part)], user_id_attack,
    #                                                              reward_id)
    #             locals()['self.ar_con' + str(number)].pm_set_role_data("lotteryType", 104)
    #             res = locals()['self.ar_con' + str(number)].attack_pet(locals()['part_' + str(attack_part)],
    #                                                                    user_id_attack, reward_id)
    #             res_data = json.loads(res)
    #             assert_that(res_data, has_key("win_coin"), "no win_coin response...")
    #             assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
    #             assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
    #             assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
    #             attack_part += 1
    #
    #         else:
    #             print "攻击者升级部件："
    #             self.ar_con100.connect_server()
    #             self.ar_con100.login(account_id_attack, "im", uc_id_attack)
    #             self.ar_con100.get_unread_msg()
    #             for j in range(1, 6):
    #                 self.ar_con100.upgrade_pet_part(j)
    #             time.sleep(20)
    #             self.ar_con100.close()
    #
    #             attack_part = 1
    #             continue
    #
    #         number += 1
    #
    #     print "攻击者升级部件："
    #     self.ar_con100.upgrade_pet_part(1)
    #     print "好友玩家26收到消息："
    #     self.ar_con26.get_rev()
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_26, "guidance", 131071)
    #     self.ar_con26.pm_set_role_data("lotteryType", 104)
    #     self.ar_con26.attack_pet(1, user_id_attack, reward_id)
    #
    #     print "悬赏令发布者获取悬赏令攻击信息："
    #     self.ar_con.connect_server()
    #     self.ar_con.login(account_id, "im", uc_id)
    #     self.ar_con.get_unread_msg()
    #     res = self.ar_con.get_reward_attack(reward_id, 1)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_length(50), "response length mismatch...")
    #     res = self.ar_con.get_reward_attack(reward_id, 2)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_length(50), "response length mismatch...")
    #     for m in res_data:
    #         assert_that(m, has_key("user_id"), "no user_id response")
    #         assert_that(m["user_id"], equal_to(user_id_attack), "user_id mismatch...")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(GetRewardAttackTest("test_get_reward_attack_be_rewarded_user_no_shield"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
