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
from api_call.SQL_modify.modify_SQL import ModifySql


class EvilRankListTest(unittest.TestCase):
    def setUp(self):
        print 'start run EvilRankList test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "evilRankList"
        self.account_id = 100861
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'EvilRankList test complete.....close socket'

    def test_evil_rank_list_none(self):
        """
        获取排行榜--无人攻击\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.evil_rank_list(0)
        res_data = json.loads(res)
        assert res_data == [], "response rank_list mismatch..."

    def test_evil_rank_list_success(self):
        """
        获取排行榜--验证恶人榜数据正确性（攻击次数、昵称、通缉、星级等信息）\
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
        print "创建攻击玩家B："
        res = self.ar_con2.login(account_id_2, "im")
        res_data = json.loads(res)
        user_id_2 = res_data["user_id"]
        nick_name_2 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name_2)
        #   获取玩家昵称、星章数等信息
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con2.modify_info(nick_name)
        res = self.ar_con2.scan_face(self.pet_url, "la", 1)
        res_data = json.loads(res)
        item_id_2 = res_data["item_id"]
        self.ar_con2.capture_pet(item_id_2)
        self.ar_con2.set_cultivate_pet(item_id_2)
        part_2 = CoRand.get_rand_int(1, 5)
        self.ar_con2.upgrade_pet_part(part_2)
        self.ar_con2.upgrade_pet_part(part_2)
        #   攻击
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "guidance", 131071)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.sql = ModifySql()
        self.sql.update_user(user_id_2, "lottery_type", 104)
        self.ar_con2.gm_reload_user_data(user_id_2)
        self.ar_con2.attack_pet(part, user_id_1)

        print "A获取恶人榜："
        self.ar_con.get_rev()
        res = self.ar_con.evil_rank_list(0)
        res_data = json.loads(res)
        assert res_data != [], "response rank_list mismatch..."
        users = []
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            users.append(i["user_id"])
        assert user_id_2 in users
        attack_user_index = users.index(user_id_2)
        assert_that(res_data[attack_user_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[attack_user_index]["nick_name"], equal_to(nick_name),
                    "response nick_name mismatch...")
        assert_that(res_data[attack_user_index], has_key("icon"), "no icon response...")
        assert_that(res_data[attack_user_index]["icon"], equal_to("https://www.baidu.com/"),
                    "response icon mismatch...")
        assert_that(res_data[attack_user_index], has_key("star"), "no star response...")
        assert_that(res_data[attack_user_index]["star"], equal_to(2), "response star mismatch...")
        assert_that(res_data[attack_user_index], has_key("attack"), "no attack response...")
        assert_that(res_data[attack_user_index]["attack"], equal_to(1), "response attack mismatch...")
        assert_that(res_data[attack_user_index], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data[attack_user_index]["reward_id"], equal_to(0), "response reward_id mismatch...")
        assert_that(res_data[attack_user_index], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data[attack_user_index]["reward_type"], equal_to(0), "response attack mismatch...")

        print "A悬赏B后获取恶人榜周榜、历史榜："
        self.ar_con.reward_player(0, user_id_2)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        assert_that(res_data["reward_list"][0], has_key("reward_id"), "no reward_id response...")
        reward_id = res_data["reward_list"][0]["reward_id"]
        res = self.ar_con.evil_rank_list(0)
        res_data = json.loads(res)
        assert res_data != [], "response mismatch..."
        users = []
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            users.append(i["user_id"])
        assert user_id_2 in users
        attack_user_index = users.index(user_id_2)
        assert_that(res_data[attack_user_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[attack_user_index]["nick_name"], equal_to(nick_name), "response nick_name mismatch...")
        assert_that(res_data[attack_user_index], has_key("icon"), "no icon response...")
        assert_that(res_data[attack_user_index]["icon"], equal_to("https://www.baidu.com/"), "response icon mismatch...")
        assert_that(res_data[attack_user_index], has_key("star"), "no star response...")
        assert_that(res_data[attack_user_index]["star"], equal_to(2), "response star mismatch...")
        assert_that(res_data[attack_user_index], has_key("attack"), "no attack response...")
        assert_that(res_data[attack_user_index]["attack"], equal_to(1), "response attack mismatch...")
        assert_that(res_data[attack_user_index], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data[attack_user_index]["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data[attack_user_index], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data[attack_user_index]["reward_type"], equal_to(0), "response attack mismatch...")

        res = self.ar_con.evil_rank_list(1)
        res_data = json.loads(res)
        assert res_data != [], "response rank_list mismatch..."
        users = []
        for i in res_data:
            assert_that(i, has_key("user_id"), "no user_id response...")
            users.append(i["user_id"])
        assert user_id_2 in users
        attack_user_index = users.index(user_id_2)
        assert_that(res_data[attack_user_index], has_key("nick_name"), "no nick_name response...")
        assert_that(res_data[attack_user_index]["nick_name"], equal_to(nick_name),
                    "response nick_name mismatch...")
        assert_that(res_data[attack_user_index], has_key("icon"), "no icon response...")
        assert_that(res_data[attack_user_index]["icon"], equal_to("https://www.baidu.com/"),
                    "response icon mismatch...")
        assert_that(res_data[attack_user_index], has_key("star"), "no star response...")
        assert_that(res_data[attack_user_index]["star"], equal_to(2), "response star mismatch...")
        assert_that(res_data[attack_user_index], has_key("attack"), "no attack response...")
        assert_that(res_data[attack_user_index]["attack"], equal_to(1), "response attack mismatch...")
        assert_that(res_data[attack_user_index], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data[attack_user_index]["reward_id"], equal_to(reward_id), "response reward_id mismatch...")
        assert_that(res_data[attack_user_index], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data[attack_user_index]["reward_type"], equal_to(0), "response attack mismatch...")

    def test_evil_rank_list_order(self):
        """
        获取排行榜--验证排行顺序\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print "创建玩家A："
        account_id_1 = CoRand.get_rand_int(100001)
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
        part = 1
        while part != 6:
            self.ar_con.upgrade_pet_part(part)
            part += 1
        self.ar_con.close()
        print "创建攻击玩家B,攻击一次："
        self.ar_con2 = ARControl()
        self.ar_con2.connect_server()
        account_id_2 = CoRand.get_rand_int(100001)
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
        self.ar_con2.attack_pet(1, user_id_1)
        print "创建攻击玩家C，攻击三次："
        self.ar_con3 = ARControl()
        self.ar_con3.connect_server()
        account_id_3 = CoRand.get_rand_int(100001)
        res = self.ar_con3.login(account_id_3, "im")
        res_data = json.loads(res)
        user_id_3 = res_data["user_id"]
        nick_name_3 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con3.modify_info(nick_name_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "guidance", 131071)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(2, user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(2, user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_3, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_3)
        self.ar_con3.attack_pet(3, user_id_1)
        print "创建攻击玩家D，攻击两次："
        self.ar_con4 = ARControl()
        self.ar_con4.connect_server()
        account_id_4 = CoRand.get_rand_int(100001)
        res = self.ar_con4.login(account_id_4, "im")
        res_data = json.loads(res)
        user_id_4 = res_data["user_id"]
        nick_name_4 = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con4.modify_info(nick_name_4)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "guidance", 131071)
        self.ar_con4.gm_reload_user_data(user_id_4)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "lottery_type", 104)
        self.ar_con4.gm_reload_user_data(user_id_4)
        self.ar_con4.attack_pet(4, user_id_1)
        self.sql = ModifySql()
        self.sql.update_user(user_id_4, "lottery_type", 104)
        self.ar_con3.gm_reload_user_data(user_id_4)
        self.ar_con4.attack_pet(4, user_id_1)

        print "玩家A获取恶人榜："
        self.ar_con.connect_server()
        res = self.ar_con.login(account_id_1, "im")
        res_data = json.loads(res)
        user_id_1 = res_data["user_id"]
        self.ar_con.evil_rank_list(1)
        res = self.ar_con.evil_rank_list(0)
        res_data = json.loads(res)
        assert res_data != [], "response rank_list mismatch..."
        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_3), "排序玩家错误")
        assert_that(res_data[0], has_key("attack"), "no attack response...")
        assert_that(res_data[0]["attack"], equal_to(3), "攻击次数错误")
        assert_that(res_data[1], has_key("user_id"), "no user_id response...")
        assert_that(res_data[1]["user_id"], equal_to(user_id_4), "排序玩家错误")
        assert_that(res_data[1], has_key("attack"), "no attack response...")
        assert_that(res_data[1]["attack"], equal_to(2), "攻击次数错误")
        assert_that(res_data[2], has_key("user_id"), "no user_id response...")
        assert_that(res_data[2]["user_id"], equal_to(user_id_2), "排序玩家错误")
        assert_that(res_data[2], has_key("attack"), "no attack response...")
        assert_that(res_data[2]["attack"], equal_to(1), "攻击次数错误")

        print "玩家A悬赏BCD后，追加悬赏D，获取恶人榜："
        self.ar_con.reward_player(0, user_id_2)
        self.ar_con.reward_player(1, user_id_3)
        self.ar_con.pm_set_role_data("rewardNormal", 2)
        self.ar_con.reward_player(0, user_id_4)
        self.ar_con.reward_player(0, user_id_4)
        res = self.ar_con.get_enemy_list()
        res_data = json.loads(res)
        assert_that(res_data, has_key("reward_list"), "no reward_list response...")
        for i in res_data["reward_list"]:
            if i["be_reward_user_id"] == user_id_2:
                reward_id_2 = i["reward_id"]
            elif i["be_reward_user_id"] == user_id_3:
                reward_id_3 = i["reward_id"]
            elif i["be_reward_user_id"] == user_id_4:
                reward_id_4 = i["reward_id"]

        res = self.ar_con.evil_rank_list(1)
        res_data = json.loads(res)
        assert res_data != [], "response rank_list mismatch..."
        assert_that(res_data[0], has_key("user_id"), "no user_id response...")
        assert_that(res_data[0]["user_id"], equal_to(user_id_3), "排序玩家错误")
        assert_that(res_data[0], has_key("attack"), "no attack response...")
        assert_that(res_data[0]["attack"], equal_to(3), "攻击次数错误")
        assert_that(res_data[0], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data[0]["reward_id"], equal_to(reward_id_3), "悬赏令错误")
        assert_that(res_data[0], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data[0]["reward_type"], equal_to(1), "reward_type错误")

        assert_that(res_data[1], has_key("user_id"), "no user_id response...")
        assert_that(res_data[1]["user_id"], equal_to(user_id_4), "排序玩家错误")
        assert_that(res_data[1], has_key("attack"), "no attack response...")
        assert_that(res_data[1]["attack"], equal_to(2), "攻击次数错误")
        assert_that(res_data[1], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data[1]["reward_id"], equal_to(reward_id_4), "悬赏令错误")
        assert_that(res_data[1], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data[1]["reward_type"], equal_to(0), "reward_type错误")
        assert_that(res_data[2], has_key("user_id"), "no user_id response...")
        assert_that(res_data[2]["user_id"], equal_to(user_id_2), "排序玩家错误")
        assert_that(res_data[2], has_key("attack"), "no attack response...")
        assert_that(res_data[2]["attack"], equal_to(1), "攻击次数错误")
        assert_that(res_data[2], has_key("reward_id"), "no reward_id response...")
        assert_that(res_data[2]["reward_id"], equal_to(reward_id_2), "悬赏令错误")
        assert_that(res_data[2], has_key("reward_type"), "no reward_type response...")
        assert_that(res_data[2]["reward_type"], equal_to(0), "reward_type错误")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(EvilRankListTest("test_evil_rank_list_order"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

