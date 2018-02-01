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


class GetThemeParkTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetThemePark test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getThemePark"
        self.account_id = 100861

    def tearDown(self):
        print 'GetThemePark test complete.....close socket'

    def test_get_theme_park_current(self):
        """
        获取当前主题乐园数据\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        park_code = -1
        res = self.ar_con.get_theme_park(self.user_id, park_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("park_id"), "no park_id response...")
        assert_that(res_data, has_key("park_code"), "no park_code response...")
        assert_that(res_data, has_key("park_name"), "no park_name response...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data, has_key("follow_pet_id"), "no follow_pet_id response...")
        assert_that(res_data, has_key("pet_id1"), "no pet_id1 response...")
        assert_that(res_data, has_key("pet_id2"), "no pet_id2 response...")
        assert_that(res_data, has_key("pet_id3"), "no pet_id3 response...")
        assert_that(res_data, has_key("pet_id4"), "no pet_id4 response...")
        assert_that(res_data, has_key("pet_id5"), "no pet_id5 response...")
        assert_that(res_data, has_key("buildings"), "no buildings response...")
        for building in res_data["buildings"]:
            assert_that(building, has_key("building_id"), "no building_id response...")
            assert_that(building, has_key("building_code"), "no building_code response...")
            assert_that(building, has_key("park_id"), "no park_id response...")
            assert_that(building, has_key("status"), "no status response...")
            assert_that(building, has_key("level"), "no level response...")
            assert_that(building, has_key("model"), "no model response...")

    def test_get_theme_park_appoint(self):
        """
        获取指定主题乐园数据\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        park_code = 1
        res = self.ar_con.get_theme_park(self.user_id, park_code)
        res_data = json.loads(res)

        assert_that(res_data, has_key("park_id"), "no park_id response...")
        assert_that(res_data, has_key("park_code"), "no park_code response...")
        assert_that(res_data, has_key("park_name"), "no park_name response...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data, has_key("follow_pet_id"), "no follow_pet_id response...")
        assert_that(res_data, has_key("pet_id1"), "no pet_id1 response...")
        assert_that(res_data, has_key("pet_id2"), "no pet_id2 response...")
        assert_that(res_data, has_key("pet_id3"), "no pet_id3 response...")
        assert_that(res_data, has_key("pet_id4"), "no pet_id4 response...")
        assert_that(res_data, has_key("pet_id5"), "no pet_id5 response...")
        assert_that(res_data, has_key("buildings"), "no buildings response...")
        for building in res_data["buildings"]:
            assert_that(building, has_key("building_id"), "no building_id response...")
            assert_that(building, has_key("building_code"), "no building_code response...")
            assert_that(building, has_key("park_id"), "no park_id response...")
            assert_that(building, has_key("status"), "no status response...")
            assert_that(building, has_key("level"), "no level response...")
            assert_that(building, has_key("model"), "no model response...")

if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(GetThemeParkTest("test_get_theme_park_appoint"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
