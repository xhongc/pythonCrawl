# coding=utf-8

"""
参数解析库

更加完善的命令行参数解析库
"""

__author__ = 'Administrator'


import types
import string
import sys


# 常量 标识参数声明符索引
NAME = 0
TYPE = 2
DEFAULT = 4
SPEC_LENGTH = 5

Bool = []

helpSpec = (
    ('help', 0, Bool, '显示帮助信息并退出'),
)


def parseArgs(title, argv, argSpecs, filesOK):
    """
    解析并检查命令行参数

    title   -- 程序文件名

    argv    --

    argSpecs -- 参数声明
    """

    global programName
    global _fileList

    errMsg = title + ' 命令行错误'
    programName = argv[0]

    print helpSpec

    # 命令行tuple
    argSpecs = helpSpec + argSpecs
    argSpecDic = {}

    print argSpecs

    for spec in argSpecs:
        arg = spec[NAME]
        argSpecDic[arg] = spec
        if len(spec) >= SPEC_LENGTH:
            set(arg, spec[DEFAULT])
        elif spec[TYPE] is Bool:
            set(arg, 0)
        else:
            set(arg, None)

    knownKeys = argSpecDic.keys()

    print knownKeys


    i = 1
    _fileList = []
    argc = len(argv)
    while i < argc:
        arg = argv[i]
        key = arg[1:]

        if key in knownKeys:
            spec = argSpecDic[key]
            if spec[TYPE] is Bool:
                set(key, 1)
            else:
                i = i + 1

            if i >= argc:
                return errMsg + 'missing argument to \'' + arg + '\' option'

            value = argv[i]

            if len(spec) >= SPEC_LENGTH:
                try:
                    if type(spec[DEFAULT]) == types.IntType:
                        typeStr = 'integer'
                        value = string.atoi(value)
                    elif type(spec[DEFAULT]) == types.FloatType:
                        typeStr = 'float'
                        value = string.atof(value)
                except:
                    sys.exc_traceback = None
                    return errMsg + '无法转换' + value + \
                        '为' + typeStr

                set(key, value)
            else:
                _fileList.append(arg)
                i = i + 1

    if get('help'):
        return _helpString(title, argSpecs)


def _helpString(title, argSpecs):
    pass


def exists(key):
    return configDict.has_key(key)


def get(key):
    return configDict[key]


def set(key, value):
    global configDict

    configDict[key] = value


configDict = {}


if __name__ == '__main__':
    program = 'args.py'
    commandLineArgSpecs = (
        ('fontscheme', 0, 'scheme', '字体使用，例如 pmw2'),
        ('fontsize',   0, 'num',    '字体的大小'),
        ('stdout',     0, Bool, '打印消息，而不是在label中显示')
    )

    parseArgs(program, sys.argv, commandLineArgSpecs, 0)
