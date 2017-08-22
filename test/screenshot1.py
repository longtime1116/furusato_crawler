# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver

DRIVER_PATH = "/Users/Shumo/Documents/python/chromedriver"

if __name__ == '__main__':
    # Chrome の WebDriver のインスタンスを作成
    browser = webdriver.Chrome(DRIVER_PATH)
    try:
        # Google のページを取得
        browser.get('http://www.google.com')
        # 検索ボックスの要素を取得
        search_input = browser.find_element_by_name('q')
        # 検索ワードを入力
        search_input.send_keys(u'クローリング')
        # 送信
        search_input.submit()

        # 検索結果を出力
        titles = browser.find_elements_by_xpath('//h3[@class="r"] ')
        for title in titles:
            print(title.text)
    finally:
        # ブラウザを閉じる
        browser.quit()


