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
