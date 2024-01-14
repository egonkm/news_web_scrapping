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
import datetime
from new_browser import new_browser
from save_images import save_images

base_url_newsweek = "https://www.newsweek.com/"
PAUSE_LOAD_PAGE = 1
PAUSE_NEXT = 0.5
NEWS_FILE = "news.txt"
TITLE_FILE = "title"
NEWSLET = "newsweek"

from format_text import format_text,format_file_name

        
def read_news(link,title,folder):
    # create folder
    news_folder_name = format_file_name(title)
    news_title = title
    folder = os.path.join(folder,news_folder_name)
    if os.path.exists(folder): 
        print("News already exists:",folder)
        return False
    os.makedirs(folder)

    browser.get(link)
    time.sleep(PAUSE_LOAD_PAGE)
    try:
        body = browser.find_element_by_class_name("article-body")
        pars = body.find_elements_by_tag_name("p")
        news_text = []
        ignore_list = ["Log into Facebook to start","Newsweek"]
        for p in pars:
            skip = [i for i in ignore_list if i in p.text] or p.text.strip()
            if skip: continue
            formated = format_text(p.text)
            if formated: news_text.append( formated+"\n\n") 
        
        images = browser.find_elements_by_class_name("imgPhoto")
        image_links = [i.get_attribute("src") for i in images]
    except Exception as e:
        print("News format not recognized:",e)
        return False
    
    # save text    
    if any(news_text):
        space = " - " if NEWSLET else ""
        file_ = os.path.join(folder,NEWSLET + space + NEWS_FILE)
        print(file_)
        with open(file_,"w") as f:        
            #print(text_)
            f.writelines( news_text)
        with open( os.path.join(folder,TITLE_FILE),"w") as f:
            f.write(news_title)
        #save images
        save_images(browser,folder,NEWSLET,image_links)
        return True
    else:
        print("News empty. File not created") 
        return False
             
    
    
browser = None
def read_news_from_newsweek(base_folder,day):
    global browser
    print("Reading news from ", base_url_newsweek,"...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()
    browser.get(base_url_newsweek)
    input("Click in the button and press enter...")
    
    articles = [article for article in browser.find_elements_by_tag_name("article") ]
    links = []
    titles = []
    for article in articles:
        a_ = article.find_elements_by_tag_name("a")
        idx = 2 if len(a_)>2 else 1
        links.append( a_[idx].get_attribute("href"))
        titles.append( a_[idx].text)
    total_news = 0
    for link,title in zip(links,titles):
        print(link)
        print(title)
        if read_news(link,title,folder): total_news += 1
        time.sleep(PAUSE_NEXT)

    browser.close()
    print("News created:",total_news)
if __name__=="__main__":
    read_news_from_newsweek("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    