#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Read news from bbc
    Go to BBC site and read X news
    Save them as text
    
 
@author: egon
"""
 
import os
import time
import re
import datetime
from new_browser import new_browser
from save_images import save_images
import common

from format_text import format_text,format_file_name

        
def read_news(div,folder):
    # create folder
    news_title = div["short"]
    news_folder_name = format_file_name(div["short"])
    
    if common.already_created(news_folder_name,True): 
        print("News already exists:",news_title)
        return False
           
    folder = os.path.join(folder,news_folder_name)
    os.makedirs(folder)
    
    print(div["link"])
    browser.get(div["link"] )
    time.sleep(common.PAUSE_LOAD_PAGE)
    for button in browser.find_elements_by_class_name("fc-button-label"):
        if button.text=="Consent":
            button.click()
            break
    time.sleep(common.PAUSE_LOAD_PAGE*2)
    
    images = browser.find_elements_by_xpath('//div[@data-component="image-block"]')
    image_links = [i.find_element_by_tag_name("img").get_attribute("src") for i in images ]
    p_divs =  browser.find_elements_by_xpath('//div[@data-component="text-block"]')
    pars = [ p.find_element_by_tag_name("p") for p in p_divs ]
    
    text_ = [ format_text(p.text)+"\n\n" for p in pars if p.text.strip() and 
               not any( [ el for el in ["@bbc","BBC","Newsbeat","Charts by",
                                        "You may also be interested in:"] if el in p.text ]) ]
    
    # save text    
    if any(text_):
        space = " - "
        file_ = os.path.join(folder,common.BBC+space+ common.NEWS_FILE)
        print(file_)
        with open(file_,"w") as f:        
            #print(text_)
            f.writelines( text_)
        #save title
        with open( os.path.join(folder,common.TITLE_FILE),"w") as f:
            f.write(news_title)
        #save images
        save_images(browser,folder,common.BBC,image_links)
        with open(os.path.join(folder,common.LINK_FILE),"w") as f:
            f.write(div["link"])
        return True
    else:
        print("News empty. File not created") 
        return False
             
    
    
browser = None
def read_news_from_bbc(base_folder,day):
    global browser
    print("Reading news from ", common.BASE_URL_BBC,"...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()
    browser.get(common.BASE_URL_BBC)
    divs = [ {"title":div.text,
                "link": a.get_attribute("href"),
                "short": a.text } 
                for div in browser.find_elements_by_id("item")
                    for a in [div.find_element_by_tag_name("a")] ]
    
    total_news = 0
    for div in divs:
        if "/news/" not in div["link"]: continue
        if read_news(div,folder): total_news += 1
        time.sleep(common.PAUSE_NEXT)

    browser.close()
    print("News created:",total_news)
if __name__=="__main__":
    read_news_from_bbc("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    