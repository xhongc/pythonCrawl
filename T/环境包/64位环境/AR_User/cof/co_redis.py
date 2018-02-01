# coding=utf-8

"""
redis操作库
"""

__author__ = 'Administrator'

import redis


class CoRedis(object):
    def __init__(self, host, port, password="", db=0):
        #conn = redis.Redis(host='192.168.94.26', port=6379, db=1)
        conn = redis.Redis(host=host, port=port, db=db, password=password)
        self.conn = conn

    def enc_str(self):
        """
        将字符串进行加密后，作为一个key存储
        """
        pass

    def get(self, k):
        """
        获取指定key的
        """
        return self.conn.get(k)

    def set(self, k, v):
        """

        """
        self.conn.set(k, v)

        pass


if __name__ == "__main__":
    r = CoRedis()
    r.set("hello", "world")
    print r.get("hello")
