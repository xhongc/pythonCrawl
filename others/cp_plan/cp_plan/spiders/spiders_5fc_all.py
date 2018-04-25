# -*- coding: utf-8 -*-
import scrapy
import json
from cp_plan.items import CpPlanItem,Wait_Item
from scrapy.http import Request
import time

class CpPlansSpider(scrapy.Spider):
    name = '5fc_all'
    allowed_domains = ['http://56070.la/']
    start_urls = ['http://56070.la/json/wfc.json' ,'http://56070.la/json/wfc_h2zx.json',
                  'http://56070.la/json/wfc_h3zx.json','http://56070.la/json/wfc_h3z6.json']
    sign_num = 4418

    def parse(self,response):
        html = json.loads(response.body)
        # 最新一条等开计划信息
        endlist = html.get('EndList')
        item = CpPlanItem()
        item['title'] = html.get('NewGame')['WaitGame']
        if response.url == 'http://56070.la/json/wfc.json':
            item['type'] = 11
        elif response.url == 'http://56070.la/json/wfc_h2zx.json':
            item['type'] = 12
        elif response.url == 'http://56070.la/json/wfc_h3zx.json':
            item['type'] = 13
        else:
            item['type'] = 14

        item['gameId'] = 1
        yield item
        # 其余的计划信息
        for each in endlist:
            item = CpPlanItem()
            # print(each)
            item['title'] = each['Ruestl']
            if response.url == 'http://56070.la/json/wfc.json':
                item['type'] = 11
            elif response.url == 'http://56070.la/json/wfc_h2zx.json':
                item['type'] = 12
            elif response.url == 'http://56070.la/json/wfc_h3zx.json':
                item['type'] = 13
            else:
                item['type'] = 14

            item['gameId'] = 1

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
        item['gameId'] = 1

        yield item


