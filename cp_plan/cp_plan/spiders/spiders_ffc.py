# -*- coding: utf-8 -*-
import scrapy
import json
from cp_plan.items import CpPlanItem, Wait_Item
from scrapy.http import Request
import time


class CpPlansSpider(scrapy.Spider):
    name = 'ffc'
    allowed_domains = ['http://56070.la/']
    start_urls = ['http://56070.la/json/ffc.json', 'http://56070.la/json/ffc_h2zx.json',
                  'http://56070.la/json/ffc_h3zx.json', 'http://56070.la/json/ffc_h3z6.json']
    sign_num = 4418

    def parse(self, response):

        html = json.loads(response.body)
        # 最新一条等开计划信息
        count_num = html.get('NewGame')['WaitGame'].split('期')[2]
        print(count_num)
        # 其余的计划信息
        print(self.sign_num)
        if self.sign_num == 4418:
            print('1:%s' % self.sign_num)
            self.sign_num = count_num
            print('1:%s' % self.sign_num)
            # yield scrapy.Request(response.url,callback=self.parse_data,dont_filter=True)

        if self.sign_num == count_num:
            print('2:%s' % self.sign_num)
            time.sleep(6.66)
            return scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        elif self.sign_num != count_num:

            print('3:%s' % self.sign_num)
            return scrapy.Request(response.url, callback=self.parse_data, dont_filter=True)

    def parse_data(self, response):
        html = json.loads(response.body)
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
            item['gameId'] = '分分彩'
            count_num = len(item['title'])
            yield item
            # 爬取 即刻开奖信息
        item = Wait_Item()
        item['N1'] = html.get('TopGame')['R1']
        item['N2'] = html.get('TopGame')['R2']
        item['N3'] = html.get('TopGame')['R3']
        item['N4'] = html.get('TopGame')['R4']
        item['N5'] = html.get('TopGame')['R5']
        item['N6'] = 4418
        item['N7'] = 4418
        item['N8'] = 4418
        item['N9'] = 4418
        item['N10'] = 4418
        item['gamedate'] = html.get('TopGame')['gameid']
        item['gameId'] = '分分彩'

        yield item


