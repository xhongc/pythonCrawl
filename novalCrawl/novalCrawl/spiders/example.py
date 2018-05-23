# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
from ..items import NovalcrawlItem


class ExampleSpider(scrapy.Spider):
    name = 'quanshu'
    allowed_domains = ['www.quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/list/5_1.html']
    def __init__(self):
        self.retry = 0
    def parse(self, response):
        item = NovalcrawlItem()
        html = Selector(response)
        content = html.xpath('//section/ul/li')
        for each in content:
            item['novel_title'] = each.xpath('./a/img/@alt').extract_first()
            item['novel_url'] = each.xpath('./a/@href').extract_first()
            item['img_url'] = each.xpath('./a/img/@src').extract_first()
            finished_logo = each.xpath('./img/@src').extract_first()
            #print(finished_logo)
            if finished_logo == '/kukuku/images/only2.png':
                item['finished'] = '连载中'
            else:
                item['finished'] = '完结'
            item['autor'] = each.xpath('./span/a/text()').extract()[1]
            try:
                item['desc'] = each.xpath('./span/em/text()').extract_first().strip().replace('\n','').replace(' ','')
            except:
                item['desc'] = '暂无描述'
            #print(item)
            yield item

        try:
            total_page = html.xpath('//section/div/div/em/text()').extract_first().split('/')[1]
            cur_page = response.url.split('/')[-1].replace('.html', '').split('_')[1]
            print(total_page,cur_page)
        except:

            if self.retry < 4:
                yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
                self.retry += 1


        if int(cur_page) < int(total_page):
            cur_page = int(cur_page)
            cur_page += 1
            next_url = response.url.split('_')[0] + '_' + str(cur_page) + '.html'
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse,dont_filter=True)
