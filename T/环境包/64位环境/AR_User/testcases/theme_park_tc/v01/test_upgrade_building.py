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


class UpgradeBuildingTest(unittest.TestCase):
    def setUp(self):
        print 'start run UpgradeBuilding test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "upgradeBuilding"
        self.account_id = 100861

    def tearDown(self):
        print 'UpgradeBuilding test complete.....close socket'

    def test_upgrade_building_success(self):
        """
        升级建筑\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        star_before = res_data["star"]
        coin_before = res_data["coin"]
        res = self.ar_con.get_theme_park(user_id, -1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("buildings"), "no icon response...")
        building_id = res_data["buildings"][0]["building_id"]
        level_before = res_data["buildings"][0]["level"]

        res = self.ar_con.upgrade_building(building_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], less_than(coin_before), "response coin error...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(star_before+1), "response star error...")
        assert_that(res_data, has_key("level"), "no level response...")
        assert_that(res_data["level"], equal_to(level_before + 1), "response level error...")
        assert_that(res_data, has_key("next_park"), "no next_park response...")

    def test_upgrade_building_not_enough_coin(self):
        """
        升级建筑失败，金币不足[基于当前数据，金币规则修改后可能失败]\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        res = self.ar_con.get_theme_park(user_id, -1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("buildings"), "no icon response...")
        building_id = res_data["buildings"][0]["building_id"]
        for i in range(0, 4):
            self.ar_con.upgrade_building(building_id)
        res = self.ar_con.upgrade_building(building_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ENOUGH_COIN["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ENOUGH_COIN["err_msg"]), "response msg mismatching...")

    # def test_upgrade_building_unlock_theme_park(self):
    #     """
    #     所有建筑升至最高级，解锁下一乐园\【用户数据库需配置足够金币】
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = 791099
    #     self.ar_con.login(user_id, "im")
    #     res = self.ar_con.get_user_info(user_id)
    #     res_data = json.loads(res)
    #     star_before = res_data["star"]
    #     coin_before = res_data["coin"]
    #     res = self.ar_con.get_theme_park(user_id, -1)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("buildings"), "no icon response...")
    #     for x in res_data["buildings"]:
    #         building_id = x["building_id"]
    #         for i in range(0, 5):
    #             res = self.ar_con.upgrade_building(building_id)
    #             res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("coin"), "no coin response...")
    #     assert_that(res_data["coin"], less_than(coin_before), "response coin error...")
    #     assert_that(res_data, has_key("star"), "no star response...")
    #     assert_that(res_data["star"], equal_to(star_before + 25), "response star error...")
    #     assert_that(res_data, has_key("level"), "no level response...")
    #     assert_that(res_data, has_key("next_park"), "no next_park response...")
    #     assert_that(res_data["next_park"], equal_to(1), "response next_park error...")

    # def test_upgrade_building_last_level(self):
    #     """
    #     升级一个建筑至最高级，不能解锁下一个乐园\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     self.ar_con.login(user_id, "im")
    #     for i in range(0, 50):
    #         self.ar_con.draw_lottery()
    #     # pp = 50
    #     # while pp != 0:
    #     #     res = self.ar_con.draw_lottery()
    #     #     res_data = json.loads(res)
    #     #     assert_that(res_data, has_key("pp"), "no nick_name response...")
    #     #     pp = res_data["pp"]
    #     res = self.ar_con.get_user_info(user_id)
    #     res_data = json.loads(res)
    #     star_before = res_data["star"]
    #     coin_before = res_data["coin"]
    #     res = self.ar_con.get_theme_park(user_id, -1)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("buildings"), "no icon response...")
    #     building_id = res_data["buildings"][0]["building_id"]
    #     level_before = res_data["buildings"][0]["level"]
    #
    #     for i in range(0, 4):
    #         self.ar_con.upgrade_building(building_id)
    #
    #     res = self.ar_con.upgrade_building(building_id)
    #     res_data = json.loads(res)
    #
    #     if res_data.has_key("err_msg"):
    #         pass
    #     else:
    #         assert_that(res_data, has_key("coin"), "no coin response...")
    #         assert_that(res_data["coin"], less_than(coin_before), "response coin error...")
    #         assert_that(res_data, has_key("star"), "no star response...")
    #         assert_that(res_data["star"], equal_to(star_before + 5), "response star error...")
    #         assert_that(res_data, has_key("level"), "no level response...")
    #         assert_that(res_data["level"], equal_to(level_before + 5), "response level error...")
    #         assert_that(res_data, has_key("next_park"), "no next_park response...")
    #         assert_that(res_data["next_park"], equal_to(0), "response next_park error...")

        # res = self.ar_con.get_theme_park(user_id, 2)
        # res_data = json.loads(res)
        # assert_that(res_data, has_key("park_id"), "no park_id response...")
        # assert_that(res_data, has_key("park_code"), "no park_code response...")
        # assert_that(res_data, has_key("park_name"), "no park_name response...")
        # assert_that(res_data, has_key("user_id"), "no user_id response...")
        # assert_that(res_data, has_key("follow_pet_id"), "no follow_pet_id response...")
        # assert_that(res_data, has_key("pet_id1"), "no pet_id1 response...")

    # def test_upgrade_building_was_highest(self):
    #     """
    #     升级建筑失败，建筑已经是最高级\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     self.ar_con.login(user_id, "im")
    #     for i in range(0, 50):
    #         self.ar_con.draw_lottery()
    #     # pp = 50
    #     # while pp != 0:
    #     #     res = self.ar_con.draw_lottery()
    #     #     res_data = json.loads(res)
    #     #     assert_that(res_data, has_key("pp"), "no nick_name response...")
    #     #     pp = res_data["pp"]
    #     self.ar_con.get_user_info(user_id)
    #     res = self.ar_con.get_theme_park(user_id, -1)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("buildings"), "no icon response...")
    #     building_id = res_data["buildings"][0]["building_id"]
    #
    #     for i in range(0, 5):
    #         self.ar_con.upgrade_building(building_id)
    #
    #     res = self.ar_con.upgrade_building(building_id)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_MAX_BUILDING_LEVEL["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_MAX_BUILDING_LEVEL["err_msg"]), "response msg mismatching...")

    def test_upgrade_building_error_building_id(self):
        """
        升级建筑失败，错误的建筑id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        building_id = CoRand.get_rand_int()
        res = self.ar_con.upgrade_building(building_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NO_FOUND_BUILDING["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NO_FOUND_BUILDING["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(UpgradeBuildingTest("test_upgrade_building_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
