import requests
from scrapy.selector import Selector
import pymysql
from multiprocessing import Pool
from useragents import agents
import random
import time
from scrapy.selector import Selector

db_config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'xhongc',
    'db':'ippool',
    'charset':'utf8'

}
#链接MySQL数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

def save_inDB(item):

    sql = 'insert into info01(ip,port,type) VALUES (%s,%s,%s)'
    try:
        cursor.execute(sql, (item['ip'], item['port'], item['type']))
        conn.commit()
    except pymysql.Error as e:
        print(e.args)

def user_agent():
    agent = random.choice(agents)
    return agent

def crawl_ips(page):
    headers = {"User-Agent":user_agent()}
    for i in range(page):
        req = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        selector = Selector(text=req.text)
        ip_list = selector.xpath('//tr[@class]')

        for ip in ip_list:
            item={}
            title=ip.xpath('.//td/text()').extract()
            item['ip'] = title[0]
            item['port'] = title[1]
            item['type'] = title[5]

            save_inDB(item)


    time.sleep(1.56)

def judge_ip(ip,port,type,item):
    headers = {"User-Agent": user_agent()}
    if type =='HTTP':
        proxies = {'http':'http://{0}:{1}'.format(ip,port)}
    elif type =='HTTPS':
        proxies = {'https': 'http://{0}:{1}'.format(ip, port)}
    else:
        print(ip,port,type)
    try:
        html = requests.get('http://ip.chinaz.com/',headers=headers, proxies=proxies)
        selector = Selector(html)
        my_ip = selector.xpath("//p[@class='getlist pl10']/text()").extract_first()
    except:
        print('chaoshi')

    if my_ip is None:
        print('none')
    elif my_ip != '61.241.197.247' and html.status_code == 200:
        print(my_ip)

    else:
        print('eeeee%s'%ip)


if __name__ == '__main__':
    pool = Pool(4)
    groups = [x for x in range(10)]
    pool.map(crawl_ips,groups)
