# coding=utf-8

"""
时间操作
"""
__author__ = 'linzh'

import sys

old_sys_path = sys.path
sys.path = sys.path[1:] + sys.path[:1]

import datetime
import time as sys_time

# 获取当前时间戳
now = sys_time.time()
sys.path = old_sys_path


def gen_time_str(t_info):
    """从时间信息生成要访问的日志文件名"""
    year = str(t_info.tm_year)
    if t_info.tm_mon < 10:
        month = '0'+str(t_info.tm_mon)
    else:
        month = str(t_info.tm_mon)
    if t_info.tm_mday < 10:
        day = '0'+str(t_info.tm_mday)
    else:
        day = str(t_info.tm_mday)
    return year+month+day


def get_date_ymd():
    now = sys_time.time()
    ltime = sys_time.localtime(now)
    return gen_time_str(ltime)


def info():
    print "time"
    sys_time.localtime()


def get_ts():
    """
    系统时间戳，整型
    """
    return int(sys_time.time())


def get_log_time():
    """
    返回下划线分割的格式
    """
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')


def get_cur_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')


class CoTime(object):
    def __init__(self, init_day):
        self.ts = 0
        if isinstance(init_day, float) or isinstance(init_day, int):
            # print "浮点型"
            self.ts = int(init_day)
            self.t_info = sys_time.localtime(self.ts)
        elif isinstance(init_day, str):
            # print "字符串"
            # 字符串 -> 时间结构
            self.t_info = sys_time.strptime(init_day, "%Y-%m-%d %H:%M:%S")
            self.ts_f = sys_time.mktime(self.t_info)
            self.ts = int(self.ts_f)

    def get_ts(self):
        return self.ts

    def get_year(self):
        pass

    def get_weekday(self):
        """
        返回周几
        周一返回1
        """
        return self.t_info.tm_wday + 1

    def get_t_info(self):
        """

        """
        return self.t_info

    def get_format_str(self, f):
        return sys_time.strftime(f, self.t_info)


if __name__ == '__main__':
    info()
    print "datetime获取当前时间"
    print datetime.datetime.now()
    threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=3))
    print "三天前：", threeDayAgo
    # datetime -> struct
    # mktime(str) -> struct
    # strftime
    print threeDayAgo.timetuple()
    timeStamp = int(sys_time.mktime(threeDayAgo.timetuple()))
    otherStyleTime = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
    print timeStamp
    print otherStyleTime
    print get_log_time()

    import time
    print "Y-m-d"
    print time.strftime("%Y-%m-%d")
    d = "2014-01-01 0:0:0"
    # time format
    tf = "%Y-%m-%d %H:%M:%S"
    # strptime(str, format) -> struct
    # struct -> int/float
    # int/float -> str
    # mktime
    # format, struct -> str
    # time.strftime()
    t = time.mktime(time.strptime(d, "%Y-%m-%d %H:%M:%S"))
    print time.strptime(d, tf)
    print "时间戳", t

    # 测试CoTime类
    cot1 = CoTime(time.time())
    print "获取cot1时间戳", cot1.get_ts()
    print cot1.get_weekday()
    cot2 = CoTime(d)
    print "获取cot2时间戳", cot2.get_ts()
    print cot2.get_weekday()
