# coding=utf-8
__author__ = 'Administrator'

import AR_User.cof.file as cofFile

import ConfigParser

import os

# 全局变量
gblCfp = ConfigParser.ConfigParser()


class MyCfg(object):
    """
    配置信息对象

    .. doctest::

        >>> conf_o = MyCfg('cfg.ini')
        >>> conf_o.set_section('section')
        >>> conf_o.get('key')
    """
    def __init__(self, path):
        app_loc = cofFile.get_app_loc()
        cfg_type = get_cfg_type()
        path = app_loc + 'config' + os.sep + cfg_type + os.sep + path
        ex_path = cofFile.expand_links(path)
        if not os.path.exists(ex_path):
            print "config file is not exist (" + ex_path + ")"
            exit()
        self.path = ex_path
        self.sec = ""
        self.cfg_obj = ConfigParser.ConfigParser()
        self.cfg_obj.read(self.path)

    def set_section(self, section):
        self.sec = section

    def get(self, key):
        return self.cfg_obj.get(self.sec, key)

    # 为section的字段赋值
    def set(self, section, option, value):
        self.cfg_obj.set(section, option, value)
        self.cfg_obj.write(open(self.path, "w"))

    def get_section(self, sec_name):
        return self.cfg_obj.items(sec_name)


# 获取配置类型
def get_cfg_type_path():
    filepath = cofFile.get_app_loc() + 'cfgtype.ini'
    return filepath


# 获取配置目录
def get_cfg_type():
    filepath = get_cfg_type_path()
    gblCfp.read(filepath)
    cfgtype = gblCfp.get('cfg', "type")
    return cfgtype


def read_db_cfg(cfgfile, db):
    """读取数据配置数据"""
    cf = ConfigParser.ConfigParser()
    cf.read(cfgfile)
    dbcfg = dict()
    dbcfg['host'] = cf.get(db, "hostname")
    dbcfg['user'] = cf.get(db, "username")
    dbcfg['pass'] = cf.get(db, "password")
    dbcfg['db'] = cf.get(db, "database")
    return dbcfg

if __name__ == "__main__":
    o = MyCfg('cfg.ini')
    o.set_section('report')
    print o.get('path')