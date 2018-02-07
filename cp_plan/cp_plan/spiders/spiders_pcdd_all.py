# -*- coding: utf-8 -*-
import scrapy
import json
from cp_plan.items import CpPlanItem, Wait_Item
from scrapy.http import Request
import time


class CpPlansSpider(scrapy.Spider):
    name = 'pcdd_all'
    allowed_domains = ['http://56070.la/']
    start_urls = ['http://56070.la/json/pcdd.json']
    sign_num = 4418

    def parse(self, response):
        html = json.loads(response.body)
        # 最新一条等开计划信息
        endlist = html.get('EndList')
        item = CpPlanItem()
        item['title'] = html.get('NewGame')['WaitGame']
        item['type'] = 41
        item['gameId'] = 4
        yield item
        # 其余的计划信息
        for each in endlist:
            item = CpPlanItem()
            # print(each)
            item['title'] = each['Ruestl']
            item['type'] = 41
            item['gameId'] = 4
            count_num = len(item['title'])
            yield item
            # 爬取 即刻开奖信息
        item = Wait_Item()
        N1 = html.get('TopGame')['R1']
        N2 = html.get('TopGame')['R2']
        N3 = html.get('TopGame')['R3']
        item['num'] = '{0},{1},{2}'.format(N1, N2, N3)
        item['gamedate'] = html.get('TopGame')['gameid']
        item['gameId'] = 4

        yield item


