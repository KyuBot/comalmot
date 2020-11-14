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
driver.get("http://shop.danawa.com/main/?controller=goods&methods=index&productRegisterAreaGroupSeq=20&serviceSectionSeq=597#4")
emtech = driver.find_elements_by_xpath('//*[@id="makerCode_1"]')
zotac = driver.find_elements_by_xpath('//*[@id="makerCode_3"]')
galaxy = driver.find_elements_by_xpath('//*[@id="makerCode_4"]')
emtech[0].click()
zotac[0].click()
galaxy[0].click()
n = 1
for p in range(1, 4):
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
            img_src = prod.find('a', attrs={'class': 'thumb_link'}).find('img')[
                'src']
            print(f'{n}. {name} / {price}')

            sql = 'INSERT INTO gpus (id, name, price, img_src) VALUES (%s, %s, %s, %s)'
            data = (n, name, price, img_src)
            cur.execute(sql, data)
            n += 1
            # sql = "UPDATE gpus SET img_src = %s WHERE id = %s"
            # data = (img_src, n)
            # cur.execute(sql, data)
            # n += 1

conn.commit()

print('GPU data init DB')

conn.close()
