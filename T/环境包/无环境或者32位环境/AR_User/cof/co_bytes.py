# coding=utf-8
'''
@author: 'wang'
'''

import struct
import sys

def int2byte(num):
    if(sys.byteorder == "little"):
        return struct.pack('i', num)[::-1]
    return struct.pack('i', num)

def short2byte(num):
    if(sys.byteorder == "little"):
        return struct.pack('h', num)[::-1]
    return struct.pack('h', num)

def byte2int(data):
    if(sys.byteorder == "little"):
        len, = struct.unpack('i', data[::-1])
    else:
        len, = struct.unpack('i', data)
    return len

def byte2short(data):
    if(sys.byteorder == "little"):
        len, = struct.unpack('h', data[::-1])
    else:
        len, = struct.unpack('h', data)
    return len