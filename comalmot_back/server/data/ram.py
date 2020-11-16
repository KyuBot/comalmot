import time
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pymysql

conn = pymysql.connect(host='k3b206.p.ssafy.io', user='b206',
                       password='b206', db='comalmot', charset='utf8')
cur = conn.cursor()

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(1)
driver.get("http://shop.danawa.com/main/?controller=goods&methods=index&productRegisterAreaGroupSeq=20&serviceSectionSeq=596#1")

n = 1
for p in range(1, 21):
    script = 'movePage(%d)' % p
    driver.execute_script(script)
    time.sleep(5)
    html = driver.page_source
    bs = BeautifulSoup(html, 'html.parser')
    prods_list = bs.find('div', attrs={'class': 'main_prodlist main_prodlist_list'}).findAll(
        'ul', attrs={'class': 'product_list'})

    for prod_list in prods_list:

        prods = prod_list.findAll(
            'li', attrs={'class': 'prod_item'})

        for prod in prods:
            name = prod.find('div', attrs={'class': 'head_info'}).find(
                'a').text.strip()
            price = prod.find('div', attrs={'class': 'price_info'}).find(
                'dl', attrs={'class': 'low_price'}).find('dd').find('span').text.strip()
            # print(f'{n}. {name} / {price}')

            sql = 'INSERT INTO rams (id, name, price) VALUES (%s, %s, %s)'
            data = (n, name, price)
            cur.execute(sql, data)
            n += 1

conn.commit()

print('RAM data init DB')

conn.close()
