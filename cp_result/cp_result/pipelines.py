# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
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

class CpResultPipeline(object):
    def __init__(self):
        self.conn =  pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        sql = 'insert into kj_500(lotshortname,lottype,area,lotchinesename,period,result) values(%s,%s,%s,%s,%s,%s)'

        try:
            self.cursor.execute(sql, (item['lotshortname'],
                                      item['lottype'],
                                      item['area'],
                                      item['lotchinesename'],
                                      item['periodicalnum'],
                                      item['result'],

                                      )
                                )
            self.conn.commit()
        except pymysql.Error as e:
            print(e.args)
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
