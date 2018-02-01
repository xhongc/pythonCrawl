# coding=utf-8
__author__ = 'Administrator'

import MySQLdb
import os

import cof.conf as cofConf
import cof.file as cofFile


class MysqlConn(object):
    def __init__(self, host="", port=3306, user="", password=""):
        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = password

        self.dbname = ""
        self.db = None
        self.cursor = None
        self.table = ""
        self.db_cfg_type = ""

    def get_connection(self, db):
        self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=db)

        self.cursor = self.db.cursor()

        pre_sql = "SET NAMES 'utf8'"
        self.exec_sql(pre_sql)
        return self

    def set_db_cfg_type(self, cfg_type):
        """
        设置数据库配置类型
        development
        debug
        production
        """
        self.db_cfg_type = cfg_type

    def set_db_cfg(self, cfg_name='mydb', sec_name='mysql'):
        """
        set_db_cfg_type 设置类型

        .. doctest::
            mysql_o.set_db_cfg_type('debug')
            mysql_o.set_db_cfg()

        """
        # 获取数据库配置
        app_loc = cofFile.get_app_loc()

        if not self.db_cfg_type:
            cfg_obj = cofConf.MyCfg(app_loc + os.sep + 'cfgtype.ini')
            cfg_obj.set_section('cfg')
            cfg_type = cfg_obj.get('type')
        else:
            cfg_type = self.db_cfg_type

        db_cfg_obj = cofConf.MyCfg(os.sep + cfg_name + '.ini')
        db_cfg_obj.set_section(sec_name)

        self.host = db_cfg_obj.get('host')
        self.port = int(db_cfg_obj.get('port'))
        self.user = db_cfg_obj.get('user')
        self.passwd = db_cfg_obj.get('passwd')
        self.dbname = db_cfg_obj.get('db')

        self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.dbname)
        self.cursor = self.db.cursor()

        pre_sql = "SET NAMES 'utf8'"
        self.exec_sql(pre_sql)

    def set_table(self, table):
        self.table = table

    def exec_sql(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def save(self, data):
        sql = "INSERT INTO " + self.table + " ("
        i = 0
        for k in data:
            sql += k
            i += 1
            if not i == len(data):
                sql += ','
        sql += ") "

        sql += "VALUES ("

        i = 0
        for k in data:
            val = str(data[k])
            if isinstance(val, str):
                val = str(data[k])
                sql += '"' + val + '"'
            else:
                sql += str(val)
            i += 1
            if not i == len(data):
                sql += ','
        sql += ") "

        print sql

        res = self.cursor.execute(sql)
        self.db.commit()

        return res

    def count(self):
        return self.cursor.rowcount

    def close(self):
        self.db.close()

    @staticmethod
    def get_def_conn(db="qa_share_base"):
        conf_o = cofConf.MyCfg("cfg.ini")
        conf_o.set_section("mysql")
        host = conf_o.get("host")
        port = conf_o.get("port")
        user = conf_o.get("user")
        password = conf_o.get("pass")
        mysql_o = MysqlConn(host, port, user, password)
        conn = mysql_o.get_connection(db)
        return conn


if __name__ == "__main__":
    print "start..."
    import cof.conf as CoConfM
    conf_o = CoConfM.MyCfg("cfg.ini")
    conf_o.set_section("mysql")
    host = conf_o.get("host")
    port = conf_o.get("port")
    user = conf_o.get("user")
    password = conf_o.get("pass")
    mysql_o = MysqlConn(host, port, user, password)
    conn = mysql_o.get_connection("qa_share_log")
    conn.set_table("db_info")
    data = dict()
    import cof.rand as CoRandM
    rand_o = CoRandM.CoRand()
    uuid_str = rand_o.uuid()
    data["db_info_id"] = uuid_str
    # data["info"] = "hello,world"
    conn.save(data)
    sql = """
    INSERT INTO db_info (db_info_id) VALUES ("4b416bb6626d488")
    """
    cursor = conn.db.cursor()
    # cursor.execute(sql)
    # conn.db.commit()
    # rec = conn.exec_sql(sql)
    rec = conn.exec_sql("SELECT * FROM db_info")
    print rec
    conn.close()
