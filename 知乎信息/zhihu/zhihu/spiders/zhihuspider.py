# -*- coding: utf-8 -*-
import scrapy


class ZhihuspiderSpider(scrapy.Spider):
    name = 'zhihuspider'
    allowed_domains = ['https://zhihu.com']
    start_urls = ['http://https://zhihu.com/']

    def parse(self, response):
        pass
#https://www.zhihu.com/login/phone_num