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


class UpgradePetPartTest(unittest.TestCase):
    def setUp(self):
        print 'start run UpgradePetPart test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "upgradePetPart"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        self.total_part_name = ["head", "arm", "clothes", "skirt", "shoes"]

    def tearDown(self):
        print 'UpgradePetPart test complete.....close socket'

    def test_upgrade_pet_part_success(self):
        """
        升级部件成功\
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
        coin_before = res_data["coin"]
        star_before = res_data["star"]
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        res = self.ar_con.upgrade_pet_part(part)
        res_data = json.loads(res)

        assert_that(res_data, has_key("part"), "no part response...")
        assert_that(res_data["part"], equal_to(part), "response part mismatch...")
        assert_that(res_data, has_key("level"), "no level response...")
        assert_that(res_data["level"], equal_to(1), "response level mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], less_than(coin_before), "response coin error...")
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")
        assert_that(res_data["is_complete"], equal_to(0), "response is_complete mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(star_before+1), "response star mismatch...")
        assert_that(res_data, has_key("reward_normal"), "no reward_normal response...")
        assert_that(res_data["reward_normal"], equal_to(1), "reward_normal mismatching...")

        res = self.ar_con.get_pet_info(pet_id, user_id)
        res_data = json.loads(res)
        attack_part_status = self.total_part_name[part-1] + "_status"
        attack_part_level = self.total_part_name[part-1] + "_level"
        assert_that(res_data, has_key(attack_part_status), "no attack_part_status response...")
        assert_that(res_data[attack_part_status], equal_to(0), "response attack_part_status mismatch...")
        assert_that(res_data, has_key(attack_part_level), "no attack_part_level response...")
        assert_that(res_data[attack_part_level], equal_to(1), "response attack_part_level mismatch...")

    def test_upgrade_pet_part_error_part(self):
        """
        升级部件失败，part错误\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int()
        res = self.ar_con.upgrade_pet_part(part)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_upgrade_pet_part_not_enough_coin(self):
        """
        升级部件失败，金币不足\
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
        self.sql.update_user(user_id, "coin", 0)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = CoRand.get_rand_int(1, 5)
        res = self.ar_con.upgrade_pet_part(part)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ENOUGH_COIN["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ENOUGH_COIN["err_msg"]), "response msg mismatching...")

    def test_upgrade_pet_part_max_pet(self):
        """
        所有部件升级至最高级，解锁下一个养成宠\
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
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = 1
        while part != 6:
            for i in range(0, 5):
                self.ar_con.upgrade_pet_part(part)
            part += 1

        res = self.ar_con.get_pet_info(pet_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")
        assert_that(res_data["is_complete"], equal_to(1), "response is_complete mismatch...")

        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id_2 = res_data["item_id"]
        self.ar_con.capture_pet(pet_id_2)
        self.ar_con.set_cultivate_pet(pet_id_2)
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data["pet_idx"], equal_to(2), "response pet_idx mismatch...")

    def test_upgrade_pet_part_without_part(self):
        """
        升级部件失败，未传part参数\
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

    def test_upgrade_pet_part_get_reward_normal(self):
        """
        升级部件：完成一只养成宠，获得一个普通悬赏令\
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
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
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
        assert_that(res_data, has_key("part"), "no part response...")
        assert_that(res_data["part"], equal_to(5), "response part mismatch...")
        assert_that(res_data, has_key("level"), "no level response...")
        assert_that(res_data["level"], equal_to(5), "response level mismatch...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("is_complete"), "no is_complete response...")
        assert_that(res_data["is_complete"], equal_to(1), "response is_complete mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(25), "response star mismatch...")
        assert_that(res_data, has_key("reward_normal"), "no reward_normal response...")
        assert_that(res_data["reward_normal"], equal_to(2), "reward_normal mismatching...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("reward_normal"), "no reward_normal response...")
        assert_that(res_data["reward_normal"], equal_to(2), "reward_normal mismatching...")
        assert_that(res_data, has_key("reward_advance"), "no reward_advance response...")
        assert_that(res_data["reward_advance"], equal_to(1), "reward_advance mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(UpgradePetPartTest("test_upgrade_pet_part_max_pet"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
