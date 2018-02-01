#coding=utf-8
__author__ = 'Administrator'

import os
import zipfile

import AR_User.cof.co_time as CoTimeM

APP_LOC = ''


def get_app_loc():
    local_dir = os.path.dirname(__file__)

    if not local_dir:
        local_dir = "."

    return local_dir + os.sep + '..' + os.sep


def expand_links(path):
    """
    将路径扩展为绝对路径

    主程序在不同目录下进行测试
    """
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    return path


# 压缩目录
def zip_dir(dirname, zipfilename):
    """
    对指定目录进行压缩，并保存到dirname
    """
    filelist = []

    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    # 创建压缩对象
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)

    for tar in filelist:
        arcname = tar[len(dirname):]
        # 添加压缩文件到压缩对象
        zf.write(tar, arcname)

    zf.close()


class CoFile(object):
    """
    文件处理类
    """
    def __init__(self):
        self.prefix = ""
        self.path_str = ""
        self.path = ""
        self.filename = ""
        self.cur_path = ""

    def set_prefix(self, pre):
        self.prefix = pre

    def set_path(self, path, suffix='.log'):
        is_dir = os.path.isdir(path)
        print is_dir
        # 获取文件后缀信息
        ext_info = os.path.splitext(path)
        # print ext_info[0][-4]
        if ext_info[1] or ext_info[0][-4] == '.':
            # 如果有后缀，是文件
            print "文件"
            path_info = os.path.split(path)
            self.path_str = path_info[0]
            self.filename = path_info[1]

            if not ext_info[1]:
                self.filename = CoTimeM.get_cur_date() + suffix
        else:
            self.path_str = path
            self.filename = CoTimeM.get_cur_date() + suffix

        self.filename = self.filename.replace(suffix, "")

    def parse_dir_str(self):
        self.path = self.path_str.split("/")
        return self.path

    def get_fname(self):
        return self.filename

    def create_dir(self, path_list):
        self.cur_path = self.prefix
        for dir_seg in path_list:
            if dir_seg:
                self.cur_path = self.cur_path + os.path.sep + dir_seg
                if not os.path.exists(self.cur_path):
                    os.mkdir(self.cur_path)

    def get_full_path(self):
        return self.prefix + self.path_str

if __name__ == "__main__":
    cf = CoFile()
    cf.set_prefix("E:/temp")
    cf.set_path("/hello/world/.log")
    path_list = cf.parse_dir_str()
    print "文件名"
    print cf.get_fname()
    cf.create_dir(path_list)
    print cf.get_full_path()
    print cf.get_fname()

