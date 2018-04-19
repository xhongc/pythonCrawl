# -*- coding: utf-8 -*-
import scrapy


class Cai491Spider(scrapy.Spider):
    name = 'cai491'
    allowed_domains = ['496.cc']
    start_urls = ['http://496.cc/']

    def parse(self, response):
        pass
