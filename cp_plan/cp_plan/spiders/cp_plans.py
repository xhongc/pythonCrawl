# -*- coding: utf-8 -*-
import scrapy
import json
from cp_plan.items import CpPlanItem

class CpPlansSpider(scrapy.Spider):
    name = 'cp_plans'
    allowed_domains = ['http://56070.la/']
    start_urls = ['http://56070.la/json/wfc.json?r=0.39526537519666616']

    def parse(self, response):
        html = json.loads(response.body)
        endlist = html.get('EndList')
        for each in endlist:
            item = CpPlanItem()
            item['title'] = each['Ruest1']
            item['wait_title'] = html.get('NewGame')['WaitGame']
            item['type'] = html.get('GameMultiple')['Gt']