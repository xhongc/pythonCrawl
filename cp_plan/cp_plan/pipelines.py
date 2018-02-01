# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from cp_plan.items import CpPlanItem,Wait_Item
import pymysql
#数据库配置信息
db_config = {
    'host':'uupp777.vicp.cc',
    'port': 28771,
    'user':'root',
    'password':'quziwei123',
    'db':'info',
    'charset':'cpjh',
}

class CpPlanPipeline(object):
    def __init__(self):
        self.f = open('plan_content.json','w',encoding='utf-8')
        self.g = open('open_wait.json', 'w', encoding='utf-8')
        self.sign_count = 0
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


# class CpPlanPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect(**db_config)
#         self.cursor = self.conn.cursor()
#     def process_item(self, item, spider):
#
#         if isinstance(item, CpPlanItem):
#             # 你的处理方法
#             sql = 'insert into cp_info(ticket_infomation,game_id,ticket_id) values(%s,%s,%s)'
#
#             try:
#                 self.cursor.execute(sql, (item['title'],
#                                           item['type'],
#                                           item['gameId']
#
#                                           )
#                                     )
#                 self.conn.commit()
#             except pymysql.Error as e:
#                 print(e.args)
#             return item
#         else:
#             sql = 'insert into cp_lottery(number,issue,ticket_id) values(%s,%s,%s)'
#
#             try:
#                 self.cursor.execute(sql, (
#                                           item['num'],
#                                           item['gamedate'],
#                                           item['gameId']
#
#                                           )
#                                     )
#                 self.conn.commit()
#             except pymysql.Error as e:
#                 print(e.args)
#             return item
#
#     def close_spider(self, spider):
#         self.cursor.close()
#         self.conn.close()

