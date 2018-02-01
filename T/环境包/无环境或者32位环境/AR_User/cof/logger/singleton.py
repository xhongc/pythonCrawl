# coding=utf-8

__author__ = 'Administrator'


class Borg(object):
    """
    单实例化
    """
    _state = {}

    def __new__(cls, *args, **kw):
        """
        实例化时调用
        """

        # 调用父类的构造函数
        ob = super(Borg, cls).__new__(cls, *args, **kw)
        ob.__dict__ = cls._state
        return ob


