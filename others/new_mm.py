import requests
from scrapy.selector import Selector
import urllib.request
import os
from multiprocessing import Pool

def get_one_page(page_num):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'}
    url = ('http://jandan.net/ooxx/page-{page_num}#comments').format(page_num=page_num)
    html = requests.get(url)
    return html

def parse_page(html):

    selector = Selector(html)
    mm_list = selector.xpath('//ol[@class = "commentlist"]')
    for each in mm_list:
        image_url = each.xpath('.//img/@src').extract()
        for index in range(len(image_url)):
            url = 'http:'+image_url[index]
            yield url

def save_image(url):

    filename = url.split('/')[-1]
    with open (filename,'wb') as f:
        img = urllib.request.urlopen(url).read()
        f.write(img)

def main(page_num):
    print(page_num)
    html = get_one_page(page_num)
    urls = parse_page(html)

    for url in urls:
        save_image(url)

if __name__ == '__main__':
    os.mkdir('folder')
    os.chdir('folder')
    groups= [x for x in range(50)]
    groups.reverse()
    pool = Pool()
    pool.map(main,groups)
