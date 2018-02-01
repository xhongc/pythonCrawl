# coding=utf-8

"""
操作memcache缓存
"""
__author__ = 'Administrator'

import memcache


class CoMemcache(object):
    def __init__(self, host, port):
        link_info = host + ':' + port
        conn = memcache.Client([link_info], debug=0)
        self.conn = conn

    def set(self, k, v):
        self.conn.set(k, v)

    def get(self, k):
        return self.conn.get(k)


if __name__ == "__main__":
    import cof.conf as CoConfM
    conf_o = CoConfM.MyCfg('cfg.ini')
    conf_o.set_section('memcache')
    host = conf_o.get('host')
    port = conf_o.get('port')

    mc = CoMemcache(host, port)
    mc.set("hello", "world")
    print mc.get("hello")
