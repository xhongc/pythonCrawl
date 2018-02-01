# coding=utf-8
"""
@author: 'wang'
"""
import socket
import threading
import time
from cof.co_bytes import *


class MySocket(object):
    
    def __init__(self, host, port):
        self.socket_client = None
        self.host = host
        self.port = port
        self.lock = threading.Lock()
        self.int_len = 4

    def connect_server(self):
        try:
            if (self.socket_client != None):
                self.socket_client.close()
            self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket_client.settimeout(10)
            self.socket_client.connect((self.host, self.port))
        except socket.error, e:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + 'error creating socket:%s' %e

    def request(self, packet):
        try:
            if self.lock.acquire():
                print 'send data...'
                self.socket_client.send(packet.data)
                len_recv = self.socket_client.recv(self.int_len)
                data_size = byte2int(len_recv) - self.int_len
                data_recv = ''
                recv_size = 0
                while True:
                    buff = self.socket_client.recv(1024)
                    recv_size += len(buff)
                    data_recv += buff
                    if recv_size >= data_size:
                        break
                recv = len_recv + data_recv
                self.lock.release()
            return recv
        except socket.error, e:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + 'error send message:%s' %e

    def recive(self):
        try:
            if self.lock.acquire():
                print 'recv data...'
                len_recv = self.socket_client.recv(self.int_len)
                data_size = byte2int(len_recv) - self.int_len
                data_recv = ''
                recv_size = 0
                while True:
                    buff = self.socket_client.recv(1024)
                    recv_size += len(buff)
                    data_recv += buff
                    if recv_size >= data_size:
                        break
                recv = len_recv + data_recv
                self.lock.release()
            return recv
        except socket.error, e:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + 'error send message:%s' %e
    
    def close(self):
        try:
            if (self.socket_client != None):
                self.socket_client.close()
        except socket.error, e:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + 'error close socket:%s' %e
