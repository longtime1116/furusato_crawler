#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
import time
import io
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
URL = 'https://www.furusato-tax.jp/search.html?q=%E3%82%B9%E3%83%86%E3%83%BC%E3%82%AD'
DRIVER_PATH = "/Users/Shumo/develop/furusato_crawler/chromedriver"
#DRIVER_PATH = "/Users/Shumo/develop/furusato_crawler/phantomjs"

def parse_url(url):
    browser.get(url)
    time.sleep(1)

    try:
        title = browser.find_element_by_class_name('itemDitailh1_sp_fontSize').text.replace(u',', u'.')
        price = browser.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/div[4]/div[2]/div[1]/span[1]').text.replace(u',', u'')
        if not price:
            price = browser.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/div[3]/div[2]/div[1]/span[1]').text.replace(u",", u"")

        content = browser.find_element_by_class_name('cart_item_detail').text.replace(u",", u".").replace(u'容量', u'').replace(u'\n', u' ')

    except:
        if not title:
            title = ""
        if not price:
            price = ""
        if not content:
            content = ""

    info = {}
    info["title"] = title
    info["price"] = price
    info["content"] = content
    info["url"] = url

    return info


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

        url_dict = {}
#        for url in urls:
#            url_info = parse_url(url)
#            url_dict[url_info["title"]] = url_info
        url = urls[0]
        url_info = parse_url(url)
        url_dict[url_info["title"]] = url_info
        url = urls[1]
        url_info = parse_url(url)
        url_dict[url_info["title"]] = url_info
        url = urls[2]
        url_info = parse_url(url)
        url_dict[url_info["title"]] = url_info

        sorted_url_dict = OrderedDict(sorted(url_dict.items(), key=lambda x: (x[1]['price']), reverse=False))
    finally:
        browser.quit()

    output_file = "result/%s.csv" % SEARCH_WORD
    with io.open(output_file, 'w', encoding="cp932") as f:
        for url_title in sorted_url_dict:
            f.write(
                sorted_url_dict[url_title]["title"] + ',' + \
                sorted_url_dict[url_title]["price"] + ',' + \
                sorted_url_dict[url_title]["content"] + ',' + \
                sorted_url_dict[url_title]["url"] + '\n'
            )
