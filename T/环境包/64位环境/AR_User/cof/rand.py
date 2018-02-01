# coding=utf-8

"""
生成各种符合要求的随机串
"""
__author__ = 'Administrator'

import random
import string
import uuid
import sys
from api_call.sensitive_word.illegal_word import *


class CoRand(object):
    def __init__(self):
        pass

    @staticmethod
    def randomword(length):
        return ''.join(random.choice(string.lowercase) for i in range(length))

    @staticmethod
    def uuid(length=16):
        uuid_str = str(uuid.uuid4())
        print uuid_str
        uuid_str = uuid_str.replace('-', '')

        return uuid_str[:16]

    @staticmethod
    def get_rand_num(num, start=0, end=100):
        serial_arr = list()
        rand_arr = list()
        i = start
        while i <= end:
            serial_arr.append(i)
            i += 1

        for i in range(num):
            rnd_num = random.choice(serial_arr)
            rand_arr.append(rnd_num)
            serial_arr.remove(rnd_num)

        return rand_arr

    @staticmethod
    def get_rand_int(start=1, end=sys.maxint):
        rnd_int = random.randint(start, end)
        return rnd_int

    @staticmethod
    def get_rand_chinese(length):
        return ''.join(random.choice(unichr(random.randint(0x4E00, 0x9FA5))) for i in range(length))

    @staticmethod
    def get_rand_combination(char_length):
        rand_int = str(random.randint(0, 99))
        rand_str = CoRand.randomword(1)
        rand_char = CoRand.get_rand_chinese(char_length)
        return string.join(random.sample([rand_str, rand_int, rand_char], 3)).replace(" ", "")

    @staticmethod
    def get_random_word_filter_sensitive(length):
        random_word = CoRand.randomword(length)
        result = judge_sensitive_word(random_word)
        while result is False:
            random_word = CoRand.randomword(length)
            result = judge_sensitive_word(random_word)
        return random_word


if __name__ == "__main__":
#     rand_o = CoRand()
#     # 生成10个字符长度的字符串
#     print rand_o.randomword(10)
#     print rand_o.uuid()
#     print rand_o.get_rand_num(5, end=9)
#     print CoRand.get_rand_int()
    print CoRand.get_random_word_filter_sensitive(6)




