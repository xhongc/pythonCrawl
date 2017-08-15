# -*- coding: utf-8 -*-
import scrapy
from lagou.items import LagouItem
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider



class CrawlLagouSpider(RedisSpider):
    page = 1
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    redis_key = 'lagou:start_urls'
    #start_urls = ["https://www.lagou.com/zhaopin/Python/?filterOption=3"]


    def parse(self, response):
        soup= BeautifulSoup(response.text,"html.parser")
        list1 = soup.find_all('li',{'class':'con_list_item default_list'})
        for each in list1:
            item = LagouItem()
            item['title'] = each.attrs['data-positionname']
            salary = each.attrs['data-salary'].lower().split('k')[0]
            item['salary'] = int(salary)*1000
            item['company'] = each.attrs['data-company']
            item['position'] = each.find('span',{'class':'add'}).em.get_text().split('·')[0]
            item['time'] = each.find('span',{'class':'format-time'}).get_text()
            grade = each.find('div',{'class':'li_b_l'}).get_text().split('/')[-1]
            item['grade'] = grade.replace('\n','').replace(' ','')

            yield item

        if self.page <6:
            self.page += 1
            url ="https://www.lagou.com/zhaopin/Python/{page}/?filterOption=3"

            new_url =url.format(page=self.page)

            yield scrapy.Request(new_url,callback=self.parse)



