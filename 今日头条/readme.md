## 多线程抓取今日头条图片
<br />


> AJAX即“Asynchronous Javascript And XML”（异步JavaScript和XML），是指一种创建交互式网页应用的网页开发技术。
> AJAX 是一种用于创建快速动态网页的技术。 
> 通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。 
> 传统的网页（不使用 AJAX）如果需要更新内容，必须重载整个网页页面（html页面）。


<br />
1. 分析今日头条ajax 网页<br>
我们查看网页审查，分析Ajax加载的秘密。 <br>
首先动态加载肯定不是Doc目录下的，所以应该在XHR下查找。 <br>

```python
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
```

<br>
2. 解析页面组成

```python
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
```

<br>
3. 下载图片及保存数据库<br>

```python
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
```            
4. 开启循环和多进程<br>

```python
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
```    
