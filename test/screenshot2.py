#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
WOWOW_LINEUP_URL = 'http://www.wowow.co.jp/movie/#lineup'
DRIVER_PATH = "/Users/Shumo/Documents/python/chromedriver"
NEXT_BUTTON_XPATH_PRE = '//*[@id="wol_movie_top"]/div[1]/main/div[1]/section[3]/div[3]/div/div[4]/nav/ul/li[2]/ul/li['
NEXT_BUTTON_XPATH_POST = ']/a'
TITLES_XPATH = '//*[@id="wol_movie_top"]/div[1]/main/div[1]/section[3]/div[3]/div/div[3]/ul/li[*]/a/h3/wol-onair-list-title/span'

# wowow 番組表から日本語タイトルを引っ張ってくる
if __name__ == '__main__':
    # ドライバー取得
    browser = webdriver.Chrome(DRIVER_PATH)
    try:
        is_first = True
        page = 1
        while True:
            if is_first:
                # 初回は url から
                browser.get(WOWOW_LINEUP_URL)
                is_first = False
            else:
                # 2 回目以降は、一番下のボタンから次の映画一覧を取得
                try:
                    time.sleep(1)
                    # 一番下のボタンの xpath 取得して遷移
                    next_page = browser.find_element_by_xpath(NEXT_BUTTON_XPATH_PRE +
                                    str(page) + NEXT_BUTTON_XPATH_POST)
                    browser.execute_script("arguments[0].click();", next_page)
                except Exception:
                    break
    
            # そのページにある邦題をすべて取得して出力
            titles = browser.find_elements_by_xpath(TITLES_XPATH)
            if len(titles) == 0:
                break
            for title in titles:
                print(title.text)
            page += 1
    finally:
        browser.quit()
