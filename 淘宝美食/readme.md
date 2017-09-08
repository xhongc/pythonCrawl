## Selenium + Chorme 实现模拟浏览器爬虫
<br>

> selenium 是一个web的自动化测试工具,免费，小巧，支持C、 java、ruby、python。
> 导入模块 `from selenium import webdriver`
<br>

### 显示等待
- 显示等待的代码定义了等待条件，只有该条件触发，才执行后续代码，WebDriverWait 和 ExpectedCondition 组合使用，就是一种有效的解决手段。

> from selenium.common.exceptions import TimeoutException<br>
> from selenium.webdriver.common.by import By<br>
> from selenium.webdriver.support.ui import WebDriverWait<br>
> from selenium.webdriver.support import expected_conditions as EC<br>

```python
input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        submit = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
```

### 模拟点击实现翻页

```python
        input.clear()
        input.send_keys(page_num)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_num)))
```

### 获取每页源码

```python
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist > div > div')))
    #获取网页源码
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    list1 = soup.findAll('div',{'data-category':'auctions'})
    for each in list1:
        items ={}
        items['title'] = each.find('div','row row-2 title').get_text().strip()
        items['momeny'] = each.find('div','price g_price g_price-highlight').strong.get_text()
        items['people'] = each.find('div','deal-cnt').get_text()[:-3]
        items['name'] = each.find('a','shopname J_MouseEneterLeave J_ShopInfo').get_text().strip()
        save_products(items)
```

### 连接MYSQL 数据库进行储存

```python
conn = pymysql.connect(**db_config)
cursor = conn.cursor()
sql ="insert into taobao(title,momeny,people,name)VALUES (%s,%s,%s,%s)"
    try:
        cursor.execute(sql,(items['title'],items['momeny'],items['people'],items['name']))
        conn.commit()
    except pymysql.Error as e:
        print(e.args)
```
