# -*- coding: utf-8 -*-
import scrapy
import json
from cp_plan.items import CpPlanItem,Wait_Item
from scrapy.http import Request

class CpPlansSpider(scrapy.Spider):
    name = '5fc'
    allowed_domains = ['http://56070.la/']
    start_urls = ['http://56070.la/json/wfc.json' ,'http://56070.la/json/wfc_h2zx.json',
                  'http://56070.la/json/wfc_h3zx.json','http://56070.la/json/wfc_h3z6.json']


    def parse(self, response):

        html = json.loads(response.body)
        # 爬取 即刻开奖信息

        item = Wait_Item()
        item['N1'] =html.get('TopGame')['R1']
        item['N2'] =html.get('TopGame')['R2']
        item['N3'] =html.get('TopGame')['R3']
        item['N4'] =html.get('TopGame')['R4']
        item['N5'] =html.get('TopGame')['R5']
        item['gamedate'] = html.get('TopGame')['gameid']
        item['gameId'] = '五分彩'

        yield item
        # 最新一条等开计划信息
        endlist = html.get('EndList')
        item = CpPlanItem()
        item['title'] = html.get('NewGame')['WaitGame']
        yield item
        # 其余的计划信息
        for each in endlist:
            item = CpPlanItem()
            # print(each)
            item['title'] = each['Ruestl']
            item['type'] = html.get('GameMultiple')['Gt']
            item['gameId'] = '五分彩'
            yield item













