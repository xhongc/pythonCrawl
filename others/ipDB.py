import requests
from scrapy.selector import Selector
import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="xhongc",
    db="ippool"

)
cursor = conn.cursor()

def crawl_ips():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(3):
        req = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        selector = Selector(text=req.text)
        ip_list = selector.xpath('//tr[@class]')

        for ip in ip_list:
            item={}
            title=ip.xpath('.//td/text()').extract()
            item['ip'] = title[0]
            item['port'] = title[1]
            item['type'] = title[5]
            sql ='insert into ip01(ip,port,type) VALUES (%s,%s,%s)'
            cursor.execute (sql,(item['ip'],item['port'],item['type']))

            conn.commit()



class GetIP(object):
    def delete_ip(self,ip):
        delete_sql = "delete from ip01 where ip ='{0}'".format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self,ip,port,type):
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip,port)
        try:
            if type=='HTTP':

                proxy_dict={
                        "http":proxy_url,
                    }
                response = requests.get(http_url,proxies=proxy_dict)
            else:
                proxy_dict = {
                    "https": proxy_url,
                }
                response = requests.get(http_url, proxies=proxy_dict)

        except Exception as e:
            print("inavalid ip an port~~")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code>=200 and code<300:
                print("effective ip")
                return True
            else:
                print("invalid ip an port")
                self.delete_ip(ip)
                return False
    def get_random_ip(self):
        random_sql="select ip,port,type from ip01 order by rand() limit 1"
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            type = ip_info[2]

            judge_re = self.judge_ip(ip,port,type)
            if judge_re:
                return "{2}://{0}:{1}".format(ip,port,type.lower())
            else:
                return self.get_random_ip()

#crawl_ips()
if __name__ == "__main__":
    get_ip=GetIP()
    get_ip.get_random_ip()
    print(get_ip.get_random_ip())



