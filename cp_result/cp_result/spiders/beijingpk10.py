# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class Beijingpk10Spider(scrapy.Spider):
    name = 'beijingpk10'
    self.a = datetime.now().year
    self.b = datetime.now().month
    self.c = datetime.now().day
    self.today = int(str(self.a) + str(self.b) + str(self.c))  # year month day
    url ='https://www.77c38.com/static//data/HistoryLottery.js?callback=jsonpCallback&dateStr={0}&gameId=50'.format(date)

    allowed_domains = ['www.77c38.com']
    start_urls = [url]

    def parse(self, response):
        pass
