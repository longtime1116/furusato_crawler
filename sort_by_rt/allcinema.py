#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
URL = 'http://www.allcinema.net/prog/index2.php'
#DRIVER_PATH = os.path.join(os.path.dirname(__file__), 'chromedriver')
DRIVER_PATH = "/Users/Shumo/Documents/python/chromedriver"
#DRIVER_PATH = "/Users/Shumo/Documents/python/phantomjs"

SEARCH_WORD = u"アデル、ブルーは熱い色"
#SEARCH_WORD = u"重力ピエロ"
#SEARCH_WORD = 'hoge'
if __name__ == '__main__':
    # ドライバー取得
    browser = webdriver.Chrome(DRIVER_PATH)
#    browser = webdriver.PhantomJS(DRIVER_PATH)
    try:
        browser.get(URL)
        time.sleep(1)
        # 検索ボックスのエレメントを取得
        search_input = browser.find_element_by_name('SearchTxt')

        # 検索
        search_input.send_keys(SEARCH_WORD)
        search_input.submit()
        time.sleep(1)
        # print(browser.title)
        # 作品名取得
        title = browser.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[2]/table[4]/tbody/tr/td[3]/a')
        #print("作品名 : {0}").format(title.text)
        print(u"作品名 : " + title.text)

        url_title = title.get_attribute('href')
        print(u"「" + title.text + u"」の URL : " + url_title)
        time.sleep(1)

        # タイトルのページに移動(原題を知るため)
        browser.get(url_title)

        foreign_title = browser.find_element_by_xpath('//*[@id="contentleft"]/div[1]/div[3]/h2')
        english_title = foreign_title.text.split("\n")[-1]

        print(english_title)

        time.sleep(1)

    finally:
        browser.quit()

