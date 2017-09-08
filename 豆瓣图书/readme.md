## 爬取豆瓣全部图书爬虫

### 获取图书所有标签

```python
def get_tag():

    url= 'https://book.douban.com/tag/?view=cloud'
    headers ={ 'Use-Agent': user_agent() }
    html = SESSION.get(url,headers=headers)
    selector = Selector(html)
    list1 = selector.xpath('//tbody/tr/td/a/text()').extract()

    list1 =list1[7:]

    return list1
```

### 爬取每个标签类下的所有图书

```python
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
```

### 保存为json 格式

```python
def save_books(tag,content):
    file_name = tag+'.json'
    content = json.dumps(content,ensure_ascii=False)+"\n"
    with open(file_name,'a',encoding='utf-8') as f:
        f.write(content)
```

### 运行

```python
def main():
    for tag in get_tag():
        for off in range(100):
            time.sleep(5)
            html = get_TagURL(tag,off*10)
            for book in parse_url(tag,html):
                save_books(tag,book)
```
