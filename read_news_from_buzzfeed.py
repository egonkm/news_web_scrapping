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

        
def read_news(link,title,folder):
    # create folder
    news_folder_name = format_file_name(title)
    folder = os.path.join(folder,news_folder_name)
    
    if common.already_created(news_folder_name,True):    
        print("News already exists:",news_folder_name)
        return False
    
    os.makedirs(folder)
    
    print(link)
    browser.get(link)
    browser.implicitly_wait(2)
    try:
        buttons = browser.find_elements_by_tag_name("button")
        button = [button_ for button_ in buttons if "AGREE" in button_.text]
        if button: button[0].click()
    except Exception as e:
        print("Button not found.")
        
    try:
        div = browser.find_element_by_class_name("subbuzz-text")
        paragraphs = div.find_elements_by_tag_name("p")
        news_text = [ format_text(p.text.strip())+"\n\n" for p in paragraphs ]
        images = browser.find_elements_by_class_name("subbuzz-media")
        image_links = [ image.find_element_by_tag_name("img").get_attribute("src") for image in images]
    except Exception as e:
        print("Trying second format...")
        try:
            div = browser.find_element_by_class_name("js-article-wrapper")
            span = div.find_elements_by_class_name("js-subbuzz__title-text")
            news_text = [format_text(span_.text)+"\n\n" for span_ in span]
            images = div.find_elements_by_class_name("subbuzz__media")
            image_links = [ i.find_element_by_tag_name("img").get_attribute("src") for i in images ]
            
        except:
            print("News format unkown.")
            return False
        
    # save text    
    if any(news_text):
        space = " - "
        file_ = os.path.join(folder,common.BUZZFEED+space+ common.NEWS_FILE)
        print(file_)
        with open(file_,"w") as f:        
            #print(text_)
            f.writelines( news_text)
        #save title
        with open( os.path.join(folder,common.TITLE_FILE),"w") as f:
            f.write(title)
        #save images
        save_images(browser,folder,common.BUZZFEED,image_links)
        with open(os.path.join(folder,common.LINK_FILE),"w") as f:
            f.write(link)
        return True
    else:
        print("News empty. File not created") 
        return False
             
    
    
browser = None
def read_news_from_buzzfeed(base_folder,day):
    global browser
    print("Reading news from ", common.BASE_URL_BUZZFEED,"...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()
    browser.get(common.BASE_URL_BUZZFEED)
    
    try:
        buttons = browser.find_elements_by_tag_name("button")
        button = [button_ for button_ in buttons if "AGREE" in button_.text]
        if button: button[0].click()
    except Exception as e:
        print("Button not found:",e)
    
    articles = browser.find_elements_by_class_name("newsblock-story-card")
    h2 = [ article.find_element_by_tag_name("h2") for article in articles]
    links = [ header.find_element_by_tag_name("a").get_attribute("href") for header in h2 ]
    titles = [ header.text for header in h2]
    
    total_news = 0
    for link,title in zip(links,titles):
        if read_news(link,title,folder): total_news += 1
        time.sleep(common.PAUSE_NEXT)

    browser.close()
    print("News created:",total_news)
if __name__=="__main__":
    read_news_from_buzzfeed("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    