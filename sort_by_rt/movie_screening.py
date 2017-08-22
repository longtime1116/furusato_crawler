#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
URL = 'http://www.allcinema.net/prog/index2.php'
WOWOW_LINEUP_URL = 'http://www.wowow.co.jp/movie/#lineup'
#DRIVER_PATH = os.path.join(os.path.dirname(__file__), 'chromedriver')
#DRIVER_PATH = "/Users/Shumo/Documents/python/phantomjs"
DRIVER_PATH = "/Users/Shumo/Documents/python/chromedriver"
CHROME_DRIVER_PATH = "/Users/Shumo/Documents/python/chromedriver"
PHANTOMJS_DRIVER_PATH = "/Users/Shumo/Documents/python/phantomjs"

SEARCH_WORD = u"アデル、ブルーは熱い色"
SEARCH_WORD = u"重力ピエロ"
#SEARCH_WORD = 'hoge'

#class WebDriver:
#    """ ドライバー管理クラス """
#    def __init__(self, driverPath):
#        self.browser = webdriver.Crome(driverPath)
#
#    def getBrower(self):
#        return self.browser
#

# wowow から日本語タイトルを引っ張ってくる
def get_japanese_titles(browser):
    is_first = True
    all_titles = []
    page = 1
    while True:
        if is_first:
            # 初回は url から
            browser.get(WOWOW_LINEUP_URL)
            is_first = False
        else:
            # 2 回目以降は、一番下のボタンをクリックして映画リロード
            try:
                time.sleep(1)
                # 一番下のボタンの xpath 取得してクリック
                next_page = browser.find_element_by_xpath('//*[@id="wol_movie_top"]/div[1]/main/div[1]/section[3]/div[3]/div/div[4]/nav/ul/li[2]/ul/li[' + str(page) + ']/a')
                browser.execute_script("arguments[0].click();", next_page)
        
                # そのページにある邦題をすべて取得して出力
                titles = browser.find_elements_by_xpath('//*[@id="wol_movie_top"]/div[1]/main/div[1]/section[3]/div[3]/div/div[3]/ul/li[*]/a/h3/wol-onair-list-title/span')
                if len(titles) == 0:
                    break
                for title in titles:
                    all_titles.append(title.text)
                    print(title.text)
            except Exception:
                break
        page += 1
    return all_titles

# wowow から日本語タイトルを引っ張ってくる
def output_japanese_titles(titles):
    with open('output.csv','wt') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(titles)

if __name__ == '__main__':
#    # ドライバー管理クラスのインスタンスを生成
#    pjsDriver = WebDriver(PHANTOMJS_DRIVER_PATH)
#    chromeDriver = WebDriver(CHROME_DRIVER_PATH)


    # ドライバー取得
#    browser = webdriver.PhantomJS(DRIVER_PATH)
    browser = webdriver.Chrome(DRIVER_PATH)
    try:
        japanese_titles = get_japanese_titles(browser)
        output_japanese_titles(japanese_titles)

    finally:
        browser.quit()
