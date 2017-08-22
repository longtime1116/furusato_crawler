# -*- coding: utf-8 -*-
import lxml.html
import requests
import sys
import codecs

#sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='ignore')

target_url = 'https://tabelog.com/tokyo/A1303/A130302/13001541/'
target_html = requests.get(target_url)
root = lxml.html.fromstring(target_html.text)

# 店の名前を取得
title = root.xpath('//*[@id="rstdtl-head"]/div[1]/div[1]/div[1]/div/div/h2/a/span')
# 点数を取得
score = root.xpath('//*[@id="js-detail-score-open"]/p/b/span')


print title[0].text.strip() + "," + score[0].text
print score[0].text
