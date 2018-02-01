# coding=utf-8

__author__ = 'Administrator'

import socket

from singleton import Borg


class ScribeLogger(Borg):
    """
    scribe日志记录器
    """

    APPID = "9997"

    def __init__(self):
        """
        初始化套接字
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(('192.168.205.8', 11215))
            self.sock = sock
        except Exception, e:
            print Exception, e
            exit(1)

    def write(self, msg):
        """
        写日志消息到服务器
        """
        self.sock.send(ScribeLogger.APPID + ":" + msg)
        pass

    def writeln(self, msg):
        self.sock.send(ScribeLogger.APPID + ":" + msg + "\n")
        pass

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    logger = ScribeLogger()
    logger.write("hello, world")

