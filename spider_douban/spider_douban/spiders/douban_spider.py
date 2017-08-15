import scrapy
import sys
sys.path.append(r'D:\work\spider_douban\spider_douban')
from items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name='douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self,response):
        item=DoubanItem()
        
        sel = scrapy.selector.Selector(response)
        
        title = sel.xpath("//div[@class='hd']/a/span/text()").extract()
        
        
        star = sel.xpath("//div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()").extract()

        item['title'] = title
        item['star'] = star
        

        return item
        
            
        
