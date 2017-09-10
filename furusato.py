#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime
import sys
import time
import io
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#URL = 'https://www.furusato-tax.jp/search.html?q=%E3%82%B9%E3%83%86%E3%83%BC%E3%82%AD'
#URL = 'https://www.furusato-tax.jp/search.html?q=%E3%81%86%E3%81%AA%E3%81%8E%E3%80%80%E5%B0%BE'
URL = 'https://www.furusato-tax.jp/'
DRIVER_PATH = "/Users/Shumo/develop/furusato_crawler/chromedriver"
#DRIVER_PATH = "/Users/Shumo/develop/furusato_crawler/phantomjs"
SEARCH_WORD = u"うなぎ 尾"
FILENAME = u"うなぎ"
#SEARCH_WORD = u"ステーキ"

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
        if not title or not price:
            print("title or price is not found / url: " + url)
            return None

        if not content:
            content = ""

    info = {}
    info["title"] = title
    info["price"] = price
    info["content"] = content
    info["url"] = url

    return info

def parse_args(argv):
    argc = len(argv)
    if argc < 2:
        return None
    search_word =  ' '.join(argv[1:len(argv)])
    return search_word

def initialize_file(output_file):
    with io.open(output_file, 'w', encoding="shift-jis") as f:
        try:
            f.write(u'title,price,content,url\n')
        except:
            print("fail to write")
            return False
    return True

def add_item_to_file(output_file, sorted_url_dict):
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
                continue

if __name__ == '__main__':
    # ドライバー取得
    browser = webdriver.Chrome(DRIVER_PATH)
#    browser = webdriver.PhantomJS(DRIVER_PATH)
    browser.implicitly_wait(5)

    try:
        search_word = parse_args(sys.argv)

        # 検索ワードがなければ終了
        if search_word is None:
            print("no search word")
            sys.exit()
        else:
            print("search word : " + search_word)

        # 出力ファイル名では、半角スペースはアンダーバーに置換される
        output_file = "result/%s_%s.csv" % (search_word.replace(' ', '_'), datetime.now().strftime('%Y%m%d%H%M'))

        # 一行目出力
        if initialize_file(output_file) is False:
            sys.exit()

        # 検索実行
        browser.get(URL)
        search_input = browser.find_element_by_name('q')
        search_input.send_keys(search_word.decode('utf-8'))
        search_input.submit()
        time.sleep(2)

        # 金額の低い順をクリック
        try:
            price_sorted_page = browser.find_element_by_xpath('//*[@id="contents"]/div[5]/p[1]/a[3]')
        except:
            price_sorted_page = browser.find_element_by_xpath('//*[@id="contents"]/div[4]/p[1]/a[3]')

        url = price_sorted_page.get_attribute('href')
        browser.get(url)
        time.sleep(1)

        # リンク一覧取得
        n_page = 1
        while True:
            try:
                next_page = browser.find_element_by_link_text('次 ＞')
                next_url = next_page.get_attribute('href')
            except:
                print("next page is not found")
                next_url = None

            titles = browser.find_elements_by_xpath('//*[@id="contents"]/div[6]/div/div/div/div/div[*]/div[2]/div/a')
            if len(titles) == 0:
                titles = browser.find_elements_by_xpath('//*[@id="contents"]/div[5]/div/div/div/div/div[*]/div[2]/div/a')

            urls = []
            for title in titles:
                urls.append(str(title.get_attribute('href')))

            # 各お礼の品ページの情報を取得して url_dict に格納
            url_dict = {}
            for url in urls:
                url_info = parse_url(url)
                if url_info is None:
                    continue
                url_dict[url_info["title"]] = url_info
                print(url_info["title"])

            # する必要ないけどなんとなくソート(勉強のため)
            sorted_url_dict = OrderedDict(sorted(url_dict.items(), key=lambda x: (x[1]['price']), reverse=False))

            # ファイルにこのページの情報を書き出す
            add_item_to_file(output_file, sorted_url_dict)

            # 次ページへ遷移
            print(str(n_page) + " page done")
            if next_url is None:
                break
            n_page += 1
            browser.get(next_url)
            time.sleep(1)
    finally:
        browser.quit()

