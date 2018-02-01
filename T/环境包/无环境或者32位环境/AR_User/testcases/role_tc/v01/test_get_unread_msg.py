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
from api_call.SQL_modify.modify_SQL import ModifySql


class GetUnreadMsgTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetUnreadMsg test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getUnReadMsg"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'GetUnreadMsg test complete.....close socket'

    def test_get_unread_msg_add_friend_online(self):
        """
        获取未读消息--添加好友（在线）\
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
        res = self.ar_con2.get_rev()
        res_data = json.loads(res)
        # assert_that(res_data, has_key("type"), "no type response...")
        # assert_that(res_data["type"], equal_to(1), "response type mismatch...")
        # assert_that(res_data, has_key("user_id"), "no user_id response...")
        # assert_that(res_data["user_id"], equal_to(user_id_1), "response type mismatch...")

    def test_get_unread_msg_add_friend_offline(self):
        """
        获取未读消息--添加好友（不在线）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建玩家2后离线："
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.close()
        time.sleep(1)

        print "玩家1向2请求添加好友："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)

        print "玩家2登陆后获取未读消息："
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        res = self.ar_con2.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("type"), "no type response...")
            assert_that(i["msg"]["type"], equal_to(1), "response type mismatch...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_1), "response user_id mismatch...")

    def test_get_unread_msg_deal_add_friend_agree_online(self):
        """
        获取未读消息--同意添加好友（在线）\
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
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data, has_key("op"), "no op response...")
        assert_that(res_data["op"], equal_to(1), "response op mismatch...")
        assert_that(res_data, has_key("convid"), "no convid response...")

    def test_get_unread_msg_deal_add_friend_agree_offline(self):
        """
        获取未读消息--同意添加好友（不在线）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建玩家2："
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)

        print "玩家1向2请求添加好友后离线："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)
        self.ar_con.close()
        time.sleep(1)

        print "玩家2同意好友请求："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, 1)

        print "玩家1登陆后获取消息："
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        res = self.ar_con.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_2), "response user_id mismatch...")
            assert_that(i["msg"], has_key("op"), "no op response...")
            assert_that(i["msg"]["op"], equal_to(1), "response op mismatch...")
            assert_that(i["msg"], has_key("convid"), "no convid response...")

    def test_get_unread_msg_deal_add_friend_refuse_online(self):
        """
        获取未读消息--拒绝添加好友（在线）\
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
        self.ar_con2.deal_add_friend(user_id_1, -1)
        print "玩家1执行操作："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data, has_key("op"), "no op response...")
        assert_that(res_data["op"], equal_to(-1), "response op mismatch...")
        assert_that(res_data, has_key("type"), "no type response...")
        assert_that(res_data["type"], equal_to(2), "response type mismatch...")

    def test_get_unread_msg_deal_add_friend_refuse_offline(self):
        """
        获取未读消息--拒绝添加好友（不在线）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "玩家2执行操作："
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)

        print "玩家1执行操作后离线："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.ar_con.add_friend(user_id_2)
        self.ar_con.close()
        time.sleep(1)

        print "玩家2处理好友请求："
        self.ar_con2.get_rev()
        self.ar_con2.deal_add_friend(user_id_1, -1)

        print "玩家1登陆后获取消息："
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        res = self.ar_con.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_2), "response user_id mismatch...")
            assert_that(i["msg"], has_key("op"), "no op response...")
            assert_that(i["msg"]["op"], equal_to(-1), "response op mismatch...")

    def test_get_unread_msg_no_msg(self):
        """
        无未读消息\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.get_unread_msg()
        res_data = json.loads(res)

        assert_that(res_data, equal_to([]), "response mismatch...")

    # def test_get_unread_msg_coin_steal_online(self):
    #     """
    #     获取未读消息--金币被偷取（在线）\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     res = self.ar_con.login(account_id_1, "im")
    #     res_data = json.loads(res)
    #     user_id_1 = res_data["user_id"]
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_1, "guidance", 131071)
    #     self.ar_con.gm_reload_user_data(user_id_1)
    #     self.sql = ModifySql()
    #     self.sql.update_user(user_id_1, "lottery_type", 105)
    #     self.ar_con.gm_reload_user_data(user_id_1)
    #     print "玩家获取富豪列表："
    #     res = self.ar_con.get_rich_player_list()
    #     res_data = json.loads(res)
    #     user_total_ids = []
    #     coins = []
    #     for i in res_data:
    #         assert_that(i, has_key("user_id"), "no user_id response...")
    #         user_total_ids.append(i["user_id"])
    #         res_info = self.ar_con.get_user_info(i["user_id"])
    #         res_info_data = json.loads(res_info)
    #         coins.append(res_info_data["coin"])
    #     # 获取富豪user_id和coin
    #     rich_user_index = coins.index(max(coins))
    #     rich_user_id = user_total_ids[rich_user_index]
    #     user_ids = [rich_user_id]
    #     print rich_user_id
    #     print "被偷取玩家登录："
    #     self.sql = ModifySql()
    #     rich_account_id = self.sql.query_account_id(rich_user_id)
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     self.ar_con2.login(rich_account_id, "im")
    #     print "玩家捕捉富豪："
    #     self.ar_con.catch_player_list(user_ids)
    #     print "被偷取玩家收到服务端消息："
    #     res = self.ar_con2.get_rev()
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("user_id"), "no user_id response...")
    #     assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
    #     assert_that(res_data, has_key("type"), "no type response...")
    #     assert_that(res_data["type"], equal_to(4), "response type mismatch...")
    #     assert_that(res_data, has_key("steal_time"), "no steal_time response...")
    #     assert_that(res_data, has_key("steal_coin"), "no steal_coin response...")
    #     assert_that(res_data["steal_coin"], equal_to(int(max(coins)*0.7)), "response steal_coin mismatch...")

    def test_get_unread_msg_coin_steal_offline(self):
        """
        获取未读消息--金币被偷取（不在线）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "guidance", 131071)
        self.ar_con.gm_reload_user_data(user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "lottery_type", 105)
        self.ar_con.gm_reload_user_data(user_id_1)
        print "玩家获取富豪列表："
        res = self.ar_con.get_rich_player_list()
        res_data = json.loads(res)
        user_total_ids = []
        coins = []
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            user_total_ids.append(i["user_id"])
            res_info = self.ar_con.get_user_info(i["user_id"])
            res_info_data = json.loads(res_info)
            coins.append(res_info_data["coin"])
        # 获取富豪user_id和coin
        rich_user_index = coins.index(max(coins))
        rich_user_id = user_total_ids[rich_user_index]
        user_ids = [rich_user_id]
        print "玩家捕捉富豪："
        self.ar_con.catch_player_list(user_ids)
        print "被偷取玩家登录："
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        self.ar_con2.login(rich_user_id, "im")
        print "被偷取玩家获取未读消息："
        res = self.ar_con2.get_unread_msg()
        res_data = json.loads(res)
        msg_user_list = []
        if res_data!=[]:
            for i in res_data:
                assert_that(i, has_key("msg"), "no msg response...")
                assert_that(i["msg"], has_key("user_id"), "no user_id response...")
                msg_user_list.append(i["msg"]["user_id"])
            assert user_id_1 in msg_user_list
            msg_index = msg_user_list.index(user_id_1)

            assert_that(res_data[msg_index]["msg"], has_key("type"), "no type response...")
            assert_that(res_data[msg_index]["msg"]["type"], equal_to(4), "response type mismatch...")
            assert_that(res_data[msg_index]["msg"], has_key("steal_time"), "no steal_time response...")
            assert_that(res_data[msg_index]["msg"], has_key("steal_coin"), "no steal_coin response...")
            assert_that(res_data[msg_index]["msg"]["steal_coin"], equal_to(int(max(coins)*0.7)),
                        "response steal_coin mismatch...")
        else:
            pass

    def test_attack_pet_attacked_user_notify_online(self):
        """
        获取未读消息--验证无护盾玩家被攻击通知（在线）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)

        #   第一次攻击
        print "创建玩家B，攻击A："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        print "玩家A获取服务端消息："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("type"), "no type response...")
        assert_that(res_data["type"], equal_to(3), "response type mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data, has_key("attack_time"), "no attack_time response...")
        assert_that(res_data, has_key("part"), "no part response...")
        assert_that(res_data["part"], equal_to(part), "response part mismatch...")
        assert_that(res_data, has_key("level"), "no level response...")
        assert_that(res_data["level"], equal_to(1), "response level mismatch...")
        assert_that(res_data, has_key("status"), "no status response...")
        assert_that(res_data["status"], equal_to(1), "response status mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(1), "response star mismatch...")
        assert_that(res_data, has_key("shield"), "no shield response...")
        assert_that(res_data["shield"], equal_to(0), "response shield mismatch...")

        #   第二次攻击
        print "玩家B第二次攻击A："
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        print "玩家A获取服务端消息："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("type"), "no type response...")
        assert_that(res_data["type"], equal_to(3), "response type mismatch...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data, has_key("attack_time"), "no attack_time response...")
        assert_that(res_data, has_key("part"), "no part response...")
        assert_that(res_data["part"], equal_to(part), "response part mismatch...")
        assert_that(res_data, has_key("level"), "no level response...")
        assert_that(res_data["level"], equal_to(0), "response level mismatch...")
        assert_that(res_data, has_key("status"), "no status response...")
        assert_that(res_data["status"], equal_to(0), "response status mismatch...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data["star"], equal_to(0), "response star mismatch...")
        assert_that(res_data, has_key("shield"), "no shield response...")
        assert_that(res_data["shield"], equal_to(0), "response shield mismatch...")

    def test_attack_pet_attacked_user_notify_offline(self):
        """
        获取未读消息-验证有护盾玩家被攻击通知（不在线）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        account_id_2 = CoRand.get_rand_int(100001)
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        print "创建玩家A后离线："
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "shield", 2)
        self.ar_con.gm_reload_user_data(user_id_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        part = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part)
        self.ar_con.close()
        time.sleep(1)

        print "创建玩家B，攻击A："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        print "玩家A获取未读消息后离线："
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        res = self.ar_con.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_2), "response user_id mismatch...")
            assert_that(i["msg"], has_key("type"), "no type response...")
            assert_that(i["msg"]["type"], equal_to(3), "response type mismatch...")
            assert_that(i["msg"], has_key("attack_time"), "no attack_time response...")
            assert_that(i["msg"], has_key("part"), "no part response...")
            assert_that(i["msg"]["part"], equal_to(part), "response part mismatch...")
            assert_that(i["msg"], has_key("level"), "no level response...")
            assert_that(i["msg"]["level"], equal_to(1), "response level mismatch...")
            assert_that(i["msg"], has_key("status"), "no status response...")
            assert_that(i["msg"]["status"], equal_to(0), "response status mismatch...")
            assert_that(i["msg"], has_key("star"), "no star response...")
            assert_that(i["msg"]["star"], equal_to(1), "response star mismatch...")
            assert_that(i["msg"], has_key("shield"), "no shield response...")
            assert_that(i["msg"]["shield"], equal_to(2), "response shield mismatch...")
        self.ar_con.close()
        time.sleep(1)

        print "玩家B第二次攻击A："
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)
        print "玩家A登陆，获取未读消息："
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        res = self.ar_con.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_2), "response user_id mismatch...")
            assert_that(i["msg"], has_key("type"), "no type response...")
            assert_that(i["msg"]["type"], equal_to(3), "response type mismatch...")
            assert_that(i["msg"], has_key("attack_time"), "no attack_time response...")
            assert_that(i["msg"], has_key("part"), "no part response...")
            assert_that(i["msg"]["part"], equal_to(part), "response part mismatch...")
            assert_that(i["msg"], has_key("level"), "no level response...")
            assert_that(i["msg"]["level"], equal_to(1), "response level mismatch...")
            assert_that(i["msg"], has_key("status"), "no status response...")
            assert_that(i["msg"]["status"], equal_to(0), "response status mismatch...")
            assert_that(i["msg"], has_key("star"), "no star response...")
            assert_that(i["msg"]["star"], equal_to(1), "response star mismatch...")
            assert_that(i["msg"], has_key("shield"), "no shield response...")
            assert_that(i["msg"]["shield"], equal_to(2), "response shield mismatch...")

    def test_get_unread_msg_reward_player_online(self):
        """
        获取未读消息--验证悬赏消息（在线）,包含部件被打坏、打爆\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        print "好友玩家收到消息："
        self.ar_con2.get_rev()

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.get_user_info(user_id_3)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        res = self.ar_con3.upgrade_pet_part(part_3)
        res_data = json.loads(res)
        coin_level_1 = coin_before - res_data["coin"]
        res = self.ar_con3.upgrade_pet_part(part_3)
        res_data = json.loads(res)
        coin_level_2 = coin_before - res_data["coin"] - coin_level_1
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用普通通缉令通缉攻击者："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        self.ar_con.reward_player(0, user_id_3)

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.evil_rank_list(0)

        print "好友玩家收到消息并攻击被悬赏者："
        res = self.ar_con2.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_1), "response user_id mismatch...")
        assert_that(res_data, has_key("be_reward_user_id"), "no be_reward_user_id response...")
        assert_that(res_data["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
        assert_that(res_data, has_key("type"), "no type response...")
        assert_that(res_data["type"], equal_to(6), "response type mismatch...")
        assert_that(res_data, has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_type"], equal_to(0), "response reward_type mismatch...")
        assert_that(res_data, has_key("reward_time"), "no reward_time response...")
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part_3, user_id_3, reward_id)

        print "悬赏者收到消息："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("type"), "no type response...")
        assert_that(res_data["type"], equal_to(5), "response type mismatch...")
        assert_that(res_data, has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_type"], equal_to(0), "response reward_type mismatch...")
        assert_that(res_data, has_key("attack_time"), "no attack_time response...")
        assert_that(res_data, has_key("toll"), "no toll response...")
        assert_that(res_data["toll"], equal_to(int(coin_level_2*0.5)), "response toll mismatch...")

        print "好友玩家再次攻击被悬赏者："
        self.ar_con2.pm_set_role_data("lotteryType", 104)
        self.ar_con2.attack_pet(part_3, user_id_3, reward_id)

        print "悬赏者收到消息："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response user_id mismatch...")
        assert_that(res_data, has_key("reward_id"), "no reward_id response...")
        assert_that(res_data["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data, has_key("type"), "no type response...")
        assert_that(res_data["type"], equal_to(5), "response type mismatch...")
        assert_that(res_data, has_key("reward_type"), "no reward_type response...")
        assert_that(res_data["reward_type"], equal_to(0), "response reward_type mismatch...")
        assert_that(res_data, has_key("attack_time"), "no attack_time response...")
        assert_that(res_data, has_key("toll"), "no toll response...")
        assert_that(res_data["toll"], equal_to(int(coin_level_2 * 0.5)+coin_level_1), "response toll mismatch...")

    def test_get_unread_msg_reward_player_offline(self):
        """
        获取未读消息--验证悬赏消息（不在线）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "悬赏令使用者登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.set_cultivate_pet(item_id_1)
        part_1 = CoRand.get_rand_int(1, 5)
        self.ar_con.upgrade_pet_part(part_1)
        print "创建好友玩家："
        account_id_2 = CoRand.get_rand_int(100001)
        uc_id_2 = CoRand.get_rand_int()
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        self.ar_con2.add_friend(user_id_1)
        print "悬赏令使用者同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        print "好友玩家收到消息后离线："
        self.ar_con2.get_rev()
        self.ar_con2.close()
        time.sleep(1)

        print "创建攻击者玩家："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        res = self.ar_con3.get_user_info(user_id_3)
        res_data = json.loads(res)
        coin_before = res_data["coin"]
        res = self.ar_con3.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_3 = res_data["item_id"]
        self.ar_con3.capture_pet(item_id_3)
        self.ar_con3.set_cultivate_pet(item_id_3)
        part_3 = CoRand.get_rand_int(1, 5)
        res = self.ar_con3.upgrade_pet_part(part_3)
        res_data = json.loads(res)
        coin_after = res_data["coin"]
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(part_1, user_id_1)

        print "悬赏令使用高级通缉令通缉攻击者后离线："
        self.ar_con.get_rev()
        self.ar_con.get_enemy_list()
        self.ar_con.reward_player(1, user_id_3)

        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        self.ar_con.evil_rank_list(0)
        self.ar_con.close()
        time.sleep(1)

        print "好友玩家登陆，获取未读消息并攻击被悬赏者："
        self.ar_con2.connect_server()
        res = self.ar_con2.login(account_id_2, "im", uc_id_2)
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        res = self.ar_con2.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_1), "response user_id mismatch...")
            assert_that(i["msg"], has_key("be_reward_user_id"), "no be_reward_user_id response...")
            assert_that(i["msg"]["be_reward_user_id"], equal_to(user_id_3), "response be_reward_user_id mismatch...")
            assert_that(i["msg"], has_key("type"), "no type response...")
            assert_that(i["msg"]["type"], equal_to(6), "response type mismatch...")
            assert_that(i["msg"], has_key("reward_type"), "no reward_type response...")
            assert_that(i["msg"]["reward_type"], equal_to(1), "response reward_type mismatch...")
            assert_that(i["msg"], has_key("reward_time"), "no reward_time response...")

        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part_3, user_id_3, reward_id)

        print "悬赏者登陆获取未读消息："
        self.ar_con.connect_server()
        self.ar_con.login(account_id_1, "im", uc_id_1)
        res = self.ar_con.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_2), "response user_id mismatch...")
            assert_that(i["msg"], has_key("type"), "no type response...")
            assert_that(i["msg"]["type"], equal_to(5), "response type mismatch...")
            assert_that(i["msg"], has_key("attack_time"), "no attack_time response...")
            assert_that(i["msg"], has_key("reward_type"), "no reward_type response...")
            assert_that(i["msg"]["reward_type"], equal_to(1), "response reward_type mismatch...")
            assert_that(i["msg"], has_key("reward_id"), "no reward_id response...")
            assert_that(i["msg"]["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
            assert_that(i["msg"], has_key("toll"), "no toll response...")
            assert_that(i["msg"]["toll"], equal_to(int((coin_before-coin_after)*0.5)), "response toll mismatch...")

    def test_get_unread_msg_del_friend_online(self):
        """
        获取未读消息：被好友删除（在线）\
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
        print "B收到好友同意消息："
        self.ar_con.get_rev()
        self.ar_con2.get_friend_list()

        print "A删除好友B:"
        res = self.ar_con2.del_friend(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        print "B收到消息："
        res = self.ar_con.get_rev()
        res_data = json.loads(res)
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id_2), "response user_id mismatch...")

    def test_get_unread_msg_del_friend_offline(self):
        """
        获取未读消息：被好友删除（不在线）\
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
        print "B收到好友同意消息后离线："
        self.ar_con.get_rev()
        self.ar_con.get_friend_list()
        self.ar_con.close()
        time.sleep(1)

        print "A删除好友B:"
        res = self.ar_con2.del_friend(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        print "B登陆获取未读消息："
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        res = self.ar_con.get_unread_msg()
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        for i in res_data:
            assert_that(i, has_key("msg"), "no msg response...")
            assert_that(i["msg"], has_key("user_id"), "no user_id response...")
            assert_that(i["msg"]["user_id"], equal_to(user_id_2), "response user_id mismatch...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetUnreadMsgTest("test_get_unread_msg_no_msg"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
