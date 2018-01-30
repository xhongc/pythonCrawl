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
    'host':'127.0.0.1',
    'port': 3306,
    'user':'root',
    'password':'xhongc',
    'db':'info',
    'charset':'utf8',
}

# class CpPlanPipeline(object):
#     def __init__(self):
#         self.f = open('plan_content.json','w',encoding='utf-8')
#         self.g = open('open_wait.json', 'w', encoding='utf-8')
#         self.sign_count = 0
#     def process_item(self, item, spider):
#
#         if isinstance(item, CpPlanItem):
#             # 你的处理方法
#             content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
#             self.f.write(content)
#             return item
#         else:
#             content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
#             self.g.write(content)
#             return item
#
#     def close_spider(self,spider):
#         self.f.close()
#         self.g.close()


class CpPlanPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):

        if isinstance(item, CpPlanItem):
            # 你的处理方法
            sql = 'insert into cp_plan_title(title,type,gameId) values(%s,%s,%s)'

            try:
                self.cursor.execute(sql, (item['title'],
                                          item['type'],
                                          item['gameId']

                                          )
                                    )
                self.conn.commit()
            except pymysql.Error as e:
                print(e.args)
            return item
        else:
            sql = 'insert into cp_plan_opening(N1,N2,N3,N4,N5,N6,N7,N8.N9,N10,gamedate,gameId) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            try:
                self.cursor.execute(sql, (item['N1'],
                                          item['N2'],
                                          item['N3'],
                                          item['N4'],
                                          item['N5'],
                                          item['N6'],
                                          item['N7'],
                                          item['N8'],
                                          item['N9'],
                                          item['N10'],
                                          item['gamedate'],
                                          item['gameId']

                                          )
                                    )
                self.conn.commit()
            except pymysql.Error as e:
                print(e.args)
            return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

