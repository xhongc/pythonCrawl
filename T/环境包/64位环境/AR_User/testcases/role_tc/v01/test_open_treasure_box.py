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


class OpenTreasureBoxTest(unittest.TestCase):
    def setUp(self):
        print 'start run OpenTreasureBox test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()

    def tearDown(self):
        print 'OpenTreasureBox test complete.....close socket'

    def test_open_treasure_box_success(self):
        """
        开宝箱成功，游戏结果成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        latitude = 26.092
        longitude = 119.314
        event_id = ""

        res = self.ar_con.get_random_event(latitude, longitude)
        res_data = json.loads(res)
        for event in res_data["events"]:
            if event["status"] == 2:
                event_id = event["event_id"]
                break
        print event_id
        game_result = 1
        res = self.ar_con.open_treasure_box(event_id, game_result)
        res_data = json.loads(res)

        assert_that(res_data, has_key("event_id"), "no event_id response...")
        assert_that(res_data["event_id"], equal_to(event_id), "response event_id mismatching")
        assert_that(res_data, has_key("item_list"), "no item_list response...")
        for item in res_data["item_list"]:
            assert_that(item, has_key("item_code"), "no item_code response...")
            assert_that(item, has_key("num"), "no num response...")

        res = self.ar_con.get_random_event(latitude, longitude)
        res_data = json.loads(res)

        for event in res_data["events"]:
            if event["event_id"] == event_id:
                assert_that(event["status"], equal_to(1), "response status mismatching")

    def test_open_treasure_box_repeat(self):
        """
        开宝箱失败，重复开启\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        latitude = 26.092
        longitude = 119.314
        event_id = ""

        res = self.ar_con.get_random_event(latitude, longitude)
        res_data = json.loads(res)
        for event in res_data["events"]:
            if event["status"] == 2:
                event_id = event["event_id"]
                break
        game_result = 1
        self.ar_con.open_treasure_box(event_id, game_result)
        res = self.ar_con.open_treasure_box(event_id, game_result)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_TREASURE_BOX_HAD_OPENED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_TREASURE_BOX_HAD_OPENED["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    unittest.main()
