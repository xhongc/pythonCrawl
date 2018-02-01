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


class GetAttackCountTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetAttackCount test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getAttackCount"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        self.total_part_name = ["head", "arm", "clothes", "skirt", "shoes"]

    def tearDown(self):
        print 'GetAttackCount test complete.....close socket'

    def test_get_attack_count_not_attacked(self):
        """
        获取玩家被攻击次数:未被攻击过\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        res = self.ar_con.login(self.account_id, "im")
        res_data = json.loads(res)
        self.user_id = res_data["user_id"]
        self.ar_con.connect_server()
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_attack_count(self.user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("attack"), "no attack response...")
        assert_that(res_data["attack"], equal_to(0), "response attack mismatch...")

    def test_get_attack_count(self):
        """
        获取玩家被攻击次数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建玩家A："
        account_id_1 = CoRand.get_rand_int(100001)
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
        print "创建攻击玩家B，攻击A（无护盾）："
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
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
        print "玩家A获取攻击次数："
        self.ar_con.get_rev()
        res = self.ar_con.get_attack_count(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("attack"), "no attack response...")
        assert_that(res_data["attack"], equal_to(1), "response attack mismatch...")
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "shield", 1)
        self.ar_con.gm_reload_user_data(user_id_1)
        print "玩家B再次攻击，A（有护盾）："
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        print "玩家A获取攻击次数："
        self.ar_con.get_rev()
        res = self.ar_con.get_attack_count(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("attack"), "no attack response...")
        assert_that(res_data["attack"], equal_to(2), "response attack mismatch...")

    def test_get_attack_count_without_params(self):
        """
        获取玩家被攻击次数:未传参数\
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


if __name__ == "__main__":
    unittest.main()
    # # # 构造测试集
    # suite = unittest.TestSuite()
    #
    # suite.addTest(GetAttackCountTest("test_get_attack_count_not_attacked"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
