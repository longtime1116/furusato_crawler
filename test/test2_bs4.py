# -*- coding: utf-8 -*-
import lxml.html
import requests
from bs4 import BeautifulSoup



if __name__ == '__main__':
    #target_url = 'https://tabelog.com/tokyo/A1303/A130302/13001541/'
    target_url = 'https://tabelog.com/rstLst/?PG=1&from_search=&voluntary_search=1&SrtT=rt&Srt=D&sort_mode=1&from_search_form=1&lid=&ChkNewOpen=&pcd=13&LstPrf=A1303&LstAre=A130302&station_id=1528&Cat=&LstCat=&LstCatD=&LstCatSD=&RdoCosTp=1&LstCos=0&LstCosT=2&vac_net=0&svps=2&search_date=2016%2F10%2F23%28%E6%97%A5%29&svd=20161023&svt=1930&LstRev=0&sw=&LstKind=01&LstSitu=0&LstReserve=0&LstSmoking=0'
    target_html = requests.get(target_url)
    #root = lxml.html.fromstring(target_html.text)
    soup = BeautifulSoup(target_html.text, "lxml")
    #print soup.find("a")
    for each_a in soup.find_all("a", class_="list-rst__rst-name-target cpy-rst-name"):
        print each_a
    
    #a = soup.find_all("a")
    
    #restaurant_name = a.get(list-rst__rst-name-target cpy-rst-name)
    
    ## 店の名前を取得
    #title = root.xpath('//*[@id="rstdtl-head"]/div[1]/div[1]/div[1]/div/div/h2/a/span')
    ## 点数を取得
    #score = root.xpath('//*[@id="js-detail-score-open"]/p/b/span')
    #
    #
    #print title[0].text.strip() + "," + score[0].text
    #print score[0].text
