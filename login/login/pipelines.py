# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class LoginPipeline(object):
    def process_item(self, item, spider):
        with open('name.json','w',encoding='utf-8') as f:
            result = json.dumps(dict(item))
            f.write(result)
        return item
