# -*- coding: utf-8 -*-
import scrapy
import json
from cp_plan.items import CpPlanItem, Wait_Item
from scrapy.http import Request
import time


class CpPlansSpider(scrapy.Spider):
    name = 'pk10'
    allowed_domains = ['http://56070.la/']
    start_urls = ['http://56070.la/json/pk10.json']
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
            item['type'] = 31
            item['gameId'] = 3
            count_num = len(item['title'])
            yield item
            # 爬取 即刻开奖信息
        item = Wait_Item()
        N1 = html.get('TopGame')['R1']
        N2 = html.get('TopGame')['R2']
        N3 = html.get('TopGame')['R3']
        N4 = html.get('TopGame')['R4']
        N5 = html.get('TopGame')['R5']
        N6 = html.get('TopGame')['R6']
        N7 = html.get('TopGame')['R7']
        N8 = html.get('TopGame')['R8']
        N9 = html.get('TopGame')['R9']
        N10 = html.get('TopGame')['R10']
        item['num'] = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}'.format(N1, N2, N3, N4, N5,N6,N7,N8,N9,N10)
        item['gamedate'] = html.get('TopGame')['gameid']
        item['gameId'] = 3

        yield item


