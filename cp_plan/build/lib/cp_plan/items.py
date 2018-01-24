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
    N1 =scrapy.Field()
    N2 =scrapy.Field()
    N3 =scrapy.Field()
    N4 =scrapy.Field()
    N5 =scrapy.Field()
    gamedate =scrapy.Field()
    gameId = scrapy.Field()