# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver
URL = 'http://www.google.com'
#DRIVER_PATH = os.path.join(os.path.dirname(__file__), 'chromedriver')
#DRIVER_PATH = "/Users/Shumo/Documents/python/chromedriver"
DRIVER_PATH = "/Users/Shumo/Documents/python/phantomjs"

SEARCH_WORD = 'python'

if __name__ == '__main__':
#    browser = webdriver.Chrome(DRIVER_PATH)
    browser = webdriver.PhantomJS(DRIVER_PATH)
    try:
        browser.get(URL)
        time.sleep(3)
        search_input = browser.find_element_by_name('q')
        search_input.send_keys(SEARCH_WORD)
        search_input.submit()
        time.sleep(3)
        print(browser.title)
        titles = browser.find_elements_by_xpath('//h3[@class="r"] ')
        for title in titles:
            print(title.text)
    finally:
        browser.quit()
