# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
import time
from api_call.message.err_code import *
from cof.rand import CoRand


class LeaveRoomTest(unittest.TestCase):
    """
    离开房间
    """

    def setUp(self):
        print 'start run LeaveRoom test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861
        self.room_id = 0
        self.api_name = "leaveRoom"

    def tearDown(self):
        print 'LeaveRoom test complete.....close socket'

    def test_leave_room_success(self):
        """
        离开房间成功\
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
        self.ar_con.set_def_pet_team(pet_member, team_code)

        res = self.ar_con.get_room_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("list"), "no list response...")
        for room in res_data["list"]:
            assert_that(room, has_key("player_count"), "no player_count response...")
            if room["player_count"] == 0:
                self.room_id = room["room_id"]
                break

        self.ar_con.join_room(self.room_id)
        res = self.ar_con.leave_room(self.room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("room_id"), "no room_id response...")
        assert_that(res_data["room_id"], equal_to(self.room_id), "room_id mismatching...")

    def test_leave_room_not_join(self):
        """
        离开未加入的房间\
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
        room_id = res_data["list"][0]["room_id"]

        res = self.ar_con.leave_room(room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("room_id"), "no room_id response...")
        assert_that(res_data["room_id"], equal_to(room_id), "room_id mismatching...")

    # def test_leave_room_without_params(self):
    #     """
    #     离开房间失败，未传房间id\【目前返回{}，待优化】
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     self.ar_con.login(user_id, "im")
    #     nick_name = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name)
    #     json_body = {}
    #     res = self.ar_con.get_res(self.api_name, json_body)
    #     res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_leave_room_error_room_id(self):
        """
        离开房间，错误的房间id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        room_id = CoRand.get_rand_int(100)
        res = self.ar_con.leave_room(room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("room_id"), "no room_id response...")
        assert_that(res_data["room_id"], equal_to(room_id), "room_id mismatching...")

if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(LeaveRoomTest("test_leave_room_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
