# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
from api_call.message.err_code import *
import json
from cof.rand import CoRand


class ScanFaceTest(unittest.TestCase):
    """
    人脸扫描
    """
    
    def setUp(self):
        print 'start run ScanFace test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "scanFace"
        self.account_id = 100861
    
    def tearDown(self):
        print 'ScanFace test complete.....close socket'

    def test_scan_face_advance_with_glass(self):
        """
        人脸扫描--使用高级扫描卡,戴眼镜==》高级扫描次数-1,出人脸宠,自定义命名无效\
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
        scan_advance_before = res_data["scan_advance"]
        scan_advance = CoRand.get_rand_int(1, 10000)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_true/"+str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", scan_advance)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        assert_that(res_data, has_key("item_code"), "no item_code response...")
        assert_that(res_data, has_key("item_type"), "no item_type response...")
        assert_that(res_data["item_type"], equal_to(3), "item_type mismatch...")
        assert_that(res_data, has_key("item_count"), "no item_count response...")
        assert_that(res_data["item_count"], equal_to(1), "item_count mismatch...")
        assert_that(res_data, has_key("total_count"), "no total_count response...")
        assert_that(res_data, has_key("has_glass"), "no has_glass response...")
        assert_that(res_data["has_glass"], equal_to(1), "response has_glass mismatch...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
        assert_that(res_data["scan_advance"], equal_to(scan_advance_before-1), "scan_advance mismatch...")
        item_id = res_data["item_id"]
        self.ar_con.capture_pet(item_id)
        res = self.ar_con.get_pet_info(item_id, user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("name"), "no name response...")
        assert res_data["name"] != "la", "宠物名称错误"

    def test_scan_face_advance_no_glass(self):
        """
        人脸扫描--使用高级扫描卡,不戴眼镜,高级扫描次数-1,出人脸宠\
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
        scan_advance_before = res_data["scan_advance"]
        scan_advance = CoRand.get_rand_int(1, 10000)
        photo_id = CoRand.get_rand_int(1, 10)
        url = "http://192.168.239.119:807/ARTest/glass_false/" + str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", scan_advance)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        assert_that(res_data, has_key("item_code"), "no item_code response...")
        assert_that(res_data, has_key("item_type"), "no item_type response...")
        assert_that(res_data["item_type"], equal_to(3), "item_type mismatch...")
        assert_that(res_data, has_key("item_count"), "no item_count response...")
        assert_that(res_data, has_key("total_count"), "no total_count response...")
        assert_that(res_data, has_key("has_glass"), "no has_glass response...")
        assert_that(res_data["has_glass"], equal_to(0), "response has_glass mismatch...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")
        assert_that(res_data["scan_advance"], equal_to(scan_advance_before-1), "scan_advance mismatch...")

    def test_scan_face_normal(self):
        """
        人脸扫描--使用普通扫描卡,普通扫描次数-1,可以生成灵魂宠、原生宠、金币\
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
        res = self.ar_con.scan_face(url, "la", 0)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_type"), "no item_type response...")
        if res_data["item_type"] == 0:
            print "生成灵魂宠"
            assert_that(res_data, has_key("item_id"), "no item_id response...")
            assert_that(res_data, not has_key("item_code"), "灵魂宠没有item_code字段")
            assert_that(res_data, has_key("item_count"), "no item_count response...")
            assert_that(res_data["item_count"], equal_to(1), "item_count mismatch...")
            assert_that(res_data, has_key("total_count"), "no total_count response...")
            assert_that(res_data, not has_key("has_glass"), "no has_glass response...")
            assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
            item_id = res_data["item_id"]
            res = self.ar_con.get_soul_pet_list(user_id)
            res_data = json.loads(res)
            assert_that(res_data[0], has_key("item_id"), "no item_id response...")
            assert_that(res_data[0]["item_id"], equal_to(item_id), "item_id mismatch...")
            assert_that(res_data[0], has_key("item_name"), "no item_name response...")
            assert res_data[0]["item_name"] == "la", "灵魂宠名称错误"
        elif res_data["item_type"] == 1:
            print "生成原生宠"
            assert_that(res_data, has_key("item_id"), "no item_id response...")
            assert_that(res_data, has_key("item_code"), "no item_code response...")
            assert_that(res_data, has_key("item_count"), "no item_count response...")
            assert_that(res_data, has_key("total_count"), "no total_count response...")
            assert_that(res_data, not has_key("has_glass"), "no has_glass response...")
            assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")
            item_id = res_data["item_id"]
            res = self.ar_con.get_protozoan_list(user_id)
            res_data = json.loads(res)
            assert_that(res_data[0], has_key("item_id"), "no item_id response...")
            assert_that(res_data[0]["item_id"], equal_to(item_id), "item_id mismatch...")
            assert_that(res_data[0], has_key("item_name"), "no item_name response...")
            assert res_data[0]["item_name"] != "la", "原生宠名称错误"
        elif res_data["item_type"] == 2:
            print "生成金币"
            assert_that(res_data, has_key("item_id"), "no item_id response...")
            assert_that(res_data, has_key("item_code"), "no item_code response...")
            assert_that(res_data, has_key("item_count"), "no item_count response...")
            assert_that(res_data, has_key("total_count"), "no total_count response...")
            assert_that(res_data, not has_key("has_glass"), "no has_glass response...")
            assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")

    def test_scan_face_without_scan_advance(self):
        """
        人脸扫描--不传scan_advance，默认使用普通扫描卡\
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
        url = "http://192.168.239.119:807/ARTest/glass_false/" + str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la")
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        assert_that(res_data, has_key("item_code"), "no item_code response...")
        assert_that(res_data, has_key("item_type"), "no item_type response...")
        assert res_data["item_type"] != 3, "item_type mismatch..."
        assert_that(res_data, has_key("item_count"), "no item_count response...")
        assert_that(res_data, has_key("total_count"), "no total_count response...")
        assert_that(res_data, not has_key("has_glass"), "no has_glass response...")
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")

    def test_scan_face_scan_advance_less_than_0(self):
        """
        人脸扫描--scan_advance传负数，使用普通扫描卡\
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
        url = "http://192.168.239.119:807/ARTest/glass_false/" + str(photo_id) + ".jpg"
        res = self.ar_con.scan_face(url, "la", -100)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        assert_that(res_data, has_key("item_code"), "no item_code response...")
        assert_that(res_data, has_key("item_type"), "no item_type response...")
        assert res_data["item_type"] != 3, "item_type mismatch..."
        assert_that(res_data, has_key("item_count"), "no item_count response...")
        assert_that(res_data, has_key("total_count"), "no total_count response...")
        assert_that(res_data, not has_key("has_glass"), "no has_glass response...")
        assert_that(res_data, has_key("scan_normal"), "no scan_normal response...")

    def test_scan_face_illegal_url(self):
        """
        人脸扫描--异常情况返回随机的识别结果\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        url = CoRand.randomword(8)
        res = self.ar_con.scan_face(url, "la", 1)
        res_data = json.loads(res)
        assert_that(res_data, has_key("item_id"), "no item_id response...")
        assert_that(res_data, has_key("item_code"), "no item_code response...")
        assert_that(res_data, has_key("scan_advance"), "no scan_advance response...")

    def test_scan_face_without_params(self):
        """
        人脸扫描--请求未带参数\
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

    def test_scan_face_with_error_param(self):
        """
        人脸扫描--url参数名错误\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        json_body = {
            "url12": "http://192.168.19.220/v0.1/static/cscommon/avatar/123456789/123456789.jpg"
        }
        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")




if __name__ == "__main__":
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(ScanFaceTest("test_scan_face_scan_advance_less_than_0"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
