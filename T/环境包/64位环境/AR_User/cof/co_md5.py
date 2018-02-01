# coding=utf-8

__author__ = 'linzh'

import hashlib


def get_md5(str):
    return hashlib.md5(str).hexdigest()


if __name__ == "__main__":
    print "start..."
    pwd = "123456"
    print get_md5("123456")
    md5_pwd1 = get_md5("F9X6L8PWD" + pwd + "dev")
    print md5_pwd1
    print get_md5(md5_pwd1)
