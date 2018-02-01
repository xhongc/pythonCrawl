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


class GetRewardTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetReward test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getReward"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'GetReward test complete.....close socket'

    def test_get_reward_normal(self):
        """
        获取悬赏令信息:普通悬赏令，被悬赏者被攻击后，剩余悬赏攻击次数-1\
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
        res = self.ar_con3.get_user_coin()
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
        res = self.ar_con.get_reward(reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data, has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
        assert_that(res_data, has_key("end_time"), "no end_time response...")
        assert_that(res_data, has_key("left_times"), "no left_times response...")
        assert_that(res_data["left_times"], equal_to(5), "response left_times mismatch...")
        assert_that(res_data, has_key("reward_type"), "no left_times response...")
        assert_that(res_data["reward_type"], equal_to(0), "response left_times mismatch...")
        assert_that(res_data, has_key("total_toll"), "no total_toll response...")
        assert_that(res_data["total_toll"], equal_to(0), "response total_toll mismatch...")
        assert_that(res_data, has_key("total_attack"), "no total_attack response...")
        assert_that(res_data["total_attack"], equal_to(0), "response total_attack mismatch...")

        print "悬赏令使用者自己攻击被悬赏者："
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        self.ar_con.get_rev()
        res = self.ar_con.get_reward(reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data, has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
        assert_that(res_data, has_key("end_time"), "no end_time response...")
        assert_that(res_data, has_key("left_times"), "no left_times response...")
        assert_that(res_data["left_times"], equal_to(4), "response left_times mismatch...")
        assert_that(res_data, has_key("reward_type"), "no left_times response...")
        assert_that(res_data["reward_type"], equal_to(0), "response left_times mismatch...")
        assert_that(res_data, has_key("total_toll"), "no total_toll response...")
        assert_that(res_data["total_toll"], equal_to(int((coin_before-coin_after)*0.5)), "response total_toll mismatch...")
        assert_that(res_data, has_key("total_attack"), "no total_attack response...")
        assert_that(res_data["total_attack"], equal_to(1), "response total_attack mismatch...")

    def test_get_reward_advance(self):
        """
        获取悬赏令信息:高级悬赏令\
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
        res = self.ar_con3.get_user_coin()
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
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

        print "悬赏令使用者通缉攻击者,并攻击："
        self.ar_con.get_rev()
        self.ar_con.reward_player(1, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.pm_set_role_data("lotteryType", 104)
        self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        self.ar_con.get_rev()
        res = self.ar_con.get_reward(reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data, has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
        assert_that(res_data, has_key("end_time"), "no end_time response...")
        assert_that(res_data, has_key("left_times"), "no left_times response...")
        assert_that(res_data["left_times"], equal_to(9), "response left_times mismatch...")
        assert_that(res_data, has_key("reward_type"), "no left_times response...")
        assert_that(res_data["reward_type"], equal_to(1), "response left_times mismatch...")
        assert_that(res_data, has_key("total_toll"), "no total_toll response...")
        assert_that(res_data["total_toll"], equal_to(int((coin_before - coin_after) * 0.5)),
                    "response total_toll mismatch...")
        assert_that(res_data, has_key("total_attack"), "no total_attack response...")
        assert_that(res_data["total_attack"], equal_to(1), "response total_attack mismatch...")

    def test_get_reward_others(self):
        """
        获取悬赏令信息:获取其他玩家悬赏令信息\
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

        print "悬赏令使用者通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.reward_player(1, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]

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
        res = self.ar_con4.get_reward(reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data, has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
        assert_that(res_data, has_key("end_time"), "no end_time response...")
        assert_that(res_data, has_key("left_times"), "no left_times response...")
        assert_that(res_data["left_times"], equal_to(10), "response left_times mismatch...")
        assert_that(res_data, has_key("reward_type"), "no left_times response...")
        assert_that(res_data["reward_type"], equal_to(1), "response left_times mismatch...")

    def test_get_reward_error_reward_id(self):
        """
        获取悬赏令信息:错误的reward_id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        reward_id = CoRand.get_rand_int()
        res = self.ar_con.get_reward(reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_get_reward_without_params(self):
        """
        获取悬赏令信息:未传参数\
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

    def test_get_reward_add_reward(self):
        """
        获取悬赏令信息--获取追加悬赏令信息\
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

        print "悬赏令使用者使用普通通缉令通缉攻击者："
        self.ar_con.get_rev()
        res = self.ar_con.reward_player(0, user_id_3)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        self.ar_con.get_enemy_list()
        print "追加高级悬赏令："
        self.ar_con.reward_player(1, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.evil_rank_list(0)
        # print "悬赏令使用者自己攻击被悬赏者："
        # self.sql = ModifySql()
        # self.sql.update_user(user_id_1, "lottery_type", 104)
        # self.ar_con.gm_reload_user_data(user_id_1)
        # self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        # self.ar_con.get_rev()
        print"获取悬赏令信息："
        res = self.ar_con.get_reward(reward_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data, has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
        assert_that(res_data, has_key("end_time"), "no end_time response...")
        assert_that(res_data, has_key("left_times"), "no left_times response...")
        assert_that(res_data["left_times"], equal_to(15), "response left_times mismatch...")
        assert_that(res_data, has_key("reward_type"), "no left_times response...")
        assert_that(res_data["reward_type"], equal_to(0), "response left_times mismatch...")

    def test_get_reward_add_reward_attack(self):
        """
        获取悬赏令信息--获取追加悬赏令信息,包含追加前和追加后的信息\
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

        # print "A自己攻击被悬赏者C："
        # self.sql = ModifySql()
        # self.sql.update_user(user_id_1, "lottery_type", 104)
        # self.ar_con.gm_reload_user_data(user_id_1)
        # res = self.ar_con.attack_pet(part_3, user_id_3, reward_id)
        # res_data = json.loads(res)
        # assert_that(res_data[0], has_key("reward_coin"), "no reward_coin response...")
        # assert_that(res_data[0]["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
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

    def test_get_reward_total_toll_statistics(self):
        """
        获取悬赏令信息--验证累计损失、累计攻击次数数据正确性\
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
        res = self.ar_con3.get_user_coin()
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)

        part_attacker_1 = 1
        res = self.ar_con3.upgrade_pet_part(part_attacker_1)
        res_data = json.loads(res)
        coin_part_1_level_1 = coin_before - res_data["coin"]

        res = self.ar_con3.upgrade_pet_part(part_attacker_1)
        res_data = json.loads(res)
        coin_part_1_level_2 = coin_before - res_data["coin"] - coin_part_1_level_1

        part_attacker_2 = 2
        res = self.ar_con3.upgrade_pet_part(part_attacker_2)
        res_data = json.loads(res)
        coin_part_2_level_1 = coin_before - res_data["coin"] - coin_part_1_level_1 - coin_part_1_level_2

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

        print "好友玩家B收到消息，攻击被悬赏者C，打坏部件2："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.pm_set_role_data("lotteryType", 104)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con2.attack_pet(part_attacker_2, user_id_3, reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response win_coin mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(300000), "response reward_coin mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before + 600000), "response reward_coin mismatch...")
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("toll"), "no toll response...")
        assert_that(res_data["toll"], equal_to(int(coin_part_2_level_1*0.5)))

        print "好友玩家D收到消息，攻击被悬赏者C，打坏部件1："
        self.ar_con4.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "guidance", 131071)
        self.ar_con4.gm_reload_user_data(user_id_4)
        self.ar_con4.pm_set_role_data("lotteryType", 104)
        self.ar_con4.attack_pet(part_attacker_1, user_id_3, reward_id)
        print "A收到消息："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("toll"), "no toll response...")
        assert_that(res_data["toll"], equal_to(int(coin_part_1_level_2 * 0.5)))
        print "好友玩家D再次攻击被悬赏者C，打爆部件1："
        self.ar_con4.pm_set_role_data("lotteryType", 104)
        self.ar_con4.attack_pet(part_attacker_1, user_id_3, reward_id)
        print "A收到消息："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("toll"), "no toll response...")
        assert_that(res_data["toll"], equal_to(int(coin_part_1_level_2 * 0.5)+coin_part_1_level_1))

        print "A自己攻击被悬赏者C，打爆部件2："
        self.ar_con.pm_set_role_data("lotteryType", 104)
        self.ar_con.attack_pet(part_attacker_2, user_id_3, reward_id)
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("toll"), "no toll response...")
        assert_that(res_data["toll"], equal_to(int(coin_part_2_level_1*0.5)))
        print"获取悬赏令信息："
        time.sleep(1)
        res = self.ar_con.get_reward(reward_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data, has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
        assert_that(res_data, has_key("end_time"), "no end_time response...")
        assert_that(res_data, has_key("left_times"), "no left_times response...")
        assert_that(res_data["left_times"], equal_to(1), "response left_times mismatch...")
        assert_that(res_data, has_key("reward_type"), "no left_times response...")
        assert_that(res_data["reward_type"], equal_to(0), "response left_times mismatch...")
        assert_that(res_data, has_key("total_toll"), "no total_toll response...")
        assert_that(res_data["total_toll"], equal_to(coin_part_1_level_1+coin_part_1_level_2+coin_part_2_level_1), "response total_toll mismatch...")
        assert_that(res_data, has_key("total_attack"), "no total_attack response...")
        assert_that(res_data["total_attack"], equal_to(4), "response total_attack mismatch...")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(GetRewardTest("test_get_reward_total_toll_statistics"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
