# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from pyquery import PyQuery as pq
from cp_result.items import CpResultItem
class Beijingpk10Spider(scrapy.Spider):
    name = 'beijingpk10'
    url ='http://kaijiang.500.com/static/info/kaijiang/xml/index.xml'
    allowed_domains = ['kaijiang.500.com']
    start_urls = [url]

    def parse(self, response):
        #print(response.body)
        doc = pq(response.body)
        lot_list = doc('lottery')

        for each in lot_list.items():
            item = CpResultItem()
            item['lotshortname'] = each('lotshortname').text()
            item['lottype'] = each('lottype').text()
            item['area'] = each('area').text()
            item['lotchinesename'] = each('lotchinesename').text()
            item['periodicalnum'] = each('periodicalnum').text()
            item['result'] = each('result').text()
            yield item




