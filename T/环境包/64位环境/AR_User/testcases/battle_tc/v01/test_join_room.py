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


class JoinRoomTest(unittest.TestCase):
    """
    加入房间
    """

    def setUp(self):
        print 'start run JoinRoom test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "joinRoom"
        self.account_id = 100861
        self.room_id = 0

    def tearDown(self):
        if self.room_id != 0:
            self.ar_con.leave_room(self.room_id)
            print 'leave room complete...'
        print 'JoinRoom test complete.....close socket'

    def test_join_room_success(self):
        """
        加入房间成功\
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
        res = self.ar_con.join_room(self.room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("room_id"), "no room_id response...")
        assert_that(res_data["room_id"], equal_to(self.room_id), "room_id not match...")

    def test_join_room_in_fighting(self):
        """
        加入房间失败，房间正在战斗\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        account_id_3 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()

        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.get_room_list()
        res_data = json.loads(res)
        for room in res_data["list"]:
            assert_that(room, has_key("player_count"), "no player_count response...")
            if room["player_count"] == 0:
                self.room_id = room["room_id"]
                break

        self.ar_con.join_room(self.room_id)
        self.ar_con.ready_battle()
        self.ar_con.get_room_list()

        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.join_room(self.room_id)
        self.ar_con2.ready_battle()
        self.ar_con2.get_room_list()

        res = self.ar_con3.login(account_id_3, "im")
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.join_room(self.room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_ROOM_IS_NOT_IDLE["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_ROOM_IS_NOT_IDLE["err_msg"]), "response msg mismatching...")

    def test_join_room_full(self):
        """
        加入房间失败，房间已满\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        account_id_3 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()

        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.get_room_list()
        res_data = json.loads(res)
        for room in res_data["list"]:
            assert_that(room, has_key("player_count"), "no player_count response...")
            if room["player_count"] == 0:
                self.room_id = room["room_id"]
                break

        self.ar_con.join_room(self.room_id)

        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.join_room(self.room_id)
        self.ar_con2.get_room_list()

        res = self.ar_con3.login(account_id_3, "im")
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.join_room(self.room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_ROOM_IS_NOT_IDLE["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_ROOM_IS_NOT_IDLE["err_msg"]), "response msg mismatching...")

    # def test_join_room_player_fighting(self):
    #     """
    #     加入房间失败，玩家正在战斗\
    #     开发：黄良江(900000)\
    #     测试：林冰晶（791099）
    #     """
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     account_id_2 = CoRand.get_rand_int(100001)
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #
    #     self.ar_con.login(account_id_1, "im")
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     res = self.ar_con.get_room_list()
    #     res_data = json.loads(res)
    #     for room in res_data["list"]:
    #         assert_that(room, has_key("player_count"), "no player_count response...")
    #         if room["player_count"] == 0:
    #             self.room_id = room["room_id"]
    #             break
    #     self.ar_con.join_room(self.room_id)
    #     self.ar_con.ready_battle()
    #
    #     self.ar_con2.login(account_id_2, "im")
    #     nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con2.modify_info(nick_name_2)
    #     self.ar_con2.join_room(self.room_id)
    #     self.ar_con2.ready_battle()
    #
    #     res = self.ar_con2.get_room_list()
    #     res_data = json.loads(res)
    #     for room in res_data["list"]:
    #         assert_that(room, has_key("player_count"), "no player_count response...")
    #         if room["player_count"] == 0:
    #             self.room_id = room["room_id"]
    #             break
    #     # self.ar_con2.get_room_list()
    #     self.ar_con2.join_room(self.room_id)
    #     # res_data = json.loads(res)
    #
    #     # assert_that(res_data, has_key("code"), "no code response...")
    #     # assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     # assert_that(res_data["code"], equal_to(EC_PLAYER_IS_IN_FIGHTING["code"]), "response code mismatching...")
    #     # assert_that(res_data["err_msg"], equal_to(EC_PLAYER_IS_IN_FIGHTING["err_msg"]), "response msg mismatching...")

    # def test_join_room_without_params(self):
    #     """
    #     加入房间失败，未传参数\【目前返回{}，待优化】
    #     开发：黄良江(900000)\
    #     测试：林冰晶（791099）
    #     """
    #     self.ar_con.login(self.user_id, "im")
    #     json_body = {}
    #     res = self.ar_con.get_res(self.api_name, json_body)
    #     res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_join_room_error_room_id(self):
        """
        加入房间失败，房间id错误\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        room_id = CoRand.get_rand_int(100)
        res = self.ar_con.join_room(room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(JoinRoomTest("test_join_room_player_fighting"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
