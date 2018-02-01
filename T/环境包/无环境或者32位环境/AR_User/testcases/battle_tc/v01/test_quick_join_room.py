# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand


class QuickJoinRoomTest(unittest.TestCase):
    """
    快速加入房间
    """

    def setUp(self):
        print 'start run QuickJoinRoom test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861
        self.room_id = 0

    def tearDown(self):
        if self.room_id != 0:
            self.ar_con.leave_room(self.room_id)
            print 'leave room complete...'
        print 'QuickJoinRoom test complete.....close socket'

    def test_quick_join_success(self):
        """
        快速加入房间成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.quick_join()
        res_data = json.loads(res)

        assert_that(res_data, has_key("room_id"), "no room_id response...")
        self.room_id = res_data["room_id"]

    def test_quick_join_already_join(self):
        """
        快速加入房间,已加入房间\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_room_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("list"), "no list response...")
        for room in res_data["list"]:
            assert_that(room, has_key("player_count"), "no player_count response...")
            if room["player_count"] == 0:
                self.room_id = room["room_id"]
                break
        self.ar_con.join_room(self.room_id)

        res = self.ar_con.quick_join()
        res_data = json.loads(res)

        assert_that(res_data, has_key("room_id"), "no room_id response...")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(QuickJoinRoomTest("test_quick_join_without_pet"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
