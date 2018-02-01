# coding=utf-8

"""
python日志记录设施

"""
__author__ = 'linzh'

import logging


class LogInfo(object):
    """
    日志记录类
    """
    def __init__(self, logfile="error.log", logtag="test", format_str="[%(asctime)s] %(message)s"):
        # print logfile
        try:
            self.logger = None
            self.logger = logging.getLogger(logtag)
            # 设置日志的记录设施
            self.hdlr = logging.FileHandler(logfile)
            self.logger.addHandler(self.hdlr)
            # format_str = "[%(asctime)s]: %(filename)s %(levelname)s %(message)s"
            # 完整路径
            # format_str = "[%(asctime)s]: %(pathname)s %(levelname)s %(message)s"
            # format_str = "[%(asctime)s]: %(funcName)s %(levelname)s %(message)s"
            formatter = logging.Formatter(format_str, "%Y-%m-%d %H:%M:%S")
            self.hdlr.setFormatter(formatter)
            # 设置日志级别
            self.logger.setLevel(logging.DEBUG)
        except Exception, exc:
            print Exception, exc
            print "log init error!"

    def output(self, loginfo, errorflag=0):
        """
        """
        try:
            if errorflag:
                self.logger.error("error: " + loginfo)
            else:
                self.logger.error(loginfo)
        except Exception, exc:
            print Exception, exc
            print "log output error!"

    def write(self, loginfo):
        """
        打印日志信息

        :参数:

        - `loginfo`: 要被写入的日志信息

        .. seealso:: :meth:`output`
        """

        self.output(loginfo)

    def close(self):
        try:
            self.hdlr.close()
            self.logger.removeHandler(self.hdlr)
        except Exception, exc:
            print Exception, exc
            print "log close error!"


if __name__ == "__main__":
    print "日志测试程序"
    logger = LogInfo()
    logger.write("hello, world")
    logger.close()
    # 关闭后会报错
    # No handlers could be found for logger "test"
    # logger.write("hello, linzh")
