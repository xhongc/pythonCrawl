# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.SQL_modify.modify_SQL import ModifySql
from api_call.message.err_code import *
from cof.rand import CoRand


class DrawLotteryTest(unittest.TestCase):
    def setUp(self):
        print 'start run DrawLottery test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "drawLottery"
        self.pet_url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"

    def tearDown(self):
        print 'DrawLottery test complete.....close socket'

    def test_draw_lottery_success(self):
        """
        抽奖成功\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        pp = res_data["pp"]

        res = self.ar_con.draw_lottery()
        res_data = json.loads(res)

        assert_that(res_data, has_key("item"), "no item response...")
        assert_that(res_data, has_key("count"), "no count response...")
        assert_that(res_data, has_key("place"), "no place response...")
        assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
        if res_data["item"] == 102:
            assert_that(res_data, has_key("pp"), "no pp response...")
            assert_that(res_data["pp"], equal_to(pp+9), "pp mismatching...")
        else:
            assert_that(res_data, has_key("pp"), "no pp response...")
            assert_that(res_data["pp"], equal_to(pp-1), "pp mismatching...")

    def test_draw_lottery_large(self):
        """
        50次抽奖，验证抽奖后物品数值\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        pp_before = res_data["pp"]
        coin = res_data["coin"]
        shield = res_data["shield"]
        scan_advance_count = res_data["scan_advance"]
        scan_normal_count = res_data["scan_normal"]
        pp_add = 0

        for i in range(0, 50):
            res = self.ar_con.draw_lottery()
            res_data = json.loads(res)
            assert_that(res_data, has_key("item"), "no item response...")
            assert_that(res_data, has_key("count"), "no count response...")
            if res_data["item"] == 101:
                count = res_data["count"]
                coin += count
            elif res_data["item"] == 102:
                count = res_data["count"]
                pp_add += count
            elif res_data["item"] == 103:
                count = res_data["count"]
                shield += count
                if shield > 3:
                    pp_add += 1
                    shield = 3
            elif res_data["item"] == 106:
                if 'scan_advance' in res_data.keys():
                    count = res_data["count"]
                    scan_advance_count += count
                    assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
                else:
                    count = res_data["count"]
                    scan_normal_count += count
                    assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(pp_before-50+pp_add), "response pp error...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin), "response coin error...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
        assert_that(res_data["scan_advance"], equal_to(scan_advance_count), "response scan_advance error...")
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
        assert_that(res_data["scan_normal"], equal_to(scan_normal_count), "response scan_normal error...")
        assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
        assert_that(res_data, has_key("shield"), "no shield response...")
        assert_that(res_data["shield"], equal_to(shield), "response shield error...")

    def test_draw_lottery_shield_more_than_3(self):
        """
        验证抽到护盾满3个时，再次抽取到护盾，护盾数量不增加，不扣体力\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.connect_server()
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 100)
        self.ar_con.gm_reload_user_data(user_id)
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        pp_before = res_data["pp"]
        coin = res_data["coin"]
        scan_advance_count = res_data["scan_advance"]
        scan_normal_count = res_data["scan_normal"]
        pp_add = 0
        shield_num = 0

        for i in range(0, 100):
            res = self.ar_con.draw_lottery()
            res_data = json.loads(res)
            assert_that(res_data, has_key("item"), "no item response...")
            assert_that(res_data, has_key("count"), "no count response...")
            if res_data["item"] == 101:
                count = res_data["count"]
                coin += count
            elif res_data["item"] == 102:
                count = res_data["count"]
                pp_add += count
            elif res_data["item"] == 106:
                if 'scan_advance' in res_data.keys():
                    count = res_data["count"]
                    scan_advance_count += count
                    assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
                else:
                    count = res_data["count"]
                    scan_normal_count += count
                    assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
            elif res_data["item"] == 103:
                count = res_data["count"]
                shield_num += count
                if shield_num > 3:
                    pp_add += 1
                    shield_num = 3
        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("pp"), "no pp response...")
        assert_that(res_data["pp"], equal_to(pp_before-100+pp_add), "response pp error...")
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin), "response coin error...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
        assert_that(res_data["scan_advance"], equal_to(scan_advance_count), "response scan_advance error...")
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
        assert_that(res_data["scan_normal"], equal_to(scan_normal_count), "response scan_normal error...")
        assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
        assert_that(res_data, has_key("shield"), "no shield response...")
        assert_that(res_data["shield"], equal_to(shield_num), "response shield error...")

    def test_draw_lottery_not_enough_energy(self):
        """
        抽奖失败，体力不足\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.sql = ModifySql()
        self.sql.update_user(user_id, "pp", 0)
        self.ar_con.gm_reload_user_data(user_id)

        res = self.ar_con.draw_lottery()
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ENOUGH_ENERGY["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ENOUGH_ENERGY["err_msg"]), "response msg mismatching...")

    # def test_draw_lottery_reset_timer(self):
    #     """
    #     抽奖,1小时后重置计时器、体力恢复6点\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     user_id = CoRand.get_rand_int(100001)
    #     self.ar_con.login(user_id, "im")
    #     nick_name = CoRand.get_random_word_filter_sensitive(6)
    #     self.ar_con.modify_info(nick_name)
    #     time_before = time.time()
    #     for i in range(0, 30):
    #         self.ar_con.draw_lottery()
    #     res = self.ar_con.get_user_info(user_id)
    #     res_data = json.loads(res)
    #     pp_before = res_data["pp"]
    #     time.sleep(3601)
    #
    #     res = self.ar_con.draw_lottery()
    #     time_after = time.time()
    #     time_interval = int(time_after - time_before)
    #     res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("item"), "no icon response...")
    #     assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
    #     assert_that(res_data["last_pp_regain"], equal_to(time_interval - 3600), "response last_pp_regain error...")
    #     if res_data["item"] == 102:
    #         assert_that(res_data, has_key("pp"), "no nick_name response...")
    #         assert_that(res_data["pp"], equal_to(pp_before+10+5), "pp mismatching...")
    #     else:
    #         assert_that(res_data, has_key("pp"), "no nick_name response...")
    #         assert_that(res_data["pp"], equal_to(pp_before+5), "pp mismatching...")
    #         assert_that(res_data, has_key("last_pp_regain"), "no nick_name response...")

    # def test_draw_lottery_probability(self):
    #     """
    #     抽奖概率统计\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     star_coin_num = 0.0
    #     coin_num = 0.0
    #     energy_num = 0.0
    #     shield_num = 0.0
    #     attack_num = 0.0
    #     steal_num = 0.0
    #     scan_celebrity_num = 0.0
    #     scan_unlock_num = 0.0
    #     user_num = 100
    #     draw_lottery_num = user_num*50
    #     for a in range(0, user_num):
    #         self.ar_con.connect_server()
    #         account_id = CoRand.get_rand_int(100001)
    #         res = self.ar_con.login(account_id, "im")
    #     res_data = json.loads(res)
    #     user_id = res_data["user_id"]
    #         nick_name = CoRand.get_random_word_filter_sensitive(6)
    #         self.ar_con.modify_info(nick_name)
    #         for i in range(0, 50):
    #             res = self.ar_con.draw_lottery()
    #             res_data = json.loads(res)
    #             assert_that(res_data, has_key("item"), "no item response...")
    #             if res_data["item"] == 100:
    #                 star_coin_num += 1
    #             elif res_data["item"] == 101:
    #                 coin_num += 1
    #             elif res_data["item"] == 102:
    #                 energy_num += 1
    #             elif res_data["item"] == 103:
    #                 shield_num += 1
    #             elif res_data["item"] == 104:
    #                 attack_num += 1
    #             elif res_data["item"] == 105:
    #                 steal_num += 1
    #             elif res_data["item"] == 106:
    #                 scan_celebrity_num += 1
    #             elif res_data["item"] == 107:
    #                 scan_unlock_num += 1
    #             else:
    #                 pass
    #     print "总计抽奖次数:" + str(draw_lottery_num)
    #     print "抽取星数金币概率:" + "%.2f%%" % (star_coin_num/draw_lottery_num*100)
    #     print "抽取金币概率:" + "%.2f%%" % (coin_num / draw_lottery_num * 100)
    #     print "抽取能量概率:" + "%.2f%%" % (energy_num / draw_lottery_num * 100)
    #     print "抽取护盾概率:" + "%.2f%%" % (shield_num / draw_lottery_num * 100)
    #     print "抽取攻击概率:" + "%.2f%%" % (attack_num / draw_lottery_num * 100)
    #     print "抽取偷取概率:" + "%.2f%%" % (steal_num / draw_lottery_num * 100)
    #     print "抽取扫描名人概率:" + "%.2f%%" % (scan_celebrity_num / draw_lottery_num * 100)
    #     print "抽取扫描解锁概率:" + "%.2f%%" % (scan_unlock_num / draw_lottery_num * 100)

    def test_draw_lottery_item_100(self):
        """
        验证抽取星数金币\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        self.ar_con.pm_set_role_data("coin", 100000000)
        for i in range(0, 3):
            res = self.ar_con.scan_face(self.pet_url, "la", 1)
            res_data = json.loads(res)
            pet_id = res_data["item_id"]
            self.ar_con.capture_pet(pet_id)
            self.ar_con.set_cultivate_pet(pet_id)
            part = 1
            while part != 6:
                for j in range(0, 5):
                    self.ar_con.upgrade_pet_part(part)
                part += 1

        pet_idx = 4
        star_coin_count = 200

        while pet_idx != 31:
            if pet_idx <= 8:
                star_coin_count = 200
            elif pet_idx >= 9 and pet_idx <= 13:
                star_coin_count = 300
            elif pet_idx >= 14 and pet_idx <= 18:
                star_coin_count = 400
            elif pet_idx >= 19 and pet_idx <= 23:
                star_coin_count = 500
            elif pet_idx >= 24 and pet_idx <= 28:
                star_coin_count = 600
            elif pet_idx >= 29 and pet_idx <= 30:
                star_coin_count = 700

            print "升级到第" + str(pet_idx) + "个养成宠，转盘抽中星数金币为当前星级*" + str(star_coin_count) + ":"
            res = self.ar_con.scan_face(self.pet_url, "la", 1)
            res_data = json.loads(res)
            pet_id = res_data["item_id"]
            self.ar_con.capture_pet(pet_id)
            self.ar_con.set_cultivate_pet(pet_id)
            self.sql = ModifySql()
            self.sql.update_user(user_id, "pp", 50)
            self.ar_con.gm_reload_user_data(user_id)

            res = self.ar_con.get_user_info(user_id)
            res_data = json.loads(res)
            coin = res_data["coin"]
            scan_advance_count = res_data["scan_advance"]
            scan_normal_count = res_data["scan_normal"]
            star = res_data["star"]
            shield = res_data["shield"]
            pp_add = 0

            for m in range(0, 50):
                res = self.ar_con.draw_lottery()
                res_data = json.loads(res)
                assert_that(res_data, has_key("item"), "no item response...")
                assert_that(res_data, has_key("count"), "no count response...")
                if res_data["item"] == 101:
                    count = res_data["count"]
                    coin += count
                    assert_that(res_data, has_key("coin"), "no coin response...")
                elif res_data["item"] == 102:
                    count = res_data["count"]
                    pp_add += count
                    print pp_add
                elif res_data["item"] == 103:
                    count = res_data["count"]
                    shield += count
                    if shield > 3:
                        pp_add += 1
                        shield = 3
                    print pp_add
                elif res_data["item"] == 106:
                    if 'scan_advance' in res_data.keys():
                        count = res_data["count"]
                        scan_advance_count += count
                        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
                    else:
                        count = res_data["count"]
                        scan_normal_count += count
                        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
                elif res_data["item"] == 100:
                    assert_that(res_data["count"], equal_to(star_coin_count))
                    coin += star*star_coin_count
                    assert_that(res_data, has_key("coin"), "no coin response...")

            res = self.ar_con.get_user_info(user_id)
            res_data = json.loads(res)
            assert_that(res_data, has_key("pp"), "no pp response...")
            assert_that(res_data["pp"], equal_to(pp_add), "response pp error...")
            assert_that(res_data, has_key("coin"), "no coin response...")
            assert_that(res_data["coin"], equal_to(coin), "response coin error...")
            assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
            assert_that(res_data["scan_advance"], equal_to(scan_advance_count), "response scan_advance error...")
            assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
            assert_that(res_data["scan_normal"], equal_to(scan_normal_count), "response scan_normal error...")
            assert_that(res_data, has_key("last_pp_regain"), "no last_pp_regain response...")
            self.sql = ModifySql()
            self.sql.update_user(user_id, "coin", 1000000000)
            self.ar_con.gm_reload_user_data(user_id)
            part = 1
            while part != 6:
                for j in range(0, 5):
                    self.ar_con.upgrade_pet_part(part)
                part += 1
            pet_idx += 1


if __name__ == "__main__":
    # unittest.main()
    # # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(DrawLotteryTest("test_draw_lottery_shield_more_than_3"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
