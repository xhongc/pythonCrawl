# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import urllib
from login.items import LoginItem
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['www.douban.com','accounts.douban.com']
    start_urls = 'https://www.douban.com/people/165693071/'

    def start_requests(self):
        return [Request('https://accounts.douban.com/login',meta={'cookiejar':1},callback=self.login)]

    def login(self,response):
        capt = response.xpath('//div[@class="item item-captcha"]/div/img/@src').extract_first()
        if capt:

            capt_id = response.xpath('//div[@class="captcha_block"]/input/@value').extract_first()
            urllib.request.urlretrieve(capt,filename='captcha.jpg')
            captcha = input('请手动输入captcha:\n')
            data = {
                'source': 'None',
                'redir': 'https://www.douban.com',
                'form_email': '408737515@qq.com',
                'form_password': 'chao123456789..',
                'remember': 'on',
                'login': '登录',
                'captcha-solution': captcha,
                'captcha-id': capt_id
            }
        else:
            print('无验证啊')
            data ={
                'source': 'None',
                'redir': 'https://www.douban.com',
                'form_email': '408737515@qq.com',
                'form_password': 'chao123456789..',
                'remember': 'on',
                'login': '登录'
            }
        return [FormRequest('https://accounts.douban.com/login',
                           method='POST',
                           meta ={'cookiejar': response.meta['cookiejar']},
                           formdata=data,
                           callback=self.after_login)]
    def after_login(self,response):
        return [Request(self.start_urls,
                       meta={'cookiejar':response.meta['cookiejar']},
                       callback=self.parse
                       )]
    def parse(self, response):
        item = LoginItem()
        name = response.xpath("//div[@class='info']/h1/text()").extract_first().strip()
        item['name'] = name

        yield item
