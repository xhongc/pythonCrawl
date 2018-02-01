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


class SetCultivatePetTest(unittest.TestCase):
    def setUp(self):
        print 'start run SetCultivatePet test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "setCultivatePet"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'SetCultivatePet test complete.....close socket'

    def test_set_cultivate_pet_success(self):
        """
        设置养成宠成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)

        res = self.ar_con.set_cultivate_pet(pet_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data["pet_idx"], equal_to(1), "response pet_idx mismatch...")

    def test_set_cultivate_pet_not_capture(self):
        """
        设置未抓捕宠物为养成宠\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        pet_type = res_data["item_type"]

        if pet_type < 200:
            res = self.ar_con.set_cultivate_pet(pet_id)
            res_data = json.loads(res)

            assert_that(res_data, has_key("code"), "no code response...")
            assert_that(res_data, has_key("err_msg"), "no err_msg response...")
            assert_that(res_data["code"], equal_to(EC_PET_NOT_CAPTURE["code"]), "response code mismatching...")
            assert_that(res_data["err_msg"], equal_to(EC_PET_NOT_CAPTURE["err_msg"]), "response msg mismatching...")

    def test_set_cultivate_pet_max_next(self):
        """
        当前养成宠升级至顶级，设置下一只养成宠\
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

        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id_2 = res_data["item_id"]
        self.ar_con.capture_pet(pet_id_2)
        res = self.ar_con.set_cultivate_pet(pet_id_2)
        res_data = json.loads(res)

        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data["pet_idx"], equal_to(2), "response pet_idx mismatch...")

    def test_set_cultivate_pet_not_complete_next(self):
        """
        当前养成宠未升级至顶级，设置下一只养成宠\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        part = 1
        self.ar_con.upgrade_pet_part(part)

        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id_2 = res_data["item_id"]
        self.ar_con.capture_pet(pet_id_2)
        res = self.ar_con.set_cultivate_pet(pet_id_2)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_COMPLETE_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_COMPLETE_PET["err_msg"]), "response msg mismatching...")

    def test_set_cultivate_pet_has_been_cultivate_pet(self):
        """
        已是养成宠，重设为养成宠\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        self.ar_con.capture_pet(pet_id)
        self.ar_con.set_cultivate_pet(pet_id)
        res = self.ar_con.set_cultivate_pet(pet_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ALLOW_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ALLOW_PET["err_msg"]), "response msg mismatching...")

    def test_set_cultivate_pet_not_found(self):
        """
        设置养成宠,不存在的宠物\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        pet_id = CoRand.get_rand_int()
        res = self.ar_con.set_cultivate_pet(pet_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_set_cultivate_pet_without_pet_id(self):
        """
        设置养成宠，未传pet_id\
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
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(SetCultivatePetTest("test_set_cultivate_pet_max_next"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
