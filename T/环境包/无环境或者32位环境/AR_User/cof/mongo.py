# coding=utf-8

"""
用于访问mongodb数据库

.. doctest:: 

    >>> mg_conn = MongodbConn('192.168.9.105', 27317)
    >>> mg_conn.set_coll('metis_test', 'sys_log')
"""
__author__ = 'linzh'
import pymongo


class MongodbConn(object):
    """
    创建一个到mongodb数据库的连接
    """

    is_cleaned = False

    def __init__(self, host=None, port=None):
        """创建一个到数据库的连接
        :Parameters:
            - `host`:主机名

        .. versionadded:: 1.1.0
           添加清库支持
        """

        self.host = host
        self.port = port
        self.mg_db = None
        self.mg_coll = None
        self.conn = pymongo.Connection(host, port)
        self.db = None
        self.coll = None

    def set_coll(self, mg_db, mg_coll):
        """
        设置数据库和表名
        """
        self.mg_db = mg_db
        self.mg_coll = mg_coll
        self.db = self.conn[self.mg_db]
        self.coll = self.db[self.mg_coll]

    def add(self, data):
        self.coll.insert(data)

    def clear(self):
        self.coll.remove()

    def find_one(self, cond):
        return self.coll.find_one(cond)
