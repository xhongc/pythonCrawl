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


class AddFriendTest(unittest.TestCase):
    def setUp(self):
        print 'start run AddFriend test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "addFriend"
        self.account_id = 100861

    def tearDown(self):
        print 'AddFriend test complete.....close socket'

    def test_add_friend_success(self):
        """
        请求添加好友发送成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "玩家1执行操作："
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        print "玩家2执行操作："
        self.ar_con.connect_server()
        uc_id = CoRand.get_rand_int()
        self.ar_con.login(100861, "im", uc_id)
        res = self.ar_con.add_friend(user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_add_friend_without_uc_id(self):
        """
        添加好友--玩家无uc_id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "玩家1执行操作："
        account_id_1 = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        print "玩家2执行操作："
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        res = self.ar_con2.add_friend(user_id_1)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_UCID_INVALID["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_UCID_INVALID["err_msg"]), "response msg mismatching...")

    def test_add_friend_already_added(self):
        """
        已是好友，再次请求添加好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        account_id_2 = CoRand.get_rand_int(100001)
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
        print "玩家1执行操作："
        self.ar_con.get_rev()
        res = self.ar_con.add_friend(user_id_2)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_FRIEND_ALREADY_EXISTED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_FRIEND_ALREADY_EXISTED["err_msg"]), "response msg mismatching...")

    def test_add_friend_request_repeat(self):
        """
        已经请求加好友了，再次请求\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()

        print "创建玩家2后离线："
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.close()
        time.sleep(1)
        print "玩家1两次请求添加好友："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)
        self.ar_con.add_friend(user_id_2)

        print "玩家2登陆获取未读消息："
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        res = self.ar_con2.get_unread_msg()
        res_data = json.loads(res)
        assert_that(res_data, has_length(1), "response length mismatch...")
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
            assert_that(i["msg"], has_key("type"), "no op response...")
            assert_that(i["msg"]["type"], equal_to(1), "response op mismatch...")

        self.ar_con2.deal_add_friend(user_id_1, 1)
        print "玩家2重复处理好友请求"
        res = self.ar_con2.deal_add_friend(user_id_1, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_REQUEST_HAD_DEAL["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_REQUEST_HAD_DEAL["err_msg"]), "response msg mismatching...")

    def test_add_friend_mutual_request(self):
        """
        A请求B加好友，B也请求A加好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()

        print "创建玩家B："
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        print "创建玩家A，向B申请添加好友："
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)

        print "玩家B也向A申请添加好友："
        self.ar_con2.get_rev()
        self.ar_con2.add_friend(user_id_1)
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        res = self.ar_con.deal_add_friend(user_id_2, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data, has_key("convid"), "no convid response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response code mismatching...")
        print "B再次处理添加好友请求："
        self.ar_con2.get_rev()
        res = self.ar_con2.deal_add_friend(user_id_1, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_FRIEND_ALREADY_EXISTED["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_FRIEND_ALREADY_EXISTED["err_msg"]), "response msg mismatching...")

    def test_add_friend_self(self):
        """
        添加好友--添加自己\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.add_friend(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ALLOW_ADDSELF["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ALLOW_ADDSELF["err_msg"]), "response msg mismatching...")

    def test_add_friend_not_exist(self):
        """
        添加不存在的好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        user_id_not_exist = CoRand.get_rand_int()
        res = self.ar_con.add_friend(user_id_not_exist)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_USER_NOT_EXIST["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_USER_NOT_EXIST["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(AddFriendTest("test_add_friend_mutual_request"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
