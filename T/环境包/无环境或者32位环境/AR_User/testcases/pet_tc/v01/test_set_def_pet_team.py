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


class SetDefPetTeamTest(unittest.TestCase):

    def setUp(self):
        print 'start run SetDefPetTeam test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "setDefPetTeam"

    def tearDown(self):
        print 'SetDefPetTeam test complete.....close socket'

    def test_set_def_pet_team_success(self):
        """
        设置默认的宠物队伍成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        pet_member = []
        pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        pet_member.append(pet_id)
        self.ar_con.capture_pet(pet_id)
        res = self.ar_con.get_def_pet_team()
        res_data = json.loads(res)
        team_code = res_data["team_code"]

        res = self.ar_con.set_def_pet_team(pet_member, team_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_def_pet_team()
        res_data = json.loads(res)
        assert_that(res_data, has_key("team_code"), "no team_code response...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "user_id mismatching...")
        assert_that(res_data, has_key("pet_id1"), "no pet_id1 response...")
        assert_that(res_data["pet_id1"], equal_to(pet_id), "user_id mismatching...")

    def test_set_def_pet_team_batch(self):
        """
        批量设置默认的宠物队伍成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        pet_member = []
        for A in range(0, 3):
            pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
            res = self.ar_con.scan_face(pet_url, "la", 1)
            res_data = json.loads(res)
            pet_id = res_data["item_id"]
            pet_member.append(pet_id)
            self.ar_con.capture_pet(pet_id)

        res = self.ar_con.get_def_pet_team()
        res_data = json.loads(res)
        team_code = res_data["team_code"]

        res = self.ar_con.set_def_pet_team(pet_member, team_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_set_def_pet_team_too_much_pet(self):
        """
        批量设置默认的宠物队伍失败，宠物超过3个\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        pet_member = []
        for A in range(0, 5):
            pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
            res = self.ar_con.scan_face(pet_url, "la", 1)
            res_data = json.loads(res)
            pet_id = res_data["item_id"]
            pet_member.append(pet_id)
            self.ar_con.capture_pet(pet_id)

        res = self.ar_con.get_def_pet_team()
        res_data = json.loads(res)
        team_code = res_data["team_code"]

        res = self.ar_con.set_def_pet_team(pet_member, team_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_set_def_pet_team_without_params(self):
        """
        设置默认的宠物队伍失败，未传参数\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(100861, "im")
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_set_def_pet_team_error_pet_member(self):
        """
        设置默认的宠物队伍失败，错误的宠物id列表\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(100861, "im")
        pet_member = [1, 2, 3]
        res = self.ar_con.get_def_pet_team()
        res_data = json.loads(res)
        team_code = res_data["team_code"]
        res = self.ar_con.set_def_pet_team(pet_member, team_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_set_def_pet_team_error_team_code(self):
        """
        设置默认的宠物队伍失败，错误的队伍编号\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        pet_member = []
        pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(pet_url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["item_id"]
        pet_member.append(pet_id)
        self.ar_con.capture_pet(pet_id)
        team_code = 9999

        res = self.ar_con.set_def_pet_team(pet_member, team_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    unittest.main()
    #  # 构造测试集
    #  suite = unittest.TestSuite()
    #  suite.addTest(SetDefPetTeamTest("test_set_def_pet_team_success"))
    #
    #  # 执行测试
    #  runner = unittest.TextTestRunner()
    #  runner.run(suite)
