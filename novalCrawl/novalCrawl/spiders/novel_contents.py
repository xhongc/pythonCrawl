import scrapy
import pymysql
from scrapy.selector import Selector


class Novel_contents(scrapy.Spider):
    name = 'contents'

    def start_requests(self):
        db = pymysql.connect(host="localhost", user="root", passwd="xhongc", db="novel", charset='utf8',
                             use_unicode=False)
        cur = db.cursor()
        cur.execute("select novel_url from novel_info")

        for url in cur.fetchall():
            url = str(url[0], encoding='utf-8')  # http://www.quanshuwang.com/book_139577.html
            url = url.replace('_', '/1/').replace('.html', '')
            # print(url)
            yield scrapy.Request(url, self.parse_start)

        cur.close()
        db.close()

    def parse_start(self, response):
        html = Selector(response)
        start_url = html.xpath('//div[@class="clearfix dirconone"]/li/a/@href').extract()
        for title_url in start_url:
            # print(title_url,response.url)
            yield scrapy.Request(title_url, self.parse)

    def parse(self, response):
        html = Selector(response)
        contents = html.xpath('//div[@id="content"]/text()').extract()
        contents = ''.join(contents)
        contents = contents.replace('\r','').replace('\n','').replace(' ','')
        print(contents,response.url)
