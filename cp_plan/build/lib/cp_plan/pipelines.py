# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from cp_plan.items import CpPlanItem,Wait_Item

class CpPlanPipeline(object):
    def __init__(self):
        self.f = open('plan_content.json','w',encoding='utf-8')
        self.g = open('open_wait.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        if isinstance(item, CpPlanItem):
            # 你的处理方法
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.f.write(content)
            return item
        else:
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.g.write(content)
            return item

    def close_spider(self,spider):
        self.f.close()
        self.g.close()

# class WaitPipeline(object):
#     def __init__(self):
#         self.f = open('open_wait.json','w',encoding='utf-8')
#     def process_item(self, item2, spider):
#         if isinstance(item2, Wait_Item):
#             content = json.dumps(dict(item2), ensure_ascii=False) + ",\n"
#             self.f.write(content)
#             return item2
#         else:
#             pass
#     def close_spider(self,spider):
#         self.f.close()
