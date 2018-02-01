# coding=utf-8

"""
91u消息发送接口
"""
__author__ = 'Administrator'


import cof.http as cofHttp
import urllib


class MsgSender(object):
    def __init__(self, t, m):
        self.sender = ""
        self.to = t
        self.msg = m

    def set_sender(self, nr):
        self.sender = nr

    def set_to(self, nr):
        self.to = nr

    def set_msg(self, msg):
        self.msg = msg

    def send(self):
        data = dict()
        data['key'] = 'xxxx99u#$%'
        data['msg'] = self.msg
        data['to'] = self.to
        data = urllib.urlencode(data)
        print data
        http_obj = cofHttp.Http("192.168.205.8", 8889)
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        http_obj.set_header(header)
        return http_obj.post("/msg_send", data)
        #return http_obj.get("/")
        return http_obj.get("/msg_send")


if __name__ == "__main__":
    send_obj = MsgSender("871101", "hello")
    print send_obj.send()
