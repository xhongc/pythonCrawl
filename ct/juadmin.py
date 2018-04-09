import requests
from scrapy.selector import Selector
import time
from pprint import pprint
def get_url(page):
    url = 'https://dns.aizhan.com/118.123.17.15/%s/'%page
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    html = requests.get(url,headers=headers)
    html = Selector(html)
    title = html.xpath("//table[@class='table table-striped table-s1']/tbody")
    res = title.xpath('//td[@class="domain"]/a/@href').extract()

    return res

def save_txt(res):
    with open('result_admin.txt','a') as f:
        f.write(res)
        f.write('\n')

def run_get_url():
    for page in range(1,12):
        try:
            result = get_url(page)
        except:
            time.sleep(2)
        for each in result:
            print(each)
            save_txt(each)
        time.sleep(1)

def test_add_admin():
    with open('result.txt','r') as f:
        for each in f.readlines():
            each = each+'admin'
            each =each.replace('\n','')
            #print(each)
            request_url(each)
def request_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        html = requests.get(url,headers=headers)
        code = html.status_code
        # if 200<code<300:
        #     with open('code.txt','a') as f:
        #         f.write(url)
        #         f.write('\n')
        print(url,code)
    except:
        print('erro:',url)


test_add_admin()



