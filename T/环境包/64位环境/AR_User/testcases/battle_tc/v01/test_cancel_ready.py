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


class CancelReadyTest(unittest.TestCase):
    """
    取消战斗准备
    """

    def setUp(self):
        print 'start run CancelReady test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.room_id = 0

    def tearDown(self):
        if self.room_id != 0:
            self.ar_con.leave_room(self.room_id)
            print 'leave room complete...'
        print 'CancelReady test complete.....close socket'

    def test_cancel_ready_success(self):
        """
        取消战斗准备成功\
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
        self.ar_con.ready_battle()

        res = self.ar_con.cancel_ready()
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_cancel_ready_not_join(self):
        """
        取消战斗准备失败，还未加入房间\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        res = self.ar_con.cancel_ready()
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_USER_NOT_JOIN_ANY_ROOM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_USER_NOT_JOIN_ANY_ROOM["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    unittest.main()
