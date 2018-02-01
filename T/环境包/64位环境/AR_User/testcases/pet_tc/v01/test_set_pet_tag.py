# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *
from cof.rand import CoRand


class SetPetTagTest(unittest.TestCase):
    def setUp(self):
        print 'start run SetPetTag test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "setPetTag"

    def tearDown(self):
        print 'SetPetTag test complete.....close socket'

    def test_set_pet_tag_success(self):
        """
        设置宠物备注\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        tag = CoRand.get_random_word_filter_sensitive(25)
        res = self.ar_con.set_pet_tag(item_id, tag)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_pet_info(item_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("tag"), "no tag response...")
        assert_that(res_data["tag"], equal_to(tag), "response tag mismatching...")

    def test_set_pet_tag_chinese(self):
        """
        设置宠物备注--中文\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        tag = CoRand.get_rand_chinese(5)
        res = self.ar_con.set_pet_tag(item_id, tag)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_pet_info(item_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("tag"), "no tag response...")
        assert_that(res_data["tag"], equal_to(tag), "response tag mismatching...")

    def test_set_pet_tag_without_item_id(self):
        """
        设置宠物备注--请求参数缺少item_id\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        tag = CoRand.get_random_word_filter_sensitive(8)
        json_body = {
            "tag": tag
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_set_pet_tag_without_tag(self):
        """
        设置宠物备注--请求参数缺少tag,取消备注\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)

        json_body = {
            "pet_id": item_id
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_pet_info(item_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, not has_key("tag"), "no tag response...")

    def test_set_pet_tag_with_tag_null(self):
        """
        设置宠物备注--tag传空值,取消备注\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        tag = ""
        res = self.ar_con.set_pet_tag(item_id, tag)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")
        res = self.ar_con.get_pet_info(item_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, not has_key("tag"), "no tag response...")

    def test_set_pet_tag_update(self):
        """
        设置宠物备注--修改备注\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        tag_1 = CoRand.get_random_word_filter_sensitive(25)
        tag_2 = CoRand.get_random_word_filter_sensitive(25)
        print "首次备注："
        res = self.ar_con.set_pet_tag(item_id, tag_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        print "再次备注："
        res = self.ar_con.set_pet_tag(item_id, tag_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_pet_info(item_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("tag"), "no tag response...")
        assert_that(res_data["tag"], equal_to(tag_2), "response tag mismatching...")

    def test_set_pet_tag_second_time_tag_null(self):
        """
        设置宠物备注--第一次正常备注，第二次备注tag传空\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        account_id = CoRand.get_rand_int(100001)
        res = self.ar_con.login(account_id, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        nick_name = CoRand.get_random_word_filter_sensitive(6)
        self.ar_con.modify_info(nick_name)
        url = "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        tag_1 = CoRand.get_random_word_filter_sensitive(25)
        tag_2 = ""
        print "首次备注："
        res = self.ar_con.set_pet_tag(item_id, tag_1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        print "再次备注："
        res = self.ar_con.set_pet_tag(item_id, tag_2)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_pet_info(item_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("tag"), "no tag response...")
        assert_that(res_data["tag"], equal_to(tag_2), "response tag mismatching...")


if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(SetPetTagTest("test_set_pet_tag_second_time_tag_null"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
