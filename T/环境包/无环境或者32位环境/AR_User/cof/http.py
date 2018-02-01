# coding=utf-8
__author__ = 'Administrator'
# modify = weichunwang 2016-01-12

import time
import datetime
import pycurl
import StringIO
import AR_User.lib.log as LLog

logger = LLog.Logger()


def get_current_time():
    """
    获取当前时间
    """
    current_time = int(time.time()) * 1000 + datetime.datetime.now().microsecond/1000
    return current_time


class Http(object):
    """对GET/POST进行了封装，让代码更简短易读
    :class:`cof.http.Http` 先初始化

    * `METHOD`: 默认请求方法
    httplib的一层封装，更易于使
    >>> http_obj = cofHttp.Http(url, 80)
    >>> http_obj.set_header(header)
    >>> http_obj.post("/syslog", self.data)
    """

    METHOD = "GET"

    def __init__(self, host, port=80, url='', ssl=False):
        """
        使用httplib库进行操作
        """
        import httplib
        self.host = host
        self.port = str(port)
        if self.port == "":
            self.port = None
        self.url = url
        self.header = dict()
        # 请求body
        self.params = None
        if ssl:
            self.conn = httplib.HTTPSConnection(self.host, self.port)
        else:
            # self.conn = httplib.HTTPConnection("127.0.0.1", 8888)
            self.conn = httplib.HTTPConnection(self.host, self.port)

        # self.conn.set_tunnel(self.host, int(self.port))

    def parse_url(self):
        pass

    def set_header(self, header):
        """
        设置http请求头，可以设置AccessToken
        """
        self.header = header

    def get(self, url, params = None):
        if params:
            url = url + '?'
            for p in params:
                url += '&' + p + '=' + params[p]
        conn = self.conn
        begin_time = get_current_time()
        conn.request(method="GET", url=url, headers=self.header)
        end_time = get_current_time()
        response = conn.getresponse()
        res = dict()
        if self.port is None:
            res["request"] = "GET " + self.host + url
        else:
            res["request"] = "GET " + self.host + ":" + self.port + url
        res["code"] = response.status                   # 状态码
        res["data"] = response.read()                   # 响应的返回值
        res["response_header"] = response.msg.dict      # 响应的头信息
        res["response_time"] = end_time - begin_time    # http响应的间隔时间，单位ms
        #print "get method's response time is " + str( res["response_time"] ) +"ms"
        logger.info(url)
        logger.info("===============================")
        logger.info(res["data"])
        conn.close()
        return res

    def post(self, url, params):
        conn = self.conn
        begin_time = get_current_time()
        conn.request(method="POST", url=url, headers=self.header, body=params)
        end_time = get_current_time()
        response = conn.getresponse()
        res = dict()
        if self.port is None:
            res["request"] = "POST " + self.host + url + ",\nbody=" + params
        else:
            res["request"] = "POST " + self.host + ":" + self.port + url + ",\nbody=" + params
        res["code"] = response.status
        res["data"] = response.read()
        res["response_header"] = response.msg.dict
        res["response_time"] = end_time - begin_time
        logger.info(url)
        logger.info(params)
        logger.info("===============================")
        logger.info(res["data"])
        conn.close()
        return res

    def delete(self, url, params=None):
        conn = self.conn
        begin_time = get_current_time()
        conn.request(method="DELETE", url=url, headers=self.header, body=params)
        end_time = get_current_time()
        response = conn.getresponse()
        res = dict()
        if self.port is None:
            res["request"] = "DELETE " + self.host + url
        else:
            res["request"] = "DELETE " + self.host + ":" + self.port + url
        res["code"] = response.status
        res["data"] = response.read()
        res["response_header"] = response.msg.dict
        res["response_time"] = end_time - begin_time
        res["request_header"] = self.header
        conn.close()
        return res

    def patch(self, url, params):
        conn = self.conn
        begin_time = get_current_time()
        conn.request(method="PATCH", url=url, headers=self.header, body=params)
        end_time = get_current_time()
        response = conn.getresponse()
        res = dict()
        if self.port is None:
            res["request"] = "PATCH " + self.host + url + ",\nbody=" + params
        else:
            res["request"] = "PATCH " + self.host + ":" + self.port + url + ",\nbody=" + params
        res["code"] = response.status
        res["data"] = response.read()
        res["response_header"] = response.msg.dict
        res["response_time"] = end_time - begin_time
        conn.close()
        return res

    def put(self, url, params):
        conn = self.conn
        begin_time = get_current_time()
        conn.request(method="PUT", url=url, headers=self.header, body=params)
        end_time = get_current_time()
        response = conn.getresponse()
        res = dict()
        if self.port is None:
            res["request"] = "PUT " + self.host + url + ",\nbody=" + params
        else:
            res["request"] = "PUT " + self.host + ":" + self.port + url + ",\nbody=" + params
        res["code"] = response.status
        res["data"] = response.read()
        res["response_header"] = response.msg.dict
        res["response_time"] = end_time - begin_time
        conn.close()
        return res

