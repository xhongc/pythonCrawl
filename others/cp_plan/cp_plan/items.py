# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CpPlanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    gameId = scrapy.Field()
    
class Wait_Item(scrapy.Item):
    num = scrapy.Field()
    gamedate =scrapy.Field()
    gameId = scrapy.Field()

class Cp_wait_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    gameId = scrapy.Field()