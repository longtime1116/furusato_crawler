#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
URL = 'https://www.furusato-tax.jp/search.html?q=%E3%82%B9%E3%83%86%E3%83%BC%E3%82%AD'
#DRIVER_PATH = os.path.join(os.path.dirname(__file__), 'chromedriver')
#DRIVER_PATH = "/Users/Shumo/Documents/python/chromedriver"
DRIVER_PATH = "/Users/Shumo/develop/furusato_crawler/chromedriver"
#DRIVER_PATH = "/Users/Shumo/develop/furusato_crawler/phantomjs"

SEARCH_WORD = u"ステーキ"
if __name__ == '__main__':
    # ドライバー取得
    browser = webdriver.Chrome(DRIVER_PATH)
#    browser = webdriver.PhantomJS(DRIVER_PATH)
    browser.implicitly_wait(30)
    try:
        browser.get(URL)
        time.sleep(1)
        # 検索ボックスのエレメントを取得
        #search_input = browser.find_element_by_xpath('//*[@id="searchform"]/dl/dt/input')

        # 検索
        #search_input.send_keys(SEARCH_WORD)
        #search_input.submit()
        #time.sleep(1)

        # リンク一覧取得
        titles = browser.find_elements_by_xpath('//*[@id="contents"]/div[6]/div/div/div/div/div[*]/div[2]/div/a')
        urls = []
        for title in titles:
            urls.append(str(title.get_attribute('href')))

        for url in urls:
            browser.get(url)
            time.sleep(1)

            try:
                main = browser.find_element_by_class_name('itemDitailh1_sp_fontSize').text.replace(u',', u'.')
                price = browser.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/div[4]/div[2]/div[1]/span[1]').text.replace(u',', u'.')
                if not price:
                    price = browser.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/div[3]/div[2]/div[1]/span[1]').text.replace(u",", u".")

                content = browser.find_element_by_class_name('cart_item_detail').text.replace(u",", u".").replace(u'容量', u'').replace(u'\n', u' ')

            except:
                if not main:
                    main = ""
                if not price:
                    price = ""
                if not content:
                    content = ""

            print((main + ', ' + price + ', ' + content + ',' + url))

    finally:
        browser.quit()

