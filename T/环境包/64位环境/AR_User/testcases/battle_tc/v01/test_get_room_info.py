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


class GetRoomInfoTest(unittest.TestCase):
    """
    获取房间信息
    """

    def setUp(self):
        print 'start run GetRoomInfo test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861
        self.api_name = "getRoomInfo"

    def tearDown(self):
        print 'GetRoomInfo test complete.....close socket'

    def test_get_room_info_success(self):
        """
        获取房间信息成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.get_room_list()
        res_data = json.loads(res)
        room_id = res_data["list"][0]["room_id"]

        res = self.ar_con.get_room_info(room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("room_id"), "no room_id response...")
        assert_that(res_data, has_key("desc"), "no desc response...")
        assert_that(res_data, has_key("map_id"), "no map_id response...")
        assert_that(res_data, has_key("is_battling"), "no is_battling response...")
        assert_that(res_data, has_key("players"), "no players response...")

    def test_get_room_info_notexist(self):
        """
        获取房间信息失败，不存在的房间\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        room_id = CoRand.get_rand_int(4)
        res = self.ar_con.get_room_info(room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_get_room_info_error_room_id(self):
        """
        获取房间信息失败，错误的room_id\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")
        room_id = CoRand.randomword(6)
        res = self.ar_con.get_room_info(room_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    # def test_get_room_info_without_params(self):
    #     """
    #     获取房间信息失败，未传room_id\【目前返回room_id:0的数据，待优化】
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

if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetRoomInfoTest("test_get_room_info_error_room_id"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
