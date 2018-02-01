# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
import time
from api_call.SQL_modify.modify_SQL import ModifySql
from api_call.message.err_code import *
from cof.rand import CoRand


class GiveFriendEnergyTest(unittest.TestCase):
    def setUp(self):
        print 'start run GiveFriendEnergy test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "giveFriendEnergy"
        self.account_id = 100861

    def tearDown(self):
        print 'GiveFriendEnergy test complete.....close socket'

    def test_give_friend_energy_success(self):
        """
        赠送体力--当天第一次赠送，赠送成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "玩家A登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        print "创建好友玩家B："
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
        print "玩家A同意添加好友，赠送体力："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        res = self.ar_con.give_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(50), "response pp mismatching...")

    def test_give_friend_energy_again_one_day(self):
        """
        赠送体力--当天已赠送，好友已领取，无法再次赠送\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "玩家A登陆："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        print "创建好友玩家B："
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
        print "玩家A同意添加好友，赠送体力："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        res = self.ar_con.give_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        print "玩家B领取体力："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "pp", 0)
        self.ar_con.gm_reload_user_data(user_id_2)
        self.ar_con2.get_friend_energy(user_id_1)
        print "玩家A再次赠送体力："
        res = self.ar_con.give_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_ENERGY_HAD_GIVE["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_ENERGY_HAD_GIVE["err_msg"]), "response msg mismatching...")

    def test_give_friend_energy_give_more_than_50(self):
        """
        赠送体力--每天赠送体力无上限（测试60次）\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建玩家A："
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        number = 1
        while number < 61:
            print "创建好友玩家" + str(number) + ":"
            locals()['account_id_' + str(number)] = CoRand.get_rand_int(100001)
            locals()['uc_id_' + str(number)] = CoRand.get_rand_int()
            locals()['self.ar_con' + str(number)] = ARControl()
            locals()['self.ar_con' + str(number)].connect_server()
            res = locals()['self.ar_con' + str(number)].login(locals()['account_id_' + str(number)], "im",
                                                              locals()['uc_id_' + str(number)], )
            res_data = json.loads(res)
            locals()['user_id_' + str(number)] = res_data["user_id"]
            locals()['nick_name_' + str(number)] = CoRand.get_random_word_filter_sensitive(6)
            locals()['self.ar_con' + str(number)].modify_info(locals()['nick_name_' + str(number)])
            locals()['self.ar_con' + str(number)].add_friend(user_id)
            print "玩家A同意添加好友" + str(number) + ",并赠送体力:"
            self.ar_con.get_rev()
            self.ar_con.deal_add_friend(locals()['user_id_' + str(number)], 1)
            res = self.ar_con.give_friend_energy(locals()['user_id_' + str(number)])
            res_data = json.loads(res)
            assert_that(res_data, has_key("code"), "no code response...")
            assert_that(res_data, has_key("err_msg"), "no err_msg response...")
            assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
            assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
            number += 1

    def test_give_friend_energy_not_friend(self):
        """
        赠送体力--赠送非好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        res = self.ar_con.give_friend_energy(self.account_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_FRIEND["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_FRIEND["err_msg"]), "response msg mismatching...")

    def test_give_friend_energy_not_exist(self):
        """
        赠送体力--赠送给不存在的玩家\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        user_id = CoRand.get_rand_int(100001)
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.give_friend_energy(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_FRIEND["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_FRIEND["err_msg"]), "response msg mismatching...")

    # def test_give_friend_energy_friend_not_get_after_48_hour(self):
    #     """
    #     赠送体力--好友未领取，48h后可赠送\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     print "玩家A登陆："
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     uc_id_1 = CoRand.get_rand_int()
    #     self.ar_con.login(user_id_1, "im", uc_id_1)
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     print "创建好友玩家B："
    #     account_id_2 = CoRand.get_rand_int(100001)
    #     uc_id_2 = CoRand.get_rand_int()
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     self.ar_con2.login(user_id_2, "im", uc_id_2)
    #     nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con2.modify_info(nick_name_2)
    #     self.ar_con2.add_friend(user_id_1)
    #     print "玩家A同意添加好友，赠送体力："
    #     self.ar_con.get_rev()
    #     self.ar_con.deal_add_friend(user_id_2, 1)
    #     res = self.ar_con.give_friend_energy(user_id_2)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
    #     # time.sleep(17280)
    #     # print "玩家A在48h后再次赠送体力："
    #     # res = self.ar_con.give_friend_energy(user_id_2)
    #     # res_data = json.loads(res)
    #     # assert_that(res_data, has_key("code"), "no code response...")
    #     # assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     # assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
    #     # assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    # def test_get_friend_energy_can_not_get_after_48_hour(self):
    #     """
    #     领取体力--好友赠送体力，48h后不可领取\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     print "玩家A登陆："
    #     account_id_1 = CoRand.get_rand_int(100001)
    #     uc_id_1 = CoRand.get_rand_int()
    #     self.ar_con.login(user_id_1, "im", uc_id_1)
    #     nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name_1)
    #     print "创建好友玩家B："
    #     account_id_2 = CoRand.get_rand_int(100001)
    #     uc_id_2 = CoRand.get_rand_int()
    #     self.ar_con2 = ARControl()
    #     self.ar_con2.connect_server()
    #     self.ar_con2.login(user_id_2, "im", uc_id_2)
    #     nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con2.modify_info(nick_name_2)
    #     self.ar_con2.add_friend(user_id_1)
    #     print "玩家A同意添加好友，赠送体力："
    #     self.ar_con.get_rev()
    #     self.ar_con.deal_add_friend(user_id_2, 1)
    #     res = self.ar_con.give_friend_energy(user_id_2)
    #     res_data = json.loads(res)
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
    #     # time.sleep(17280)
    #     # print "玩家B在48h后领取体力："
    #     # self.ar_con2.get_rev()
    #     # res = self.ar_con2.get_friend_energy(user_id_1)
    #     # res_data = json.loads(res)
    #     # assert_that(res_data, has_key("code"), "no code response...")
    #     # assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     # assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
    #     # assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(GiveFriendEnergyTest("test_give_friend_energy_again_one_day"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
