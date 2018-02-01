# coding=utf-8

"""
提取函数调用等运行时信息
"""

__author__ = 'Administrator'

import sys
import inspect
import traceback

import os
import re


cfgType = "dev"


class ExecHandler(object):
    """
    处理异常信息
    """


class Proc(object):
    def __init__(self):
        info = sys.exc_info()
        traceback.format_exc()
        pass

    def log_w(msg):
        f = inspect.currentframe()
        lineno = f.f_back.f_lineno

        if cfgType == "dev" or True:
            msg = "函数：" + str(f.f_back.f_code.co_name) + "行号：" + str(lineno) + "\t消息：" + str(msg)

    def get_call_info(self, msg):
        msg = sys._getframe().f_code.co_name + ': ' + msg
        return msg


def get_proc_id(name):
    cmd = 'ps aux | grep \'%s\'' % name

    f = os.popen(cmd)

    info = f.read()

    #print "进程查询信息：" + cmd
    #print info
    procList = info.split("\n")
    #print procList
    for proc in procList:
        #print proc
        patn = re.compile(r'\s+')
        procInfo = patn.split(proc)
        #print len(procInfo)
        if len(procInfo) >= 10:
            #print "进程信息"
            cmdRun = procInfo[10]
            patn1 = re.compile(r'^grep')
            patn2 = re.compile(r'^sh')
            if not patn1.match(cmdRun) and not patn2.match(cmdRun):
                return procInfo[1]

    print "进程不存在"
    return 0


    m = re.search('\w+\s+(\d+).*', info)
    print m

    if m is not None:
        match = m.group()
        #print "匹配成功"
        #print match
        #print "分组"
        print m.groups(0)
        if match.find("ps aux") > 0:
            #print "进程不存在"
            #print match.find("ps aux")
            return 0
        else:
            return m.groups(0)[0]

if __name__ == "__main__":
    proc = Proc()
    print proc.get_call_info("hello, world")
    print get_proc_id('log_server')
    try:
        raise Exception("hello, exeception")
    except Exception, err_msg:
        print Exception
        print err_msg
        print str(err_msg)


