# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from api_call.message.err_code import *


class PeopleNearByTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run PeopleNearBy test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.api_name = "peopleNearBy"
    
    def tearDown(self):
        print 'PeopleNearBy test complete.....close socket'
    
    def test_people_near_by_success(self):
        """
        查找附近的人成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
        """
        self.ar_con.login(100861, "im")
        latitude = 26.092
        longitude = 119.314
        
        res = self.ar_con.people_near_by(latitude, longitude)
        res_data = json.loads(res)
        
        for people in res_data:
            assert_that(people, has_key("user_id"), "no user_id response...")
            assert_that(people, has_key("nick_name"), "no nick_name response...")
            assert_that(people, has_key("latitude"), "no latitude response...")
            assert_that(people, has_key("longitude"), "no longitude response...")
            assert_that(people, has_key("icon"), "no icon response...")

    # def test_people_near_by_illegal(self):
    #     """
    #     查找附近的人失败，在经纬度范围之外(纬度-90~90，经度-180~180)\
    #     开发：黄良江(900000)\
    #     测试：林冰晶(791099)
    #     """
    #     self.ar_con.login(100861, "im")
    #     latitude = -180.092
    #     longitude = 361.314
    #
    #     res = self.ar_con.people_near_by(latitude, longitude)
    #     res_data = json.loads(res)
    #
    #     assert_that(res_data, has_key("code"), "no code response...")
    #     assert_that(res_data, has_key("err_msg"), "no err_msg response...")
    #     assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
    #     assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_people_near_by_without_params(self):
        """
        查找附近的人失败，不带参数\
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

    def test_people_near_by_without_latitude(self):
        """
        查找附近的人失败，未传latitude参数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        json_body = {
            "longitude": 119.314
        }

        res = self.ar_con.get_res(self.api_name, json_body)
        res_data = json.loads(res)

        assert_that(res_data, has_key("code"), "no code response...")
        assert_that(res_data, has_key("err_msg"), "no err_msg response...")
        assert_that(res_data["code"], equal_to(EC_INVALID_REQUEST_PARAM["code"]), "response code mismatching...")
        assert_that(res_data["err_msg"], equal_to(EC_INVALID_REQUEST_PARAM["err_msg"]), "response msg mismatching...")

    def test_people_near_by_without_longitude(self):
        """
        查找附近的人失败，未传latitude参数\
        开发：黄良江(900000)\
        测试：林冰晶(791099)
        """
        self.ar_con.login(100861, "im")
        json_body = {
            "latitude": 26.092
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
    # suite.addTest(PeopleNearByTest("test_people_near_by_without_latitude"))
    # suite.addTest(PeopleNearByTest("test_people_near_by_without_longitude"))
    #
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
