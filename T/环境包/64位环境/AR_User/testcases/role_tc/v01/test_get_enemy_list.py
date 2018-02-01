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


class GetEnemyListTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetEnemyList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.sql = ModifySql()
        self.api_name = "getEnemyList"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        self.total_part_name = ["head", "arm", "clothes", "skirt", "shoes"]

    def tearDown(self):
        print 'GetEnemyList test complete.....close socket'

    def test_attack_pet_join_enemy_list(self):
        """
        非好友玩家攻击成功，加入仇人列表（未复仇）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "创建玩家B攻击A："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name)
        res = self.ar_con2.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_2 = res_data["item_id"]
        self.ar_con2.capture_pet(item_id_2)
        self.ar_con2.set_cultivate_pet(item_id_2)
        part_2 = CoRand.get_rand_int(1, 5)
        self.ar_con2.upgrade_pet_part(part_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        user2_coin_before = res_data["coin"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        win_coin = res_data["win_coin"]
        assert_that(res_data["coin"], equal_to(user2_coin_before + win_coin), "response coin mismatch...")
        print "玩家A查看仇人列表："
        self.ar_con.get_rev()
        time.sleep(1)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_2 in user_ids
        enemy_index = user_ids.index(user_id_2)
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index]["nick_name"], equal_to(nick_name),
                    "response nick_name mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index]["sex"], equal_to(0), "response sex mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")

    def test_attack_pet_join_enemy_list_revenge(self):
        """
        非好友玩家攻击,玩家已复仇，从仇人列表中去除\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "创建玩家B攻击A："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name)
        res = self.ar_con2.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_2 = res_data["item_id"]
        self.ar_con2.capture_pet(item_id_2)
        self.ar_con2.set_cultivate_pet(item_id_2)
        part_2 = CoRand.get_rand_int(1, 5)
        self.ar_con2.upgrade_pet_part(part_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        user2_coin_before = res_data["coin"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        win_coin = res_data["win_coin"]
        assert_that(res_data["coin"], equal_to(user2_coin_before + win_coin), "response coin mismatch...")
        print "玩家A复仇，攻击B后查看仇人列表："
        self.ar_con.get_rev()
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_2 in user_ids
        enemy_index = user_ids.index(user_id_2)
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index]["nick_name"], equal_to(nick_name),
                    "response nick_name mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index]["sex"], equal_to(0), "response sex mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.attack_pet(part_2, user_id_2)
        time.sleep(1)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert res_data["enemy_list"] == [], "response enemy_list mismatch..."
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["reward_list"] == [], "response reward_list mismatch..."

    def test_attack_pet_join_enemy_list_has_revenged_and_friend_reward(self):
        """
        非好友玩家攻击,玩家已复仇，且该攻击玩家被好友悬赏，查看仇人列表\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        print "创建玩家A："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
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
        res = self.ar_con2.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_2 = res_data["item_id"]
        self.ar_con2.capture_pet(item_id_2)
        self.ar_con2.set_cultivate_pet(item_id_2)
        part_2 = CoRand.get_rand_int(1, 5)
        self.ar_con2.upgrade_pet_part(part_2)
        self.ar_con2.add_friend(user_id_1)
        print "A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "B收到消息："
        self.ar_con2.get_rev()
        print "创建玩家C攻击A、B："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name)
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
        self.ar_con3.attack_pet(part, user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_2, user_id_2)
        print "B通缉攻击者C："
        self.ar_con2.get_rev()
        self.ar_con2.reward_player(0, user_id_3)
        print "玩家A复仇，攻击C后查看仇人列表："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.attack_pet(part_3, user_id_3)
        time.sleep(1)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_3 in user_ids
        enemy_index = user_ids.index(user_id_3)
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index]["nick_name"], equal_to(nick_name),
                    "response nick_name mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index]["sex"], equal_to(0), "response sex mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")

        assert res_data["reward_list"] != [], "response reward_list mismatch..."
        reward_player_ids = []
        for j in res_data["reward_list"]:
            assert_that(j, has_key("be_reward_user_id"), "no be_reward_user_id response...")
            reward_player_ids.append(j["be_reward_user_id"])
        assert user_id_3 in reward_player_ids, "attack_user not in reward_list..."
        user_id_3_index = reward_player_ids.index(user_id_3)
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["reward_list"][user_id_3_index]["user_id"], equal_to(user_id_2),
                    "response user_id mismatch...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_list"][user_id_3_index]["reward_type"], equal_to(0),
                    "response reward_type mismatch...")

    def test_attack_pet_friend(self):
        """
        好友玩家攻击成功，加入仇人列表\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家2："
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
        print "创建好友玩家1："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)
        print "玩家2同意添加好友："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, 1)
        print "玩家1执行操作："
        self.ar_con.get_rev()
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "玩家2攻击1："
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        print "玩家1获取仇人列表："
        self.ar_con.get_rev()
        time.sleep(1)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)

        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_2 in user_ids
        enemy_index = user_ids.index(user_id_2)
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index]["nick_name"], equal_to(nick_name_2),
                    "response nick_name mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index]["sex"], equal_to(0), "response sex mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")

    def test_get_enemy_list_reward_player_normal(self):
        """
        获取仇人列表--悬赏仇人后，加入悬赏令列表（普通通缉令）\
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
        print "悬赏令使用者获取仇人列表："
        self.ar_con.get_rev()
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_3 in user_ids
        enemy_index = user_ids.index(user_id_3)
        assert_that(res_data["enemy_list"][enemy_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["enemy_list"][enemy_index]["user_id"], equal_to(user_id_3), "response user_id mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("pet_id"), "no pet_id response...")

        print "悬赏令使用者通缉攻击者后，查询仇人列表："
        self.ar_con.reward_player(0, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_3 in user_ids
        enemy_index = user_ids.index(user_id_3)
        assert_that(res_data["enemy_list"][enemy_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["enemy_list"][enemy_index]["user_id"], equal_to(user_id_3), "response user_id mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("pet_id"), "no pet_id response...")

        reward_player_ids = []
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["reward_list"] != [], "response reward_list mismatch..."
        for j in res_data["reward_list"]:
            assert_that(j, has_key("be_reward_user_id"), "no be_reward_user_id response...")
            reward_player_ids.append(j["be_reward_user_id"])
        assert user_id_3 in reward_player_ids, "attack_user not in reward_list..."
        user_id_3_index = reward_player_ids.index(user_id_3)
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["reward_list"][user_id_3_index]["user_id"], equal_to(user_id_1),
                    "response user_id mismatch...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_list"][user_id_3_index]["reward_type"], equal_to(0),
                    "response reward_type mismatch...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("end_time"), "no end_time response...")

    def test_get_enemy_list_reward_player_advance(self):
        """
        获取仇人列表---悬赏仇人后，加入悬赏令列表（高级通缉令）\
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
        print "悬赏令使用者获取仇人列表："
        self.ar_con.get_rev()
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_3 in user_ids
        enemy_index = user_ids.index(user_id_3)
        assert_that(res_data["enemy_list"][enemy_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["enemy_list"][enemy_index]["user_id"], equal_to(user_id_3), "response user_id mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("pet_id"), "no pet_id response...")

        print "悬赏令使用者通缉攻击者后，查询仇人列表："
        self.ar_con.reward_player(1, user_id_3)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_3 in user_ids
        enemy_index = user_ids.index(user_id_3)
        assert_that(res_data["enemy_list"][enemy_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["enemy_list"][enemy_index]["user_id"], equal_to(user_id_3), "response user_id mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("pet_id"), "no pet_id response...")

        reward_player_ids = []
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["reward_list"] != [], "response reward_list mismatch..."
        for j in res_data["reward_list"]:
            assert_that(j, has_key("be_reward_user_id"), "no be_reward_user_id response...")
            reward_player_ids.append(j["be_reward_user_id"])
        assert user_id_3 in reward_player_ids, "attack_user not in reward_list..."
        user_id_3_index = reward_player_ids.index(user_id_3)
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["reward_list"][user_id_3_index]["user_id"], equal_to(user_id_1),
                    "response user_id mismatch...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_list"][user_id_3_index]["reward_type"], equal_to(1),
                    "response reward_type mismatch...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("end_time"), "no end_time response...")

    def test_get_enemy_list_reward_player_friend(self):
        """
        获取仇人列表--被悬赏玩家加入悬赏者好友的悬赏列表\
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
        self.ar_con.reward_player(0, user_id_3)

        print "好友玩家收到消息："
        self.ar_con2.get_rev()
        res = self.ar_con2.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["reward_list"] != [], "response reward_list mismatch..."
        reward_player_ids = []
        for j in res_data["reward_list"]:
            assert_that(j, has_key("be_reward_user_id"), "no be_reward_user_id response...")
            reward_player_ids.append(j["be_reward_user_id"])
        assert user_id_3 in reward_player_ids, "attack_user not in reward_list..."
        user_id_3_index = reward_player_ids.index(user_id_3)
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("user_id"), "no user_id response...")
        assert_that(res_data["reward_list"][user_id_3_index]["user_id"], equal_to(user_id_1),
                    "response user_id mismatch...")
        assert_that(res_data["reward_list"][user_id_3_index], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_list"][user_id_3_index]["reward_type"], equal_to(0),
                    "response reward_type mismatch...")

    def test_get_enemy_list_attacker_can_not_attack(self):
        """
        攻击自己的非好友玩家养成宠不可被攻击，加入仇人列表\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "创建玩家B攻击A,B当前养成宠未升级，不可攻击："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        user2_coin_before = res_data["coin"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        win_coin = res_data["win_coin"]
        assert_that(res_data["coin"], equal_to(user2_coin_before + win_coin), "response coin mismatch...")
        print "玩家A查看仇人列表："
        self.ar_con.get_rev()
        time.sleep(1)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["enemy_list"] != [], "response enemy_list mismatch..."
        user_ids = []
        for i in res_data["enemy_list"]:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_ids.append(i["user_id"])
        assert user_id_2 in user_ids
        enemy_index = user_ids.index(user_id_2)
        assert_that(res_data["enemy_list"][enemy_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["enemy_list"][enemy_index]["nick_name"], equal_to(nick_name),
                    "response nick_name mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("sex"), "no sex response...")
        assert_that(res_data["enemy_list"][enemy_index]["sex"], equal_to(0), "response sex mismatch...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("icon"), "no icon response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("star"), "no star response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["enemy_list"][enemy_index], has_key("attack"), "no attack response...")
        assert_that(res_data["enemy_list"][enemy_index]["attack"], equal_to(1), "response attack mismatch...")

    def test_enemy_list_attack_first(self):
        """
        A攻击B，B复仇,B不加入A的仇人列表\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家B："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "创建玩家A攻击B："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name)
        res = self.ar_con2.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_2 = res_data["item_id"]
        self.ar_con2.capture_pet(item_id_2)
        self.ar_con2.set_cultivate_pet(item_id_2)
        part_2 = CoRand.get_rand_int(1, 5)
        self.ar_con2.upgrade_pet_part(part_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        user2_coin_before = res_data["coin"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        win_coin = res_data["win_coin"]
        assert_that(res_data["coin"], equal_to(user2_coin_before + win_coin), "response coin mismatch...")
        print "玩家B复仇，攻击A："
        self.ar_con.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.ar_con.attack_pet(part_2, user_id_2)

        print "获取A的仇人列表："
        self.ar_con2.get_rev()
        res = self.ar_con2.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("enemy_list"), "no enemy_list response...")
        assert res_data["enemy_list"] == [], "response enemy_list mismatch..."
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert res_data["reward_list"] == [], "response reward_list mismatch..."

if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetEnemyListTest("test_get_enemy_list_reward_player_normal"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
