# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *


class UpdateLocationTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run UpdateLocation test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "updateLocation"
    
    def tearDown(self):
        print 'UpdateLocation test complete.....close socket'
    
    def test_update_location_success(self):
        """
        上传位置信息成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        res = self.ar_con.login(100861, "im")
        res_data = json.loads(res)
        user_id = res_data["user_id"]
        latitude = 26.092
        longitude = 119.314
        
        res = self.ar_con.update_location(latitude, longitude)
        res_data = json.loads(res)
        
        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_SUCCESS["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_SUCCESS["err_msg"]), "response msg mismatching...")

        res = self.ar_con.get_user_info(user_id)
        res_data = json.loads(res)
        assert_that(res_data, has_key("latitude"), "no code response...")
        assert_that(res_data, has_key("longitude"), "no err_msg response...")
        assert_that(res_data["latitude"], equal_to(latitude), "response code mismatching...")
        assert_that(res_data["longitude"], equal_to(longitude), "response msg mismatching...")

    def test_update_location_without_params(self):
        """
        上传位置信息失败，不带参数\
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

    # def test_update_location_illegal(self):
    #     """
    #     上传位置信息失败，在经纬度范围之外(纬度-90~90，经度-180~180)\【目前未对值做限制】
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     self.ar_con.login(100861, "im")
    #     latitude = -180.092
    #     longitude = 361.314
    #
    #     res = self.ar_con.update_location(latitude, longitude)
    #     res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")


if __name__ == "__main__":
    # unittest.main()
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(UpdateLocationTest("test_update_location_success"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
