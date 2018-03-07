# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest


class PosSpider(scrapy.Spider):
    name = 'pos'
    allowed_domains = ['mch.speedpos.cn']
    start_urls = ['http://www.baidu.com/']
    def start_requests(self):
        return [Request('https://mch.speedpos.cn/index/index',meta={'cookiejar':1},callback=self.login)]
    def login(self,response):
        data = {
            'login_name': '2100800007966',
            'login_pwd': 'd976a22c'
        }
        return [FormRequest('https://mch.speedpos.cn/index/index',
                            method='POST',
                            formdata=data,
                            callback=self.after_login)]
    def after_login(self,response):
        search_data = {
            '_loadpage': '1',
            'page': page,
            'start_time': '2018-03-01 00:00:00',
            'end_time': '2018-03-01 23:59:59',
            'time_by': 'pay_time',
            'trade_type': '',
            'order_status': '1',
        }
        return [FormRequest(self.start_urls,
                            method= 'POST',
                            meta={'cookiejar':response.meta['cookiejar']},
                            formdata=search_data,
                            callback=self.parse)]
    def parse(self, response):
        pass
