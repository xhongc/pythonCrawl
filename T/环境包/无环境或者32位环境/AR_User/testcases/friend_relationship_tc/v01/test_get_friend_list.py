# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
import time
from cof.rand import CoRand
from api_call.message.err_code import *


class GetFriendListTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetFriendList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getFriendList"
        self.account_id = 100861

    def tearDown(self):
        print 'GetFriendList test complete.....close socket'

    def test_get_friend_list_no_friend(self):
        """
        获取好友列表，无好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_friend_list()
        res_data = json.loads(res)

        assert_that(res_data, equal_to([]), "response error...")

    def test_get_friend_list_success(self):
        """
        获取好友列表成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "玩家2执行操作："
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        print "玩家1执行操作："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)
        print "玩家2执行操作："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, 1)
        time.sleep(1)
        self.ar_con2.get_friend_list()
        print "玩家1执行操作："
        self.ar_con.get_rev()
        time.sleep(1)
        res = self.ar_con.get_friend_list()
        res_data = json.loads(res)

        for friend in res_data:
            assert_that(friend, has_key("user_id"), "no user_id response...")
            assert_that(friend["user_id"], equal_to(user_id_2), "response user_id mismatch")
            assert_that(friend, has_key("nick_name"), "no nick_name response...")
            assert_that(friend["nick_name"], equal_to(nick_name_2), "response nick_name mismatch")
            assert_that(friend, has_key("sex"), "no sex response...")
            assert_that(friend["sex"], equal_to(0), "response sex mismatch")
            assert_that(friend, has_key("icon"), "no icon response...")
            assert_that(friend["icon"], equal_to("https://www.baidu.com/"), "response icon mismatch")
            assert_that(friend, has_key("star"), "no star response...")
            assert_that(friend["star"], equal_to(0), "response star mismatch")
            assert_that(friend, has_key("can_attack"), "no can_attack response...")
            assert_that(friend, has_key("attack"), "no attack response...")
            assert_that(friend, has_key("conv_id"), "no conv_id response...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetFriendListTest("test_get_friend_list_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
