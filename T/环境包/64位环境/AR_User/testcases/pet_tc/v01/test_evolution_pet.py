# coding=utf-8
"""
@author: 'wang'
"""
import unittest
from hamcrest import *
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand


class EvolutionPetTest(unittest.TestCase):
    
    def setUp(self):
        print 'start run EvolutionPet test ......connect server'
        self.ar_con = ARControl()
        self.ar_con.connect_server()
    
    def tearDown(self):
        print 'EvolutionPet test complete.....close socket'
    
    def test_evolution_pet_success(self):
        """
        进化宠物成功\
        开发：黄良江(900000)\
        测试：魏春旺(100861)
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
        pet_id = res_data["pet_id"]
        self.ar_con.capture_pet(pet_id)
        res = self.ar_con.get_pet_list(user_id)
        res_data = json.loads(res)
        
        pet_id = res_data[0]["pet_id"]
        res = self.ar_con.get_pet_info(pet_id, user_id)
        res_data = json.loads(res)   

        assert_that(res_data, has_key("pet_id"), "no id response...")
        assert_that(res_data, has_key("user_id"), "no user_id response...")
        assert_that(res_data["user_id"], equal_to(user_id), "user_id not match...")
        assert_that(res_data, has_key("pet_code"), "no pet_code response...")
        assert_that(res_data, has_key("name"), "no name response...")
        assert_that(res_data, has_key("quality"), "no quality response...")
        assert_that(res_data, has_key("evolution_type"), "no evolution_type response...")
        assert_that(res_data, has_key("lookface"), "no lookface response...")
        assert_that(res_data, has_key("power"), "no power response...")
        assert_that(res_data, has_key("level"), "no level response...")
        assert_that(res_data, has_key("exp"), "no exp response...")
        assert_that(res_data, has_key("hp"), "no hp response...")
        assert_that(res_data, has_key("is_capture"), "no isCapture response...")
        assert_that(res_data, has_key("atk"), "no atk response...")
        assert_that(res_data, has_key("hit_rate"), "no hit_rate response...")
        assert_that(res_data, has_key("dodge_rate"), "no dodge_rate response...")
        assert_that(res_data, has_key("crit_rate"), "no crit_rate response...")
        assert_that(res_data, has_key("anti_crit_rate"), "no anti_crit_rate response...")
        assert_that(res_data, has_key("skill1"), "no skill1 response...")
        assert_that(res_data, has_key("skill1_level"), "no skill1_level response...")
        assert_that(res_data, has_key("skill2"), "no skill2 response...")
        assert_that(res_data, has_key("skill2_level"), "no skill2_level response...")
        assert_that(res_data, has_key("skill3"), "no skill3 response...")
        assert_that(res_data, has_key("skill3_level"), "no skill3_level response...")
        assert_that(res_data, has_key("skill4"), "no skill4 response...")
        assert_that(res_data, has_key("skill4_level"), "no skill4_level response...")

if __name__ == "__main__":
    unittest.main()
