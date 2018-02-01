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


class GetAndGiveFriendEnergyTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetAndGiveFriendEnergy test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getAndGiveFriendsEnergy"
        self.account_id = 100861

    def tearDown(self):
        print 'GetAndGiveFriendEnergy test complete.....close socket'

    def test_get_and_give_friend_energy_success(self):
        """
        一键领取和赠送体力-- 一键赠送和领取所有好友体力\
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
        while number < 11:
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
            print "玩家A同意添加好友" + str(number) + ":"
            self.ar_con.get_rev()
            self.ar_con.deal_add_friend(locals()['user_id_' + str(number)], 1)
            print "好友玩家" + str(number) + "赠送体力给A："
            locals()['self.ar_con' + str(number)].get_rev()
            locals()['self.ar_con' + str(number)].give_friend_energy(user_id)
            number += 1

        print "修改玩家A体力值0，一键赠送和获取体力："
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 0)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_and_give_friends_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_pp"), "返回参数缺少get_pp")
        assert_that(res_data["get_pp"], equal_to(10), "返回参数get_pp数值错误")
        assert_that(res_data, has_key("pp"), "返回参数缺少pp")
        assert_that(res_data["pp"], equal_to(10), "返回参数pp数值错误")
        number = 1
        while number < 11:
            print "好友玩家" + str(number) + "领取体力:"
            self.sql = ModifySql()
            self.sql.update_user(locals()['user_id_' + str(number)], "pp", 10)
            self.ar_con.gm_reload_user_data(locals()['user_id_' + str(number)])
            res = locals()['self.ar_con' + str(number)].get_friend_energy(user_id)
            res_data = json.loads(res)
            assert_that(res_data, has_key("code"), "no code response...")
            assert_that(res_data, has_key("err_msg"), "no err_msg response...")
            assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
            assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
            number += 1

    def test_get_and_give_friend_energy_part_can_give_part_can_not_give(self):
        """
        一键领取和赠送体力--部分好友可赠送体力，部分不可赠送\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建玩家A："
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
        print "玩家A同意添加好友B，并赠送体力："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        self.ar_con.give_friend_energy(user_id_2)
        print "好友B领取体力："
        self.ar_con2.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "pp", 0)
        self.ar_con2.gm_reload_user_data(user_id_2)
        res = self.ar_con2.get_friend_energy(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        print "创建好友玩家C："
        account_id_3 = CoRand.get_rand_int(100001)
        uc_id_3 = CoRand.get_rand_int()
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        res = self.ar_con3.login(account_id_3, "im", uc_id_3)
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        self.ar_con3.add_friend(user_id_1)
        print "玩家A同意添加好友C："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_3, 1)
        print "A一键赠送和获取体力："
        res = self.ar_con.get_and_give_friends_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_pp"), "返回参数缺少get_pp")
        assert_that(res_data["get_pp"], equal_to(0), "返回参数get_pp数值错误")
        assert_that(res_data, has_key("pp"), "返回参数缺少pp")
        assert_that(res_data["pp"], equal_to(50), "返回参数pp数值错误")
        print "好友B领取体力："
        res = self.ar_con2.get_friend_energy(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_ENERGY_HAD_GET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_ENERGY_HAD_GET["err_msg"]), "response msg mismatching...")
        print "好友C领取体力："
        self.ar_con3.get_rev()
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "pp", 0)
        self.ar_con3.gm_reload_user_data(user_id_3)
        res = self.ar_con3.get_friend_energy(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

    def test_get_and_give_friend_energy_no_friends(self):
        """
        一键领取和赠送体力-- 无好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int()
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_and_give_friends_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_pp"), "返回参数缺少get_pp")
        assert_that(res_data["get_pp"], equal_to(0), "返回参数get_pp数值错误")
        assert_that(res_data, has_key("pp"), "返回参数缺少pp")
        assert_that(res_data["pp"], equal_to(50), "返回参数pp数值错误")

    def test_get_and_give_friend_energy_get_part_energy_pp_to_50(self):
        """
        一键领取和赠送体力-- 可领取体力>（50-玩家当前体力），先领取部分体力，剩余体力可下次领取\
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
        while number < 4:
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
            print "玩家A同意添加好友" + str(number) + ":"
            self.ar_con.get_rev()
            self.ar_con.deal_add_friend(locals()['user_id_' + str(number)], 1)
            print "好友玩家" + str(number) + "赠送体力给A："
            locals()['self.ar_con' + str(number)].get_rev()
            locals()['self.ar_con' + str(number)].give_friend_energy(user_id)
            number += 1
        print "修改玩家A体力值48，一键赠送和获取体力："
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 48)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_and_give_friends_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_pp"), "返回参数缺少get_pp")
        assert_that(res_data["get_pp"], equal_to(2), "返回参数get_pp数值错误")
        assert_that(res_data, has_key("pp"), "返回参数缺少pp")
        assert_that(res_data["pp"], equal_to(50), "返回参数pp数值错误")
        print "修改玩家A体力值40，一键获取体力剩余待领取体力："
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 40)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_and_give_friends_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_pp"), "返回参数缺少get_pp")
        assert_that(res_data["get_pp"], equal_to(1), "返回参数get_pp数值错误")
        assert_that(res_data, has_key("pp"), "返回参数缺少pp")
        assert_that(res_data["pp"], equal_to(41), "返回参数pp数值错误")

    def test_get_and_give_friend_energy_get_max_50(self):
        """
        一键领取和赠送体力--每天上限领取50个\
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
        while number < 51:
            print "创建好友玩家"+str(number)+":"
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
            print "玩家A同意添加好友"+str(number)+":"
            self.ar_con.get_rev()
            self.ar_con.deal_add_friend(locals()['user_id_'+str(number)], 1)
            print "好友玩家"+str(number)+"赠送体力给A："
            locals()['self.ar_con' + str(number)].get_rev()
            locals()['self.ar_con' + str(number)].give_friend_energy(user_id)
            number += 1

        print "修改玩家A体力值0，一键获取50体力："
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 0)
        self.ar_con.gm_reload_user_data(user_id)
        self.ar_con.get_and_give_friends_energy()
        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(50), "response pp mismatch...")
        print "创建好友玩家51："
        account_id_51 = CoRand.get_rand_int(100001)
        uc_id_51 = CoRand.get_rand_int()
        self.ar_con51 = ARControl()
        self.ar_con51.connect_server()
        res = self.ar_con51.login(account_id_51, "im", uc_id_51)
        res_data = json.loads(res)
        user_id_51 = res_data["user_id"]
        nick_name_51 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con51.modify_info(nick_name_51)
        self.ar_con51.add_friend(user_id)
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_51, 1)
        print "好友玩家51赠送体力给A："
        self.ar_con51.get_rev()
        self.ar_con51.give_friend_energy(user_id)
        print "修改玩家A体力值0，一键获取第51个玩家赠送体力："
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 0)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_and_give_friends_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_pp"), "返回参数缺少get_pp")
        assert_that(res_data["get_pp"], equal_to(0), "返回参数get_pp数值错误")
        assert_that(res_data, has_key("pp"), "返回参数缺少pp")
        assert_that(res_data["pp"], equal_to(0), "返回参数pp数值错误")
        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(0), "response pp mismatch...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_energy"), "no get_energy response...")
        assert_that(res_data["get_energy"], equal_to(50), "response get_energy mismatch...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetAndGiveFriendEnergyTest("test_get_and_give_friend_energy_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
