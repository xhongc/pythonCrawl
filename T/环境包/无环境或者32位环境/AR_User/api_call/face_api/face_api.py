# coding=utf-8
'''
@author: 'wang'
'''
import cof.http as cofHttp
import cof.restful as CoRestful

'''
服务端人脸识别接口，文档地址：
http://wiki.bigdata.99.com/bin/view/人脸验证与识别/开发指南
api_key=5669A6E68E2611E69BBD549F351429C8
api_secret=5669A7278E2611E69BBD549F351429C8
url=http://test.smart.99.com:8083/v2/proxy/faceProxy
'''


class FaceApi(object):

    def __init__(self):
        self.host = "test.smart.99.com"
        self.port = 8083
        self.http_obj = cofHttp.HttpCurl(self.host, self.port)
        self.rest_o = CoRestful.Restful()
        self.api_key = "5669A6E68E2611E69BBD549F351429C8"
        self.api_secret = "5669A7278E2611E69BBD549F351429C8"
        
        self.header = [
            "Accept: application/json"
        ]
        self.http_obj.set_header(self.header) 

    def person_create(self, person_name, img_url):
        url = "/v2/proxy/faceProxy/person_create"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('person_name', person_name),
            ('img_url', img_url)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "添加用户失败")
        return data
    
    def person_delete(self, person_name):
        url = "/v2/proxy/faceProxy/person_delete"
        fields = [
            ('api_key' , self.api_key),
            ('api_secret', self.api_secret),
            ('person_name', person_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "删除用户失败")
        return data
    
    def person_exist(self, person_name):
        url = "/v2/proxy/faceProxy/person_exist"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('person_name', person_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "判断用户是否存在失败")
        return data
    
    def group_create(self, group_name):
        url = "/v2/proxy/faceProxy/group_create"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "添加分组失败")
        return data
    
    def group_delete(self, group_name):
        url = "/v2/proxy/faceProxy/group_delete"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "删除分组失败")
        return data

    def group_get_info(self, group_name):
        url = "/v2/proxy/faceProxy/group_get_info"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "获取分组信息失败")
        return data

    def group_get_list(self):
        url = "/v2/proxy/faceProxy/group_get_list"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "获取分组列表失败")
        return data
    
    def group_exist(self, group_name):
        url = "/v2/proxy/faceProxy/group_exist"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "判断分组是否存在失败")
        return data
    
    def group_add_person(self, group_name, person_name):
        url = "/v2/proxy/faceProxy/group_add_person"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name),
            ('person_name', person_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "添加用户到分组失败")
        return data
    
    def group_remove_person(self, group_name, person_name):
        url = "/v2/proxy/faceProxy/group_remove_person"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name),
            ('person_name', person_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "从分组移除用户失败")
        return data
    
    def train_identify(self, group_name):
        url = "/v2/proxy/faceProxy/train_identify"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name)
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        # print response
        data = self.rest_o.parse_response(response, 200, "训练模型失败")
        return data
    
    def recognition_identify(self, group_name, img_url):
        url = "/v2/proxy/faceProxy/recognition_identify"
        fields = [
            ('api_key', self.api_key),
            ('api_secret', self.api_secret),
            ('group_name', group_name),
            ('img_url', img_url),
            ('n_top', "1")
        ]
        response = self.http_obj.post(url, fields, isjson=False)
        print response
        data = self.rest_o.parse_response(response, 200, "人脸识别失败")
        return data

if __name__ == "__main__":
    face = FaceApi()
    print face.group_exist("QA-Test-Group")
    print face.group_get_info("QA-Test-Group")
    # print face.train_identify("QA-Test-Group")