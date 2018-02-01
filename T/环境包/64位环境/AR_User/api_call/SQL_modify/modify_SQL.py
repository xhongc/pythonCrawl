# coding=utf-8
"""
@author: 'jing'
"""
from api_call.SQL_modify.sqlhelper import *
from cof.conf import MyCfg


class ModifySql(object):
    def __init__(self, section_name='test_db'):

        my_cfg = MyCfg('db.ini')
        my_cfg.set_section(section_name)

        self.host = my_cfg.get('host')
        self.port = my_cfg.get('port')
        self.user = my_cfg.get('user')
        self.password = my_cfg.get('password')
        self.sql = MySQLHelper(self.host, self.user, self.password)
        print self.sql.conn

    def update_user(self, user_id, param, data):
        self.sql.selectDb("argame")
        sql = "update ar_user_role set " + param + "=%s where user_id = %s"
        self.sql.update(sql, (data, user_id))
        self.sql.commit()
        self.sql.close()

    def query_account_id(self, user_id):
        self.sql.selectDb("argame")
        sql = "select * from ar_user_account where user_id = " + str(user_id)
        print sql
        result = self.sql.queryRow(sql)
        account_id = int(result[0])
        self.sql.commit()
        self.sql.close()
        return account_id

    def query_user_ids(self, num):
        self.sql.selectDb("argame")
        result = self.sql.queryAll("select * from ar_user_role")
        user_ids = []

        for i in range(0, num):
            user_id = int(result[i]["user_id"])
            user_ids.append(user_id)
        return user_ids


if __name__ == "__main__":
    t = ModifySql()
    test = t.query_user_ids(10)
    print test

