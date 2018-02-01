# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
from api_call.sensitive_word.illegal_word import *
import json
from api_call.message.err_code import *
from cof.rand import CoRand


class DealAddFriendTest(unittest.TestCase):
    def setUp(self):
        print 'start run DealAddFriend test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "dealAddFriend"
        self.account_id = 100861

    def tearDown(self):
        print 'AddFriend test complete.....close socket'

    def test_deal_add_friend_agree(self):
        """
        同意添加好友请求成功\
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
        op = 1
        res = self.ar_con2.deal_add_friend(user_id_1, op)
        res_data = json.loads(res)

        assert_that(res_data, has_key("convid"), "no convid response...")

        res = self.ar_con2.get_friend_list()
        res_data = json.loads(res)
        for friend in res_data:
            assert_that(friend, has_key("user_id"), "no user_id response...")
            assert_that(friend["user_id"], equal_to(user_id_1), "response user_id mismatch")
            assert_that(friend, has_key("nick_name"), "no nick_name response...")
            assert_that(friend, has_key("sex"), "no sex response...")
            assert_that(friend, has_key("icon"), "no icon response...")
            assert_that(friend, has_key("star"), "no star response...")
            assert_that(friend["star"], equal_to(0), "response user_id mismatch")

    def test_deal_add_friend_refuse(self):
        """
        拒绝添加好友请求成功\
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
        op = -1
        res = self.ar_con2.deal_add_friend(user_id_1, op)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con2.get_friend_list()
        res_data = json.loads(res)

        assert_that(res_data, equal_to([]), "response mismatch...")

    def test_deal_add_friend_error_user(self):
        """
        处理添加好友请求，用户未请求\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.deal_add_friend(100861, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_REQUEST_NOT_FOUND["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_REQUEST_NOT_FOUND["err_msg"]), "response msg mismatching...")

    def test_deal_add_friend_error_op(self):
        """
        处理添加好友请求，op参数取值错误\
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
        op = 123
        res = self.ar_con2.deal_add_friend(user_id_1, op)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_deal_add_friend_without_params(self):
        """
        处理添加好友请求，不带参数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    # def test_deal_add_friend_repeat(self):
    #     """
    #     处理添加好友，重复处理\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     account_id_2 = CoRand.get_rand_int(100001)
    #     uc_id_1 = CoRand.get_rand_int()
    #     uc_id_2 = CoRand.get_rand_int()
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     print "玩家2执行操作："
    #     self.ar_con2.login(user_id_2, "im", uc_id_2)
    #     nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con2.modify_info(nick_name_2)
    #     print "玩家1执行操作："
    #     self.ar_con.login(user_id_1, "im", uc_id_1)
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     self.ar_con.add_friend(user_id_2)
    #     print "玩家2执行操作："
    #     self.ar_con2.get_rev()
    #     op = 1
    #     self.ar_con2.deal_add_friend(user_id_1, op)
    #     self.ar_con2.deal_add_friend(user_id_1, op)
    #     self.ar_con2.deal_add_friend(user_id_1, op)
    #     self.ar_con2.deal_add_friend(user_id_1, op)

if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(DealAddFriendTest("test_deal_add_friend_error_user"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
