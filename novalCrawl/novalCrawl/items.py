# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovalcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    novel_title = scrapy.Field()
    novel_url = scrapy.Field()
    img_url = scrapy.Field()
    finished = scrapy.Field()
    autor = scrapy.Field()
    desc = scrapy.Field()


class NovelContentItem(scrapy.Item):


