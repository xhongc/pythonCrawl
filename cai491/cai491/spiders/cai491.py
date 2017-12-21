import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from cai491.items import Cai491Item
class CrawlCai491(CrawlSpider):
    name = 'cai491'
    allowed_domains = ["496.cc"]
    start_urls = ["https://496.cc"]

    rules = [
        Rule(LinkExtractor(allow=('zl/List\.Aspx\?id\=([\d]+)')), callback="parse_item1"),
        Rule(LinkExtractor(allow=(r'https://496.cc/zl/articletypelist.aspx?typeid=\d+')),callback='parse_item2')
    ]

    def parse_item1(self,response):
        print(response.url)
        item = Cai491Item()
        li1 = response.xpath("//html/body/div[@class='xx']").extract()
        item['name'] = li1
        print(item)
        yield item


    def parse_utem2(self):
        pass