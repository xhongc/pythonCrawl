# coding=utf-8
'''
@author: 'wang'
'''
from cof.co_bytes import *
import time


class StringPacket(object):
    
    def __init__(self, context):
        self.context = context
        self.context_data = self.context.encode('utf-8')
        self.len = len(self.context_data)
        self.data = self._get_bytes()

    def _get_bytes(self):
        len_data = short2byte(self.len)
        return len_data + self.context_data


class SocketPacket(object):
    
    def __init__(self, tag, api, param):
        self.tag = tag
        self.api = StringPacket(api)
        self.param = StringPacket(param)
        self.context_data = int2byte(self.tag) + self.api.data + self.param.data
        self.len = len(self.context_data) + 4
        self.data = self._packet_data()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ':send => ' + api+"(" + str(tag) + ")" + ": " + self.param.context
        # print 'packet data:' + self.data.encode('hex')
    
    def _packet_data(self):
        len_data = int2byte(self.len)
        return len_data + self.context_data


class StringUnPacket(object):
    
    def __init__(self, data):
        self.data = data
        self.context = self._get_context();
    
    def _get_context(self):
        self.len = byte2short(self.data[0:2])
        return self.data[2: 2 + self.len].decode('utf-8')


class SocketUnPacket(object):
    
    def __init__(self, data):
        self.data = data

        # print 'unpacket data:' + self.data.encode('hex')
        self.tag, self.api, self.param = self._unpacket_data()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ':receive => ' + self.api.context + "(" + str(self.tag) + ")" + ": " + self.param.context
    
    def _unpacket_data(self):
        self.len = byte2int(self.data[0:4])
        tag_start_index = 4
        tag_end_index = 4 + 4
        tag = byte2int(self.data[tag_start_index: tag_end_index])
        
        api_len_start_index = tag_end_index
        api_len_end_index = tag_end_index + 2
        api_len = byte2short(self.data[api_len_start_index: api_len_end_index])
#         print api_len
        
        api_data_start_index = api_len_end_index
        api_data_end_index = api_data_start_index + api_len
        api_data = self.data[api_len_start_index: api_data_end_index]
        api = StringUnPacket(api_data)
#         print api.context
#         print api_data.encode('hex')
        
        param_len_start_index = api_data_end_index
        param_len_end_index = param_len_start_index + 2
        param_len = byte2short(self.data[param_len_start_index: param_len_end_index])
#         print param_len
        
        param_data_start_index = param_len_end_index
        param_data_end_index = param_data_start_index + param_len
        param_data = self.data[param_len_start_index: param_data_end_index]
        param = StringUnPacket(param_data)
#         print param.context
#         print param_data.encode('hex')
        
        return tag, api, param

