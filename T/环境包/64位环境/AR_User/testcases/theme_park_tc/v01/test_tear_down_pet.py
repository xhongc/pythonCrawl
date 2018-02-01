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


class TearDownPetTest(unittest.TestCase):
    def setUp(self):
        print 'start run TearDownPet test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "teardownPet"

    def tearDown(self):
        print 'TearDownPet test complete.....close socket'

    def test_tear_down_pet_success(self):
        """
        卸下宠物成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        pet_id = res_data["pet_id"]
        self.ar_con.capture_pet(pet_id)
        res = self.ar_con.get_theme_park(user_id, -1)
        res_data = json.loads(res)
        theme_park_id = res_data["park_id"]
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        star = res_data["star"]
        self.ar_con.equip_pet(theme_park_id, pet_id, 1)

        res = self.ar_con.tear_down_pet(theme_park_id, pet_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(star), "response star error...")

        res = self.ar_con.get_theme_park(user_id, -1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("pet_id1"), "no pet_id1 response...")
        assert_that(res_data["pet_id1"], equal_to(0), "response pet_id1 error...")

    # def test_tear_down_follow_pet(self):
    #     """
    #     卸随身宠\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     self.ar_con.login(user_id, "im")
    #     res = self.ar_con.get_theme_park(user_id, -1)
    #     res_data = json.loads(res)
    #     theme_park_id = res_data["park_id"]
    #     pet_id = res_data["follow_pet_id"]
    #
    #     res = self.ar_con.tear_down_pet(theme_park_id, pet_id)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("star"), "no star response...")
    #     assert_that(res_data["star"], equal_to(0), "response star error...")

    # def test_tear_down_pet_not_equip(self):
    #     """
    #     卸下未装备宠物\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     self.ar_con.login(user_id, "im")
    #     url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
    #     res = self.ar_con.match_pet(url)
    #     res_data = json.loads(res)
    #     pet_id = res_data["pet_id"]
    #     self.ar_con.capture_pet(pet_id)
    #     res = self.ar_con.get_theme_park(user_id, -1)
    #     res_data = json.loads(res)
    #     theme_park_id = res_data["park_id"]
    #     res = self.ar_con.get_user_info(user_id)
    #     res_data = json.loads(res)
    #     star = res_data["star"]
    #
    #     res = self.ar_con.tear_down_pet(theme_park_id, pet_id)
    #     res_data = json.loads(res)
    #     self.ar_con.get_theme_park(user_id, -1)
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_tear_down_pet_without_params(self):
        """
        卸下宠物失败，未传参数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_tear_down_pet_error_theme_park(self):
        """
        卸下宠物失败，错误的乐园id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        res = self.ar_con.get_theme_park(user_id, -1)
        res_data = json.loads(res)
        pet_id = res_data["follow_pet_id"]
        theme_park_id = CoRand.get_rand_int()

        res = self.ar_con.tear_down_pet(theme_park_id, pet_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NO_FOUND_PLAYER_PARK["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NO_FOUND_PLAYER_PARK["err_msg"]), "response msg mismatching...")

    # def test_tear_down_pet_error_pet(self):
    #     """
    #     卸下宠物失败，错误的宠物id\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     self.ar_con.login(user_id, "im")
    #     res = self.ar_con.get_theme_park(user_id, -1)
    #     res_data = json.loads(res)
    #     theme_park_id = res_data["park_id"]
    #     pet_id = CoRand.get_rand_int()
    #
    #     res = self.ar_con.tear_down_pet(theme_park_id, pet_id)
    #     res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(TearDownPetTest("test_tear_down_pet_error_pet"))
    suite.addTest(TearDownPetTest("test_tear_down_pet_error_theme_park"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)