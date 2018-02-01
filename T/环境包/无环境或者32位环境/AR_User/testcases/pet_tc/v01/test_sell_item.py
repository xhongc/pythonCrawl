# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
from api_call.message.err_code import *
import json
from cof.rand import CoRand


class SellItemTest(unittest.TestCase):
    """
    出售物品
    """

    def setUp(self):
        print 'start run SellItem test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "sellItem"
        self.account_id = 100861

    def tearDown(self):
        print 'SellItem test complete.....close socket'

    def test_sell_item_face_pet(self):
        """
        出售物品--单个人脸宠\
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
        coin_before = res_data["coin"]
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        res = self.ar_con.sell_item(item_id, 3, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("gain_coin"), "no gain_coin response...")
        gain_coin = res_data["gain_coin"]
        assert_that(res_data, has_key("coin"), "no coin response...")
        assert_that(res_data["coin"], equal_to(coin_before+gain_coin), "coin mismatch...")
        assert_that(res_data, has_key("item_count"), "no item_count response...")
        assert_that(res_data["item_count"], equal_to(0), "item_count mismatch...")

    def test_sell_item_protozoan_pet(self):
        """
        出售物品--单个原生宠/灵魂宠\
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
        coin_before = res_data["coin"]
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 0)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_type"), "no item_type response...")
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]

        if res_data["item_type"] == 0:
            print "出售灵魂宠："
            res = self.ar_con.sell_item(item_id, 0, 1)
            res_data = json.loads(res)
            assert_that(res_data, has_key("gain_coin"), "no gain_coin response...")
            gain_coin = res_data["gain_coin"]
            assert_that(res_data, has_key("coin"), "no coin response...")
            assert_that(res_data["coin"], equal_to(coin_before + gain_coin), "coin mismatch...")
            assert_that(res_data, has_key("item_count"), "no item_count response...")
            assert_that(res_data["item_count"], equal_to(0), "item_count mismatch...")

        elif res_data["item_type"] == 1:
            print "出售原生宠"
            res = self.ar_con.sell_item(item_id, 1, 1)
            res_data = json.loads(res)
            assert_that(res_data, has_key("gain_coin"), "no gain_coin response...")
            gain_coin = res_data["gain_coin"]
            assert_that(res_data, has_key("coin"), "no coin response...")
            assert_that(res_data["coin"], equal_to(coin_before + gain_coin), "coin mismatch...")
            assert_that(res_data, has_key("item_count"), "no item_count response...")
            assert_that(res_data["item_count"], equal_to(0), "item_count mismatch...")

    def test_sell_item_no_pet(self):
        """
        出售物品--无可出售宠物\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        res = self.ar_con.sell_item(8013, 3, 1)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")

    def test_sell_item_face_pet_not_catch(self):
        """
        出售物品--未捕捉的人脸宠，不可出售\
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
        coin_before = res_data["coin"]
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]
        res = self.ar_con.sell_item(item_id, 3, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_PET_NOT_CAPTURE["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_PET_NOT_CAPTURE["err_msg"]), "response msg mismatching...")

    def test_sell_item_face_pet_not_enough(self):
        """
        出售物品--人脸宠个数不足\
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
        coin_before = res_data["coin"]
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id_1 = res_data["item_id"]
        self.ar_con.capture_pet(item_id_1)
        self.ar_con.get_pet_list(user_id)
        res = self.ar_con.sell_item(item_id_1, 3, 2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_ENOUGH_ITEM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_ENOUGH_ITEM["err_msg"]), "response msg mismatching...")

    def test_sell_item_multiple(self):
        """
        出售物品--多个灵魂宠\
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
        coin_before = res_data["coin"]
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        soul_pet_num = 0
        for i in range(0, 10):
            res = self.ar_con.scan_face(url, "la", 0)
            res_data = json.loads(res)
            if res_data["item_type"] == 0:
                assert_that(res_data, has_key("item_id"), "no item_id response...")
                item_id_soul = res_data["item_id"]
                soul_pet_num += 1
        if soul_pet_num != 0:
            res = self.ar_con.sell_item(item_id_soul, 0, soul_pet_num)
            res_data = json.loads(res)
            assert_that(res_data, has_key("gain_coin"), "no gain_coin response...")
            assert_that(res_data["gain_coin"], equal_to(3000*soul_pet_num), "gain_coin mismatch...")
            assert_that(res_data, has_key("coin"), "no coin response...")
            assert_that(res_data, has_key("item_count"), "no item_count response...")
            assert_that(res_data["item_count"], equal_to(0), "item_count mismatch...")

    def test_sell_item_cultivate(self):
        """
        出售物品--养成中的养成宠不可出售\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        self.ar_con.set_cultivate_pet(item_id)
        res = self.ar_con.sell_item(item_id, 3, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_COMPLETE_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_COMPLETE_PET["err_msg"]), "response msg mismatching...")

    def test_sell_item_without_params(self):
        """
        出售物品--请求未带参数\
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

    def test_sell_item_without_item_id(self):
        """
        出售物品--缺少参数item_id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(self.account_id, "im")
        json_body = {
            "item_type": 0,
            "item_count": 1
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_sell_item_without_item_type(self):
        """
        出售物品--缺少参数item_type\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/" + str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        json_body = {
            "item_id": item_id,
            "item_count": 1
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_sell_item_without_item_count(self):
        """
        出售物品--缺少参数item_count\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/" + str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        json_body = {
            "item_id": item_id,
            "item_type": 3
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_sell_item_face_pet_error_item_type(self):
        """
        出售物品--人脸宠,物品类型错误\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        res = self.ar_con.sell_item(item_id, 2, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_UNKNOWN_ITEM_TYPE["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_UNKNOWN_ITEM_TYPE["err_msg"]), "response msg mismatching...")

    def test_sell_item_that_item_id_not_own(self):
        """
        出售物品--非玩家物品id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        print"玩家A获取人脸宠："
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.239.119:807/ARTest/glass_true/1.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)

        print "玩家B出售A的人脸宠："
        self.ar_con.connect_server()
        self.ar_con.login(self.account_id, "im")
        res = self.ar_con.sell_item(item_id, 3, 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_NOT_FOUND_PET["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_NOT_FOUND_PET["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(SellItemTest("test_sell_item_face_pet_not_enough"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
