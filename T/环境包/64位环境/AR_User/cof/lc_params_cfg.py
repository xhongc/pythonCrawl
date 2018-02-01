# coding=utf-8
__author__ = 'hq'

import cof.file as cofFile
import ConfigParser
import os

class LcParamsCfg(object):
    def __init__(self, path='params.ini'):
        app_loc = cofFile.get_app_loc()
        path = app_loc + 'config' + os.sep + 'lc_params_cfg' + os.sep + path
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
        self.set(section, option, value)

    def get_section(self, sec_name):
        return self.cfg_obj.items(sec_name)

if __name__ == "__main__":
    o = LcParamsCfg()
    o.set_section('dist_path_instance')
    print o.get('nd_instance')