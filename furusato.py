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

    title = ""
    price = ""
    content = ""

    try:
        title = browser.find_element_by_class_name('itemDitailh1_sp_fontSize').text.replace(u',', u'.')
        price = browser.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/div[4]/div[2]/div[1]/span[1]').text.replace(u',', u'')
        if not price:
            price = browser.find_element_by_xpath('//*[@id="main"]/div[4]/div[2]/div[3]/div[2]/div[1]/span[1]').text.replace(u",", u"")

        content = browser.find_element_by_class_name('cart_item_detail').text.replace(u",", u".").replace(u'容量', u'').replace(u'\n', u' ')

    except:
        if not title or not price or not content:
            print("title, price or content is not found")
            print("    url: " + url)
            return None

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
    browser.implicitly_wait(5)
    output_file = "result/%s.csv" % SEARCH_WORD
    with io.open(output_file, 'w', encoding="shift-jis") as f:
        try:
            f.write(u'title,price,content,url\n')
        except:
            print("fail to write")
    try:
        browser.get(URL)

        # 金額の低い順をクリック
        price_sorted_page = browser.find_element_by_xpath('//*[@id="contents"]/div[5]/p[1]/a[3]')
        url = price_sorted_page.get_attribute('href')
        browser.get(url)
        time.sleep(1)
        # 検索ボックスのエレメントを取得
        #search_input = browser.find_element_by_xpath('//*[@id="searchform"]/dl/dt/input')

        # 検索
        #search_input.send_keys(SEARCH_WORD)
        #search_input.submit()
        #time.sleep(1)

        # リンク一覧取得
        n_page = 1
        while True:
            try:
                next_page = browser.find_element_by_link_text('次 ＞')
            except:
                break

            next_url = next_page.get_attribute('href')
            titles = browser.find_elements_by_xpath('//*[@id="contents"]/div[6]/div/div/div/div/div[*]/div[2]/div/a')
            urls = []
            for title in titles:
                urls.append(str(title.get_attribute('href')))

            url_dict = {}
            for url in urls:
                url_info = parse_url(url)
                if url_info is None:
                    continue
                url_dict[url_info["title"]] = url_info
                print(url_info["title"])

#            url = urls[0]
#            url_info = parse_url(url)
#            if url_info is not None:
#                url_dict[url_info["title"]] = url_info
#                print(url_info["title"])
#            url = urls[1]
#            url_info = parse_url(url)
#            if url_info is not None:
#                url_dict[url_info["title"]] = url_info
#                print(url_info["title"])

            sorted_url_dict = OrderedDict(sorted(url_dict.items(), key=lambda x: (x[1]['price']), reverse=False))

            with io.open(output_file, 'a', encoding="shift-jis") as f:
                for url_title in sorted_url_dict:
                    try:
                        f.write(
                            sorted_url_dict[url_title]["title"] + ',' + \
                            sorted_url_dict[url_title]["price"] + ',' + \
                            sorted_url_dict[url_title]["content"] + ',' + \
                            sorted_url_dict[url_title]["url"] + '\n'
                        )
                    except:
                        print("fail to write")
            browser.get(next_url)
            print(str(n_page) + " page done")
            n_page += 1
    finally:
        browser.quit()

