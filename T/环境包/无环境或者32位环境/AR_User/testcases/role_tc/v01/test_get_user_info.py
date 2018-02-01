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


class GetUserInfoTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run GetUserInfo test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "getUserInfo"
        self.account_id = 100861
    
    def tearDown(self):
        print 'GetUserInfo test complete.....close socket'
    
    def test_get_user_info_own_success(self):
        """
        获取自己的信息成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        uc_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im", uc_id)
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        icon = CoRand.get_random_word_filter_sensitive(16)
        sex = CoRand.get_rand_int(0, 1)
        sign = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name, icon, sex, sign)
        
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "user_id mismatching...")
        assert_that(res_data, has_key("uc_id"), "no uc_id response...")
        assert_that(res_data["uc_id"], equal_to(uc_id), "uc_id mismatching...")
        assert_that(res_data, has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["nick_name"], equal_to(nick_name), "nick_name mismatching...")
        assert_that(res_data, has_key("sex"), "no sex response...")
        assert_that(res_data["sex"], equal_to(sex), "sex mismatching...")
        assert_that(res_data, has_key("icon"), "no icon response...")
        assert_that(res_data["icon"], equal_to(icon), "nick_name mismatching...")
        assert_that(res_data, has_key("sign"), "no sign response...")
        assert_that(res_data["sign"], equal_to(sign), "sign mismatching...")
        assert_that(res_data, has_key("latitude"), "no latitude response...")
        assert_that(res_data, has_key("longitude"), "no longitude response...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data, has_key("can_attack"), "no can_attack response...")
        assert_that(res_data, has_key("lottery_type"), "no lottery_type response...")
        assert_that(res_data, has_key("shield"), "no shield response...")
        assert_that(res_data, has_key("reward_normal"), "no reward_normal response...")
        assert_that(res_data, has_key("reward_advance"), "no reward_advance response...")
        assert_that(res_data, has_key("trumpets"), "no trumpets response...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")

    def test_get_user_info_others_success(self):
        """
        获取其他玩家信息，不返回attack、shield、pp、last_pp_regain等信息\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)

        self.ar_con.connect_server()
        self.ar_con.login(100861, "im")
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("icon"), "no icon response...")
        assert_that(res_data["icon"], equal_to("https://www.baidu.com/"), "icon mismatching...")
        assert_that(res_data, has_key("nick_name"), "no nick_name response...")
        assert_that(res_data["nick_name"], equal_to(nick_name), "nick_name mismatching...")
        assert_that(res_data, has_key("sex"), "no sex response...")
        assert_that(res_data["sex"], equal_to(0), "sex mismatching...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "user_id mismatching...")
        assert_that(res_data, has_key("latitude"), "no latitude response...")
        assert_that(res_data, has_key("longitude"), "no longitude response...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data, has_key("star"), "no star response...")
        assert_that(res_data, has_key("pet_idx"), "no pet_idx response...")
        assert_that(res_data, has_key("pet_id"), "no pet_id response...")
        assert_that(res_data, has_key("can_attack"), "no can_attack response...")
        assert "pp" not in res_data.keys(), "pp over response..."
        assert "last_pp_regain" not in res_data.keys(), "last_pp_regain over response..."
        assert "attack" not in res_data.keys(), "attack over response..."
        assert "shield" not in res_data.keys(), "shield over response..."

    def test_get_user_info_no_exist(self):
        """
        获取不存在的好友信息\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        user_id = 100861234
        
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_FRIEND_INFO["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_FRIEND_INFO["err_msg"]), "response msg mismatching...")
    
    def test_get_user_info_with_error_param(self):
        """
        获取好友信息失败，错误的参数名\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        
        json_body = {
            "usersId": 100861
        } 
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_get_user_info_without_params(self):
        """
        获取好友信息失败，未传参数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")

        json_body = {}
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(GetUserInfoTest("test_get_user_info_others_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
