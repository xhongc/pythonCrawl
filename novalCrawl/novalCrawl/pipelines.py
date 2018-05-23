# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

# 数据库配置信息
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'xhongc',
    'db': 'novel',
    'charset': 'utf8',

}


class NovalcrawlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into novel_info(novel_title,novel_url,img_url,finished,autor,description) ' \
              'values(%s,%s,%s,%s,%s,%s)'

        try:
            self.cursor.execute(sql, (item['novel_title'],
                                      item['novel_url'],
                                      item['img_url'],
                                      item['finished'],
                                      item['autor'],
                                      item['desc'],

                                      )
                                )
            self.conn.commit()
        except pymysql.Error as e:
            print(e.args)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
