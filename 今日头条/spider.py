import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
import re
from bs4 import BeautifulSoup
from hashlib import md5
import os
from multiprocessing import Pool
#获取页面索引页
def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3'
    }
    #编译抓包到的url
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        #判断页面是否能打开，否则抛出一个错误
        if response.status_code ==200:
            return response.text
    except RequestException:
        print('请求索引页出错')
        return None
#解析页面索引页
def parse_page_index(html):
    #将HTML 转成 json格式
    data = json.loads(html)
    #取出DATA中article—url 属性
    if 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')
#获取页面详情页
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code ==200:
            return response.text
    except RequestException:
        print('请求详情页出错')
        return None
#解析页面详情页
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    pattern = re.compile(r'gallery: (.*?)\n',re.S)
    result = re.search(pattern,html)
    if result:
        data = json.loads(result.group(1).rstrip(','))
        sub_images = data.get('sub_images')
        images = [item.get('url') for item in sub_images]
        for image in images:
            download_images(image)
        return {
            'title':title,
            'url':url,
            'images':images
        }
#下载图片
def download_images(url):
    print('正在下崽',url)
    try:
        response = requests.get(url)
        if response.status_code ==200:
            save_images(response.content)
    except RequestException:
        print('请求详情页出错')
        return None
#保存图片
def save_images(content):
    images_name = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(images_name):
        with open(images_name,'wb') as f:
            f.write(content)
#主程序
def main(offset):
    html = get_page_index(offset,'街拍')
    parse_page_index(html)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        result = parse_page_detail(html,url)
        if not result:
            pass

#运行主程序，并执行多进程
if __name__ =='__main__':
    groups = [x*20 for x in range(1,11)]
    pool = Pool()
    pool.map(main,groups)