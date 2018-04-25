# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CpResultItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    lotshortname = scrapy.Field()
    lottype = scrapy.Field()
    area = scrapy.Field()
    lotchinesename = scrapy.Field()
    periodicalnum = scrapy.Field()
    result = scrapy.Field()
