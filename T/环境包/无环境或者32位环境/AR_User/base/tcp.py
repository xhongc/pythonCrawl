# coding=utf-8
"""
@author: 'wang'
"""

from cof.conf import MyCfg


class BaseTcp(object):
    def __init__(self, section_name = 'ar_api'):
        my_cfg = MyCfg('cfg.ini')
        my_cfg.set_section(section_name)

        self.host = my_cfg.get('host')
        self.port = my_cfg.get('port')

    def get_host(self):
        return self.host

    def get_port(self):
        return int(self.port)


if __name__ == "__main__":
    base_http = BaseTcp()
    print base_http.get_host()
    print base_http.get_port()
