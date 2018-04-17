import requests
import random
from useragents import agents
from scrapy.selector import Selector
import re
import time

def user_agent():
    agent = random.choice(agents)
    return agent

def get_ip_num(target_url):
    url = 'https://www.aizhan.com/cha/{0}/'.format(target_url)
    agent = user_agent()
    headers = {'User-Agent':agent}
    html = requests.get(url,headers=headers,timeout=800)
    selector = Selector(html)
    tbody = selector.xpath("//table[@class='table']/tr").extract_first()
    # print(tbody)
    ip_num = re.search('<span id="baidurank_ip" class="red">(.*?)</span> IP</li>',tbody)


    try:
        ip_num = ip_num.group(1)
        if ip_num == '-':
            time.sleep(1)
            print('sleep',target_url)
            get_ip_num(target_url)
        print(target_url, ip_num)
        #save_csv(target_url, ip_num)
    except AttributeError:
        time.sleep(0.3)
        get_ip_num(target_url)

    # return target_url,ip_num

def save_csv(target_url,ip_num):
    with open("before.txt", "a") as f:
        f.write('%s : %s'%(target_url,ip_num))
        f.write('\n')

def save_txt(each):
    with open("after.txt", "a") as f:
        f.write(each)
        f.write('\n')

def chuli():
    with open('target.txt','r',encoding='utf-8') as f:
        for each in f.readlines():
            try:
                each = re.search('([\w-]+\.)+[\w-]+(/[-./?%&=]*)?',each).group(0)
                save_txt(each)
            except:
                pass

if __name__ == '__main__':
    with open('after.txt','r') as f:
        for each in f.readlines():
            if each =='\n':
                pass
            get_ip_num(each)
