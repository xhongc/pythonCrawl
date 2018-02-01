# coding=utf-8
__author__ = 'Administrator'

import json
import AR_User.cof.http as cofHttp
import AR_User.cof.restful as CoRestful


class Send99U(object):
    """
    99u推送消息接口封装
    """
    def __init__(self):
        """
        初始化
        """
        self.host = "10.1.191.176"     # mxsnd.99.com
        self.port = 1220
        self.http_obj = cofHttp.Http(self.host, self.port)

    def send_to_receivers(self, content, receiver_list):
        """
        发送内容到各知照人的99u
        content：内容
        list：需要通知的人的名单，list类型
        """
        json_data = {
            "sender": {
                    "appid": 104,
                    "permcode": "",
                    "unitid": 42012,
                    "uid": 91000
            },
            "receiver": receiver_list,
            "msg": {
                "type": "A2A",
                "body": content,
                "level": 40
            }
        }
        param = json.dumps(json_data)
        self.http_obj.post("/send", param)

    def send_to_groups(self, content, group_list):
        """
        发送内容到99u群
        content：内容
        group_id：群id列表，list类型，但是仅会发给第一个群
        """
        for group_id in group_list:
            group_id_list = list()
            group_id_list.append(group_id)
            json_data = {
                "sender": {                 # 发送者
                    "appid": 105,               # 必填，发送应用（5位整型）
                    "unitid": 42012,            # 必填，单位编号（8位整型）
                    "uid": 91000                # 必填，组织用户ID（11位整型）
                },
                "groups": group_id_list,    # 必填，消息群编号，目前仅支持单个群（11位整型）,
                "msg": {                    # 消息内容
                    "body": content             # 必填，发送的消息内容（1024位字符）
                }
            }
            param = json.dumps(json_data)
            self.http_obj.post("/groupmsg", param)


class SendNew99U(object):
    """
    新99u推送消息接口封装
    QA机器人：
    uri:281474976720219
    password:4abb8356-d8bd-44eb-b8cc-ee6c2a281ad8
    """
    def __init__(self):
        """
        初始化
        """
        self.host = "im-agent.web.sdp.101.com"
        # self.port = None
        self.http_obj = cofHttp.Http(self.host)
        self.header = {
            "Content-Type": "application/json"
        }
        self.rest_o = CoRestful.Restful()

    def get_agent_mac_token(self):
        """
        获取推送号（只能是公众号）的授权信息
        body参数：
        uri: uid
        password: 密码
        返回值：
        {
            "mac_algorithm": "hmac-sha-256",
            "nonce": "1438677808798:2OLebj6B",
            "mac": "aIlsdFuRcV0jji+u+uwAw3hsNFSS2YJ95LnjYS0h9OY=",
            "access_token": "agent_281474976720145"
        }
        """
        # 1.发送请求
        url = "/v0.2/api/agents/users/tokens"
        body = {
            "uri": "281474976720219",
            "password": "4abb8356-d8bd-44eb-b8cc-ee6c2a281ad8"
        }
        param = json.dumps(body)
        self.http_obj.set_header(self.header)
        res = self.http_obj.post(url, param)
        code = 200
        msg = "获取代理用户授权失败"
        data = self.rest_o.parse_response(res, code, msg)

        # 2.拼装数据
        access_token = data['access_token']
        nonce = data['nonce']
        mac = data['mac']
        authorization = 'MAC id="%s",nonce="%s",mac="%s"' % (access_token, nonce, mac)
        print "authorization: ", authorization
        return authorization

    def send_to_receivers(self, info, receiver_list):
        """
        发送内容到各知照人的99u
        content：内容
        list：需要通知的人的名单，list类型
        """
        # 1.获取代理授权信息
        authorization = self.get_agent_mac_token()
        self.header["Authorization"] = authorization

        # 2.发送消息
        url = "/v0.2/api/agents/messages"
        content = "Content-Type:text/plain\r\n\r\n%s" % info
        body = {
            "filter": [
                {
                    "name": "uri",
                    "args": {
                        "uri_list": receiver_list
                    }
                }
            ],
            "body": {
                "content": content,
                "flag": 0
            }
        }
        param = json.dumps(body)
        self.http_obj.set_header(self.header)

        code = 200
        msg = "send message to anyone failed!"
        res = self.http_obj.post(url, param)
        self.rest_o.parse_response(res, code, msg)

    def send_to_groups(self, info, group_list):
        """
        发送内容到99u群
        content：内容
        group_id：群id列表，list类型
        """
        # 1.获取代理授权信息
        authorization = self.get_agent_mac_token()
        self.header["Authorization"] = authorization

        # 2.发送消息
        url = "/v0.2/api/agents/messages"
        content = "Content-Type:text/plain\r\n\r\n%s" % info
        body = {
            "filter": [
                {
                    "name": "gid",
                    "args": {
                        "gid": group_list
                    }
                }
            ],
            "body": {
                "content": content,
                "flag": 0
            }
        }
        param = json.dumps(body)
        self.http_obj.set_header(self.header)

        code = 200
        msg = "发送消息给群组失败"
        res = self.http_obj.post(url, param)
        self.rest_o.parse_response(res, code, msg)

if __name__ == "__main__":
    # 旧99u方式：
    # content = "lsx testing~!!"
    # group_list = [526397]
    # send_o = Send99U()
    # send_o.send_to_receivers(content, group_list)

    # 新99u方式：
    # 推送给个人
    content = "奇琪、好棒棒哦~"
    group_list = [31328051]
    send_o = SendNew99U()
    # send_o.send_to_receivers(content, group_list)
    # 推送给群
    # content = "能收到吗？"
    # group_list = [2180138, 2146295]
    # send_o = SendNew99U()
    send_o.send_to_groups(content, group_list)

