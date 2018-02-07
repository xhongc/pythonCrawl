# -*- coding: utf-8 -*-
import scrapy
import json
from cp_plan.items import CpPlanItem, Wait_Item
from scrapy.http import Request
import time


class CpPlansSpider(scrapy.Spider):
    name = 'ffc_all'
    allowed_domains = ['http://56070.la/']
    start_urls = ['http://56070.la/json/ffc.json', 'http://56070.la/json/ffc_h2zx.json',
                  'http://56070.la/json/ffc_h3zx.json', 'http://56070.la/json/ffc_h3z6.json']
    sign_num = 4418

    def parse(self, response):
        html = json.loads(response.body)
        # 最新一条等开计划信息
        endlist = html.get('EndList')
        item = CpPlanItem()
        item['title'] = html.get('NewGame')['WaitGame']
        if response.url == 'http://56070.la/json/ffc.json':
            item['type'] = 51
        elif response.url == 'http://56070.la/json/ffc_h2zx.json':
            item['type'] = 52
        elif response.url == 'http://56070.la/json/ffc_h3zx.json':
            item['type'] = 53
        else:
            item['type'] = 54
        item['gameId'] = 5
        yield item
        # 其余的计划信息
        for each in endlist:
            item = CpPlanItem()
            # print(each)
            item['title'] = each['Ruestl']
            if response.url == 'http://56070.la/json/ffc.json':
                item['type'] = 51
            elif response.url == 'http://56070.la/json/ffc_h2zx.json':
                item['type'] = 52
            elif response.url == 'http://56070.la/json/ffc_h3zx.json':
                item['type'] = 53
            else:
                item['type'] = 54
            item['gameId'] = 5

            yield item
            # 爬取 即刻开奖信息
        item = Wait_Item()
        N1 = html.get('TopGame')['R1']
        N2 = html.get('TopGame')['R2']
        N3 = html.get('TopGame')['R3']
        N4 = html.get('TopGame')['R4']
        N5 = html.get('TopGame')['R5']
        item['num'] = '{0},{1},{2},{3},{4}'.format(N1, N2, N3, N4, N5)
        item['gamedate'] = html.get('TopGame')['gameid']
        item['gameId'] = 5

        yield item


