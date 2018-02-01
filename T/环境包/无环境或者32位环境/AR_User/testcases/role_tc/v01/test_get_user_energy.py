# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
import time
from cof.rand import CoRand


class GetUserEnergyTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetUserEnergy test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetUserEnergy test complete.....close socket'

    def test_get_energy_success(self):
        """
        获取玩家体力值--初始体力50个\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        res = self.ar_con.get_energy()
        res_data = json.loads(res)

        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(50), "response pp mismatch...")
        assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
        assert_that(res_data["last_pp_regain"], equal_to(0), "response last_pp_regain mismatch...")

    def test_get_energy_after(self):
        """
        获取玩家体力值--抽奖后扣除体力\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.draw_lottery()
        time_full = int(time.time())
        res_data = json.loads(res)
        time.sleep(1)

        if res_data["item"] == 102:
            res = self.ar_con.get_energy()
            res_data = json.loads(res)
            assert_that(res_data, has_key("pp"), "no pp response...")
            assert_that(res_data["pp"], equal_to(59), "pp mismatching...")
            assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
            assert_that(res_data["last_pp_regain"], equal_to(0), "response last_pp_regain mismatch...")
        else:
            res = self.ar_con.get_energy()
            res_data = json.loads(res)
            time_not_full = int(time.time())
            assert_that(res_data, has_key("pp"), "no pp response...")
            assert_that(res_data["pp"], equal_to(49), "response pp mismatch...")
            assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
            assert_that(abs(res_data["last_pp_regain"] - (time_not_full-time_full)), less_than(1), "response last_pp_regain mismatch...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetUserEnergyTest("test_get_energy_after"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
