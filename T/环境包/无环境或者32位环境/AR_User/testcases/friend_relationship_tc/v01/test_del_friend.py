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


class DelFriendTest(unittest.TestCase):
    def setUp(self):
        print 'start run DelFriend test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "delFriend"
        self.account_id = 100861

    def tearDown(self):
        print 'DelFriend test complete.....close socket'

    def test_del_friend(self):
        """
        删除好友：删除成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        print "玩家B向A请求添加好友："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)
        print "A同意好友请求："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, 1)

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
        print "A删除好友B:"
        res = self.ar_con2.del_friend(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con2.get_friend_list()
        res_data = json.loads(res)
        assert res_data == [], "response mismatch..."

    def test_del_friend_repeat(self):
        """
        删除好友：重复删除\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        print "玩家B向A请求添加好友："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)
        print "A同意好友请求："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, 1)

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
        print "A重复删除好友B:"
        self.ar_con2.del_friend(user_id_1)
        res = self.ar_con2.del_friend(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_FRIEND_INFO["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_FRIEND_INFO["err_msg"]), "response msg mismatching...")
        res = self.ar_con2.get_friend_list()
        res_data = json.loads(res)
        assert res_data == [], "response mismatch..."

    def test_del_friend_not_friend(self):
        """
        删除好友：非好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.del_friend(100861)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_FRIEND_INFO["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_FRIEND_INFO["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(DelFriendTest("test_del_friend"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
