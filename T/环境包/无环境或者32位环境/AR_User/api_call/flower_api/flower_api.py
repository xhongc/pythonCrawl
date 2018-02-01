# coding=utf-8
'''
@author: 'wang'
'''
import cof.http as cofHttp
import cof.restful as CoRestful

'''
花朵识别，服务端接口：
http://cfsrv.cloud.99.com:8080/fr?client=weixin&token=786232bc0b910b2d1e9d54b836976ded&url=http://img1.3lian.com/img2011/11/132/d/01.jpg&top=5
'''
class FlowerApi(object):
    
    def __init__(self):
        self.host = "cfsrv.cloud.99.com"
        self.port = 8080
        self.http_obj = cofHttp.HttpCurl(self.host, self.port)
        self.rest_o = CoRestful.Restful()
        
        self.header = [
            "Accept: application/json",
            "Content-Type: application/json"
        ]
        self.http_obj.set_header(self.header) 
        

    def get_flower(self, flower_url):
        url = "/fr"
        json_body={
            "client": "weixin",
            "token": "786232bc0b910b2d1e9d54b836976ded",
            "url": flower_url,
            "top":"1"
        }
        response =  self.http_obj.get(url, json_body)
        print response
        data =  self.rest_o.parse_response(response, 200, "识花失败")
        return data

if __name__ == "__main__":
    flower = FlowerApi()
    flower_url = "http://img1.3lian.com/img2011/11/132/d/01.jpg"
    data =  flower.get_flower(flower_url)
    print data