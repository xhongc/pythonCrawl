import requests
from scrapy.selector import Selector
from useragents import agents
import random
import json
import time
import urllib

def user_agent():
    agent = random.choice(agents)

    return agent
headers = {'Use-Agent': user_agent()}

def get_captcha():
    url = 'https://accounts.douban.com/login'
    html = requests.get(url,headers=headers)
    selector = Selector(html)
    capt = selector.xpath('//div[@class="item item-captcha"]/div/img/@src').extract_first()
    capt_id = selector.xpath('//div[@class="captcha_block"]/input/@value').extract_first()
    with open ('captcha.jpg','wb') as f:
        f.write(urllib.request.urlopen(capt).read())
    capt = input('请输入验证码：\n')
    return capt,capt_id
def login():
    capt=get_captcha()
    url='https://accounts.douban.com/login'
    data ={
        'source':'None',
        'redir':'https://www.douban.com',
        'form_email': '408737515@qq.com',
        'form_password': '****',
        'remember':'on',
        'login': '登录',
        'captcha-solution': capt[0],
        'captcha-id': capt[1]
    }
    session = requests.session()
    res= session.post(url,headers=headers,data=data)
    return session
SESSION = login()
def get_tag():

    url= 'https://book.douban.com/tag/?view=cloud'
    headers ={ 'Use-Agent': user_agent() }
    html = SESSION.get(url,headers=headers)
    selector = Selector(html)
    list1 = selector.xpath('//tbody/tr/td/a/text()').extract()

    list1 =list1[7:]

    return list1
def get_TagURL(tag,offset=0):

    tagurl = 'https://book.douban.com/tag/%s?start=%s'% (tag,offset)

    try:
        html = SESSION.get(tagurl,headers=headers)
        if html.status_code == 200:
            return html

    except:
        print('%s is error' % tag)
        return None

def parse_url(tag,html):
    try:
        selector = Selector(html)
        list2 = selector.xpath("//li[@class='subject-item']")
        books = {}
        for each in list2:
            books['name'] = each.xpath(".//h2/a/@title").extract_first()
            books['link'] = each.xpath(".//h2/a/@href").extract_first()
            books['detail']= each.xpath(".//div[@class='pub']/text()").extract_first().strip()
            books['star'] = each.xpath(".//div[@class='star clearfix']/span[@class='rating_nums']/text()").extract_first()
            books['content'] = each.xpath(".//div[@class='info']/p/text()").extract_first()
            yield books
    except:
        pass

def save_books(tag,content):
    file_name = tag+'.json'
    content = json.dumps(content,ensure_ascii=False)+"\n"
    with open(file_name,'a',encoding='utf-8') as f:
        f.write(content)



def main():
    for tag in get_tag():
        for off in range(100):
            time.sleep(5)
            html = get_TagURL(tag,off*10)
            for book in parse_url(tag,html):
                save_books(tag,book)



if __name__ =='__main__':

    main()
