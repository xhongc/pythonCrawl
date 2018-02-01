# coding=utf-8
"""
@author: 'jing'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json


class GetUserCoinTest(unittest.TestCase):
    def setUp(self):
        print 'start run GetUserCoin test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
        self.account_id = 100861

    def tearDown(self):
        print 'GetUserCoin test complete.....close socket'

    def test_get_user_coin_success(self):
        """
        获取玩家金币成功\
        开发：黄良江(900000)\
        测试：林冰晶（791099）
        """
        self.ar_con.login(self.account_id, "im")

        res = self.ar_con.get_user_coin()
        res_data = json.loads(res)

        assert_that(res_data, has_key("coin"), "no energy response...")


if __name__ == "__main__":
    unittest.main()