class HttpCurl(object):
    """
    使用pycurl进行操作
    >>> http_obj = cofHttp.HttpCurl(host)
    >>> http_obj.set_header(header)
    >>> http_obj.post("/syslog", self.data)
    """
    def __init__(self, host, port=80, url='', ssl=False):
        """
        初始化host和port,如果url为https 则 实例化时ssl=True
        """
        self.ssl = ssl
        self.host = host
        self.port = str(port)
        self.header = list()

    def splice_url(self, url):
        """
        判断ssl确定正确的协议和端口号
        """
        if self.ssl:
            protocol = 'https'
            self.port = '443'
        else:
            protocol = 'http'

        return protocol +"://" + self.host + ":" + self.port + url

    def set_header(self, header):
        """
        设置http请求头，可以设置AccessToken
        """
        self.header = header

    def get(self, url, params = None):
        if params:
            url = url + '?'
            for p in params:
                url += '&' + p + '=' + params[p]
        url = self.splice_url(url)
        storage = StringIO.StringIO()
        print url
        c = pycurl.Curl()
        if self.ssl:
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(c.HTTPGET, 1)
        c.setopt(c.URL, url)
        c.setopt(pycurl.HTTPHEADER, self.header)
        c.setopt(c.WRITEFUNCTION, storage.write)
        begin_time = get_current_time()
        c.perform()
        end_time = get_current_time()
        response = storage.getvalue()
        res = dict()
        if self.port is None:
            res["request"] = "GET " + self.host + url
        else:
            res["request"] = "GET " + self.host + ":" + self.port + url
        res["code"] = c.getinfo(c.HTTP_CODE)                 # 状态码
        res["data"] = response                   # 响应的返回值
        res["response_time"] = end_time - begin_time    # http响应的间隔时间，单位ms
        logger.info(url)
        logger.info("===============================")
        logger.info(res["data"])
        c.close()
        return res

    def post(self, url, params = None , isjson = True):
        url = self.splice_url(url)
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        if self.ssl:
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(c.POST, 1)
        c.setopt(c.URL, url)
        if params:
            if isjson:
                c.setopt(c.POSTFIELDS, params)
            else:
                c.setopt(c.HTTPPOST, params)
        c.setopt(pycurl.HTTPHEADER, self.header)
        c.setopt(c.WRITEFUNCTION, storage.write)
        begin_time = get_current_time()
        c.perform()
        end_time = get_current_time()
        response = storage.getvalue()
        res = dict()
        if self.port is None:
            res["request"] = "POST " + self.host + url + ",\nbody=" + str(params)
        else:
            res["request"] = "POST " + self.host + ":" + self.port + url + ",\nbody=" + str(params)
        res["code"] = c.getinfo(c.HTTP_CODE)   
        res["data"] = response
        res["response_time"] = end_time - begin_time
        logger.info(url)
        logger.info(params)
        logger.info("===============================")
        logger.info(res["data"])      
        c.close()        
        return res

    def delete(self, url, params = None , isjson = True):
        url = self.splice_url(url)
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        if self.ssl:
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.CUSTOMREQUEST,"DELETE")
        c.setopt(c.URL, url)
        if params:
            if isjson:
                c.setopt(c.POSTFIELDS, params)
            else:
                c.setopt(c.HTTPPOST, params)        
        c.setopt(pycurl.HTTPHEADER, self.header)
        c.setopt(c.WRITEFUNCTION, storage.write)
        begin_time = get_current_time()
        c.perform()
        end_time = get_current_time()
        response = storage.getvalue()
        res = dict()
        if self.port is None:
            res["request"] = "DELETE " + self.host + url + ",\nbody=" + str(params)
        else:
            res["request"] = "DELETE " + self.host + ":" + self.port + url + ",\nbody=" + str(params)
        res["code"] = c.getinfo(c.HTTP_CODE)   
        res["data"] = response
        res["response_time"] = end_time - begin_time
        logger.info(url)
        logger.info(params)
        logger.info("===============================")
        logger.info(res["data"])      
        c.close()        
        return res

    def put(self, url, params = None, isjson = True):
        url = self.splice_url(url)
        storage = StringIO.StringIO()
        c = pycurl.Curl()
        if self.ssl:
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.CUSTOMREQUEST,"PUT")
        c.setopt(c.URL, url)
        if params:
            if isjson:
                c.setopt(c.POSTFIELDS, params)
            else:
                c.setopt(c.HTTPPOST, params)
        c.setopt(pycurl.HTTPHEADER, self.header)
        c.setopt(c.WRITEFUNCTION, storage.write)
        begin_time = get_current_time()
        c.perform()
        end_time = get_current_time()
        response = storage.getvalue()
        res = dict()
        if self.port is None:
            res["request"] = "PUT " + self.host + url + ",\nbody=" + str(params)
        else:
            res["request"] = "PUT " + self.host + ":" + self.port + url + ",\nbody=" + str(params)
        res["code"] = c.getinfo(c.HTTP_CODE)   
        res["data"] = response
        res["response_time"] = end_time - begin_time
        logger.info(url)
        logger.info(params)
        logger.info("===============================")
        logger.info(res["data"])      
        c.close()        
        return res

class HttpInfo(object):
    def __init__(self):
        self.host = ""

    def get_host(self):
        return self.host
