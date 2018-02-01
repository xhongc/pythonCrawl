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


class AttackPetTest(unittest.TestCase):
    def setUp(self):
        print 'start run AttackPet test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "attackPet"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        self.total_part_name = ["head", "arm", "clothes", "skirt", "shoes"]

    def tearDown(self):
        print 'AttackPet test complete.....close socket'

    def test_attack_pet_no_attack(self):
        """
        攻击玩家未抽取到攻击卡\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()

        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ALLOW_ATTACK["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ALLOW_ATTACK["err_msg"]), "response msg mismatching...")

    def test_attack_pet_no_shield(self):
        """
        被攻击玩家无护盾，攻击玩家获得300000金币\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()

        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
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
        assert_that(res_data["win_coin"], equal_to(300000), "response coin mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(1), "response star mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(0), "response reward_coin mismatch...")
        assert_that(res_data, has_key("shield"), "no shield response...")
        assert_that(res_data["shield"], equal_to(0), "response shield mismatch...")

    def test_attack_pet_has_shield(self):
        """
        被攻击玩家有护盾，攻击玩家获得100000金币\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "shield", 1)
        self.ar_con.gm_reload_user_data(user_id_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)

        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
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
        assert_that(res_data["win_coin"], equal_to(100000), "response coin mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(1), "response star mismatch...")
        assert_that(res_data, has_key("reward_coin"), "no reward_coin response...")
        assert_that(res_data["reward_coin"], equal_to(0), "response reward_coin mismatch...")
        assert_that(res_data, has_key("shield"), "no shield response...")
        assert_that(res_data["shield"], equal_to(2), "response shield mismatch...")

    def test_attack_pet_first_attack(self):
        """
        部件第一次被攻击，星章数不变，部件等级不变，仍为可攻击状态\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        res = self.ar_con.upgrade_pet_part(part)
        res_data = json.loads(res)
        user1_coin_before = res_data["coin"]
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.get_user_info(user_id_2)
        res_data = json.loads(res)
        user2_coin_before = res_data["coin"]
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        win_coin = res_data["win_coin"]
        assert_that(res_data["coin"], equal_to(user2_coin_before + win_coin), "response coin mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(1), "response star mismatch...")
        print "玩家1执行操作："
        self.ar_con.get_rev()
        res = self.ar_con.get_user_info(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["can_attack"], equal_to(1), "response can_attack mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(user1_coin_before), "response coin mismatch...")

        res = self.ar_con.get_pet_info(pet_id, user_id_1)
        res_data = json.loads(res)
        attack_part_status = self.total_part_name[part - 1] + "_status"
        attack_part_level = self.total_part_name[part - 1] + "_level"
        assert_that(res_data, has_key(attack_part_status), "no attack_part_name response...")
        assert_that(res_data[attack_part_status], equal_to(1), "response attack_part_name mismatch...")
        assert_that(res_data, has_key(attack_part_level), "no attack_part_level response...")
        assert_that(res_data[attack_part_level], equal_to(1), "response attack_part_level mismatch...")

    def test_attack_pet_twice(self):
        """
        同部件两次被攻击，部件等级重置为0，星章数-1\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家1："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        res = self.ar_con.upgrade_pet_part(part)
        res_data = json.loads(res)
        user1_coin_before = res_data["coin"]
        print "创建玩家2两次攻击1："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        self.ar_con.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("win_coin"), "no win_coin response...")
        assert_that(res_data["win_coin"], equal_to(300000), "response coin mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(0), "response star mismatch...")
        print "玩家1查看宠物信息："
        self.ar_con.get_rev()
        res = self.ar_con.get_user_info(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("can_attack"), "no can_attack response...")
        assert_that(res_data["can_attack"], equal_to(0), "response can_attack mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(user1_coin_before), "response coin mismatch...")

        res = self.ar_con.get_pet_info(pet_id, user_id_1)
        res_data = json.loads(res)
        attack_part_status = self.total_part_name[part - 1] + "_status"
        attack_part_level = self.total_part_name[part - 1] + "_level"
        assert_that(res_data, has_key(attack_part_status), "no attack_part_name response...")
        assert_that(res_data[attack_part_status], equal_to(0), "response attack_part_name mismatch...")
        assert_that(res_data, has_key(attack_part_level), "no attack_part_level response...")
        assert_that(res_data[attack_part_level], equal_to(0), "response attack_part_level mismatch...")

    def test_attack_pet_third(self):
        """
        同部件已两次被攻击，无法再次攻击\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_PLAYER_BE_PROTECTED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_PLAYER_BE_PROTECTED["err_msg"]), "response msg mismatching...")

    def test_attack_pet_part_level_0(self):
        """
        攻击0级部位\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_PLAYER_BE_PROTECTED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_PLAYER_BE_PROTECTED["err_msg"]), "response msg mismatching...")

    def test_attack_pet_user_not_have_pet(self):
        """
        攻击--被攻击玩家没有宠物\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        part = CoRand.get_rand_int(1, 5)
        res = self.ar_con2.attack_pet(part, user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_PLAYER_BE_PROTECTED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_PLAYER_BE_PROTECTED["err_msg"]), "response msg mismatching...")

    def test_attack_pet_self(self):
        """
        玩家攻击自己\
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
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.attack_pet(part, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_PLAYER_BE_PROTECTED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_PLAYER_BE_PROTECTED["err_msg"]), "response msg mismatching...")

    def test_attack_pet_without_param(self):
        """
        攻击失败，未传参数\
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
        self.sql.update_user(user_id, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id)
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_USER_NOT_EXIST["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_USER_NOT_EXIST["err_msg"]), "response msg mismatching...")

    def test_attack_pet_without_user_id(self):
        """
        攻击失败，未传user_id参数\
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
        self.sql.update_user(user_id, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id)
        json_body = {
            "part": 1
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_USER_NOT_EXIST["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_USER_NOT_EXIST["err_msg"]), "response msg mismatching...")

    def test_attack_pet_without_part(self):
        """
        攻击失败，未传part参数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        json_body = {
            "user_id": user_id_1
        }
        res = self.ar_con2.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_attack_pet_error_part(self):
        """
        攻击失败，part参数错误\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)

        json_body = {
            "user_id": user_id_1,
            "part": 123
        }
        res = self.ar_con2.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ALLOW_ATTACK_PART["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ALLOW_ATTACK_PART["err_msg"]), "response msg mismatching...")

    def test_attack_pet_error_user_id(self):
        """
        攻击失败，user_id参数错误\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        user_id_2 = CoRand.get_rand_int(100001)

        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 104)
        self.ar_con.gm_reload_user_data(user_id_1)
        json_body = {
            "user_id": user_id_2,
            "part": 1
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_USER_NOT_EXIST["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_USER_NOT_EXIST["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    unittest.main()
    # # # 构造测试集
    # suite = unittest.TestSuite()
    #
    # suite.addTest(AttackPetTest("test_attack_pet_no_shield"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
