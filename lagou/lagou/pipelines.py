# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import json
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

class LagouPipeline(object):
    '''def __init__(self):
        self.f = open('lagou.json','w')
    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii = False) +",\n"
        self.f.write(content)
        return item
    def close_spider(self,spider):
        self.f.close()'''

    def __init__(self):
        self.conn =  pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        sql = 'insert into info01(title,salary,position,time,grade,company) values(%s,%s,%s,%s,%s,%s)'

        try:
            self.cursor.execute(sql,(item['title'],
                                     item['salary'],
                                     item['position'],
                                     item['time'],
                                     item['grade'],
                                     item['company'],

                                     )
                                )
            self.conn.commit()
        except pymysql.Error as e:
            print(e.args)
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()




