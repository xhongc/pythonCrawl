# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand


class GetDefPetTeamTest(unittest.TestCase):
    """
    查看默认的宠物队伍
    """

    def setUp(self):
        print 'start run GetDefPetTeam test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()

    def tearDown(self):
        print 'GetDefPetTeam test complete.....close socket'

    def test_get_def_pet_team_ok(self):
        """
        查看默认的宠物队伍成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = 100861
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_def_pet_team()
        res_data = json.loads(res)

        assert_that(res_data, has_key("team_code"), "no team_code response...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data, has_key("pet_id1"), "no pet_id1 response...")
        assert_that(res_data, has_key("pet_id2"), "no pet_id2 response...")
        assert_that(res_data, has_key("pet_id3"), "no pet_id3 response...")
        assert_that(res_data, has_key("pet_id4"), "no pet_id4 response...")
        assert_that(res_data, has_key("pet_id5"), "no pet_id5 response...")
        assert_that(res_data, has_key("pet_id6"), "no pet_id6 response...")
        assert_that(res_data, has_key("pet_id7"), "no pet_id7 response...")
        assert_that(res_data, has_key("pet_id8"), "no pet_id8 response...")
        assert_that(res_data, has_key("pet_id9"), "no pet_id9 response...")
        assert_that(res_data, has_key("skill_id"), "no skill_id response...")


if __name__ == "__main__":
    unittest.main()
