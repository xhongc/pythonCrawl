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


class GetFriendEnergyTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetFriendEnergy test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getFriendEnergy"
        self.account_id = 100861

    def tearDown(self):
        print 'GetFriendEnergy test complete.....close socket'

    def test_get_friend_energy_pp_less_than_50(self):
        """
        领取体力--体力值小于50，可领取\
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
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        print "玩家B赠送体力:"
        self.ar_con2.get_rev()
        self.ar_con2.give_friend_energy(user_id_1)
        print "A领取体力："
        self.ar_con.pm_set_role_data("pp", 40)
        res = self.ar_con.get_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(41), "response pp mismatch...")

        res = self.ar_con.get_user_info(user_id_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("get_energy"), "no get_energy response...")
        assert_that(res_data["get_energy"], equal_to(1), "response get_energy mismatch...")

    def test_get_friend_energy_pp_50(self):
        """
        领取体力--体力值=50，不可领取\
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
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        print "玩家B赠送体力:"
        self.ar_con2.get_rev()
        self.ar_con2.give_friend_energy(user_id_1)
        print "A领取体力："
        res = self.ar_con.get_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_MAX_ENERGY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_MAX_ENERGY["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(50), "response pp mismatch...")

    def test_get_friend_energy_pp_more_than_50(self):
        """
        领取体力--体力值>50，不可领取\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "玩家A登陆,修改体力值100："
        account_id_1 = CoRand.get_rand_int(100001)
        uc_id_1 = CoRand.get_rand_int()
        res = self.ar_con.login(account_id_1, "im", uc_id_1)
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        nick_name_1 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_1, "pp", 100)
        self.ar_con.gm_reload_user_data(user_id_1)
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
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        print "玩家B赠送体力:"
        self.ar_con2.get_rev()
        self.ar_con2.give_friend_energy(user_id_1)
        print "A领取体力："
        res = self.ar_con.get_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_MAX_ENERGY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_MAX_ENERGY["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(100), "response pp mismatch...")

    def test_get_friend_energy_repeat(self):
        """
        领取体力--重复领取\
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
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)
        print "玩家B赠送体力:"
        self.ar_con2.get_rev()
        self.ar_con2.give_friend_energy(user_id_1)
        print "A重复领取体力："
        self.ar_con.pm_set_role_data("pp", 40)
        self.ar_con.get_friend_energy(user_id_2)
        res = self.ar_con.get_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_ENERGY_HAD_GET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_ENERGY_HAD_GET["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(41), "response pp mismatch...")

    def test_get_friend_energy_friend_not_give(self):
        """
        领取体力--好友未赠送\
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
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_2, 1)

        print "A领取体力："
        self.ar_con.pm_set_role_data("pp", 40)
        res = self.ar_con.get_friend_energy(user_id_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_ENERGY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_ENERGY["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_energy()
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(40), "response pp mismatch...")

    def test_get_friend_energy_not_friend(self):
        """
        领取体力--非好友\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        res = self.ar_con.login(100861, "im")
        res_data = json.loads(res)
        self.user_id = res_data["user_id"]
        self.ar_con.connect_server()

        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 10)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_friend_energy(self.user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_FRIEND["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_FRIEND["err_msg"]), "response msg mismatching...")

    def test_get_friend_energy_max_50(self):
        """
        领取体力--每天上限领取50个\
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
        self.ar_con51.add_friend(user_id)
        print "玩家A同意添加好友："
        self.ar_con.get_rev()
        self.ar_con.deal_add_friend(user_id_51, 1)
        print "好友玩家51赠送体力给A："
        self.ar_con51.get_rev()
        self.ar_con51.give_friend_energy(user_id)
        print "修改玩家A体力值0，获取第51个玩家赠送体力："
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 0)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_friend_energy(user_id_51)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_MAX_GET_ENERGY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_MAX_GET_ENERGY["err_msg"]), "response msg mismatching...")
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
    suite.addTest(GetFriendEnergyTest("test_get_friend_energy_pp_less_than_50"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
