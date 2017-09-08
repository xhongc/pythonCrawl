## 运用正则表达式匹配信息爬取猫眼TOP
<br>
> 导入模块 re,requests,multiprocessing,json

<br>
1. 获取详情页HTML

```python
    try:
        responese = requests.get(url)
        if responese.status_code ==200:
            return responese.text
        return None
    except RequestException:
        return None
```

2.正则表达式匹配信息

```python
pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?<img data-src="(.*?)".*?alt="(.*?)".*?<p class="star">(.*?)</p>'
                         +'.*?class="releasetime">(.*?)</p>.*?<p class="score"><i class="integer">(.*?)</i>'
                         +'<i class="fraction">(.*?)</i></p>',re.S)
```

3. 保存为json文件

```python
    with open ('result.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
```

4. 启用Multiprocessing.Pool实现多进程

```python
groups = [x*10 for x in range(0,11)]
    pool =Pool(4)
    pool.map(main,groups)
```    
