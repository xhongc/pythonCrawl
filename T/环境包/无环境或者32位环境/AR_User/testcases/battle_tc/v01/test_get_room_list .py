# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetRoomListTest(unittest.TestCase):
    """
    获取房间列表
    """

    def setUp(self):
        print 'start run GetRoomList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetRoomList test complete.....close socket'

    def test_get_room_list_success(self):
        """
        获取房间列表成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")

        res = self.ar_con.get_room_list()
        res_data = json.loads(res)

        assert_that(res_data, has_key("list"), "no list response...")
        for room in res_data["list"]:
            assert_that(room, has_key("room_id"), "no room_id response...")
            assert_that(room, has_key("desc"), "no desc response...")
            assert_that(room, has_key("map_id"), "no map_id response...")
            assert_that(room, has_key("player_count"), "no player_count response...")
            assert_that(room, has_key("is_battling"), "no is_battling response...")

if __name__ == "__main__":
    unittest.main()
