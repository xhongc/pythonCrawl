# coding=utf-8

"""
远程过程调用
"""

__author__ = 'Administrator'

import os
import urllib2


def post_zip(file_path,project):
    #url = 'http://auto.test.91.com/ui_test.php?prj='+project+'&zip=1'
    url = 'http://auto.test.91.com/api.php?team=dianda&prj=' + project + '&kind=ui&zip=1'
    length = os.path.getsize(file_path)
    png_data = open(file_path, "rb")
    request = urllib2.Request(url, data=png_data)
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Content-Length', '%d' % length)
    res = urllib2.urlopen(request).read().strip()
    return res

