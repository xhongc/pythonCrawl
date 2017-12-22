import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from cai491.items import Cai491Item
class CrawlCai491(CrawlSpider):
    name = 'cai491'
    allowed_domains = ["496.cc"]
    start_urls = ["https://496.cc"]

    rules = [
        Rule(LinkExtractor(allow=('/zl/List\.Aspx\?id\=([\d+])'))),
        Rule(LinkExtractor(allow=('/zl/view\.aspx.*?')),callback='parse_item1')
    ]

    def parse_item1(self,response):
        url = response.url
        item = Cai491Item()
        li1 = response.xpath("//html/body/div[@class='xx']").extract()
        item['name'] = url
        #print(item)
        yield item


    # def parse_item2(self):
    #     url2 = response.url
    #     print(url2)
    #     tem = Cai491Item()
    #     item['name'] = url2
    #     yield item
