# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand
from api_call.message.err_code import *


class GetSoulListTest(unittest.TestCase):
    """
    获取灵魂宠列表
    """
    
    def setUp(self):
        print 'start run getSoulPetList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861
        self.api_name = "getSoulPetList"
    
    def tearDown(self):
        print 'getSoulPetList test complete.....close socket'

    def test_get_soul_pet_list_success(self):
        """
        获取灵魂宠列表\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/" + str(photo_id) + ".jpg"
        for x in range(0, 10):
            res = self.ar_con.scan_face(url, "la")
            res_data = json.loads(res)
            if res_data["item_type"] == 0:
                assert_that(res_data, has_key("item_id"), "no item_id response...")
                assert_that(res_data, has_key("total_count"), "no total_count response...")
                item_id = res_data["item_id"]
                total_count = res_data["total_count"]

        res = self.ar_con.get_soul_pet_list(user_id)
        res_data = json.loads(res)
        for iteminfo in res_data:
            assert_that(iteminfo, has_key("item_id"), "no item_id response...")
            assert_that(iteminfo["item_id"], equal_to(item_id), "response item_id mismatching...")
            assert_that(iteminfo, has_key("user_id"), "no user_id response...")
            assert_that(iteminfo["user_id"], equal_to(user_id), "response user_id mismatching...")
            assert_that(iteminfo, has_key("item_code"), "no item_code response...")
            assert_that(iteminfo, has_key("item_count"), "no item_count response...")
            assert_that(iteminfo["item_count"], equal_to(total_count), "response item_count mismatching...")
            assert_that(iteminfo, has_key("item_name"), "no item_name response...")
            assert_that(iteminfo["item_name"], equal_to("la"), "response item_name mismatching...")

    def test_get_soul_no_soul_pet(self):
        """
        获取灵魂宠列表--没有灵魂宠\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        res = self.ar_con.get_soul_pet_list(user_id)
        res_data = json.loads(res)
        assert_that(res_data, equal_to([]), "response mismatch...")

    def test_get_soul_other_user_list(self):
        """
        获取灵魂宠列表--获取其他玩家灵魂宠列表\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        print"玩家A获取灵魂："
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/" + str(photo_id) + ".jpg"
        for x in range(0, 10):
            res = self.ar_con.scan_face(url, "la")
            res_data = json.loads(res)
            if res_data["item_type"] == 0:
                assert_that(res_data, has_key("item_id"), "no item_id response...")
                item_id = res_data["item_id"]

        print"玩家B获取玩A的灵魂列表："
        self.ar_con.connect_server()
        self.ar_con.login(100861, "im")
        res = self.ar_con.get_soul_pet_list(user_id)
        res_data = json.loads(res)
        assert_that(res_data, equal_to([]), "response mismatch...")

    def test_get_soul_list_user_id_error(self):
        """
        获取灵魂列表失败--用户id错误\
        开发：黄良江(900000)\
        测试：王 玲(222067)
        """
        account_id = CoRand.get_rand_int(100001)
        self.ar_con.login(account_id, "im")
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        user_id = CoRand.randomword(8)
        json_body = {
            "user_id": user_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, equal_to([]), "response mismatch...")


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetSoulListTest("test_get_soul_pet_list_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
