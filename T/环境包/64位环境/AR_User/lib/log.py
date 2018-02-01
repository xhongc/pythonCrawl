# coding=utf-8

__author__ = 'Administrator'

import logging
from AR_User.cof.logger.hyqa_logger import ScribeHandler

import AR_User.cof.conf as CoConfM


class Logger(object):
    def __init__(self):
        cfg_o = CoConfM.MyCfg('cfg.ini')
        cfg_o.set_section('log')
        log_type = cfg_o.get('type')

        logger = logging.getLogger('test01')

        if log_type == 'file':
            pass
        else:
            # 初始化一个日志处理器
            # 连接到日志服务器
            self.scribe_handler = ScribeHandler()
            self.scribe_handler.set_appid(10015)
            self.scribe_handler.set_filepath('/LogTest/Test01/error.log')
            logger.addHandler(self.scribe_handler)

        logger.setLevel(logging.DEBUG)

        self.logger = logger

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def debug_path(self, path):
        self.scribe_handler.set_filepath(path)
        self.logger.info("debug: 伪接口")

    def get_logger(self):
        return self.logger


if __name__ == "__main__":
    log = Logger()
    log.debug("/LogTest/Test02/error.log")
    log.debug("/LogTest/Test03/error.log")