import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pymysql
from config import *
from multiprocessing import Pool

driver = webdriver.Chrome(executable_path='D:\work\chromedriver\chromedriver.exe')
wait = WebDriverWait(driver, 10)
# 链接MySQL数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()


def search():
    try:
        driver.get('https://www.taobao.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))

        input.send_keys('美食')
        submit.click()
        # 返回总页数
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        search()


def next_page(page_num):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        # 清除输入框数据
        input.clear()
        input.send_keys(page_num)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_num)))
        get_products()
    except TimeoutException:
        next_page(page_num)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist > div > div')))
    # 获取网页源码
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    list1 = soup.findAll('div', {'data-category': 'auctions'})
    for each in list1:
        items = {}
        items['title'] = each.find('div', 'row row-2 title').get_text().strip()
        items['momeny'] = each.find('div', 'price g_price g_price-highlight').strong.get_text()
        items['people'] = each.find('div', 'deal-cnt').get_text()[:-3]
        items['name'] = each.find('a', 'shopname J_MouseEneterLeave J_ShopInfo').get_text().strip()
        save_products(items)


def save_products(items):
    # with open('products.json','a',encoding='utf-8') as f:
    #   f.write(json.dumps(content,ensure_ascii=False)+'\n')

    sql = "insert into taobao(title,momeny,people,name)VALUES (%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (items['title'], items['momeny'], items['people'], items['name']))
        conn.commit()
    except pymysql.Error as e:
        print(e.args)


def main():
    try:
        total = search()
        total = int(re.compile(r'.*?(\d+)').search(total).group(1))
        for i in range(1, total + 1):
            next_page(i)
    finally:
        driver.close()
        cursor.close()
        cnn.close()


if __name__ == '__main__':
    main()
