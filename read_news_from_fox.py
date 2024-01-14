#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Read news from cnn
    Go to cnn site and read X news
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


button_clicked = False

def read_news(link,title,folder):
    global button_clicked,browser
    
    if "LIVE UPDATES" in title: return False
    
    # create folder for the news
    news_folder_name = format_file_name(title)
    news_title = title
    folder = os.path.join(folder,news_folder_name)
    
    if common.already_created(news_folder_name,True):    
        print("News already exists:",news_folder_name)
        return False
    
    os.makedirs(folder)
    
    # load the link in the browser
    image_links = None
    
    print(link)
    browser.get(link)
    time.sleep(common.PAUSE_LOAD_PAGE)
     
    #load the news     
    # try:
        # main news type
    try:
        main_div = browser.find_element_by_class_name("article-content")
        p_list = [p.text for p in main_div.find_elements_by_tag_name("p") if not p.text.isupper() ]
       
        text_news = [ format_text(p)+"\n\n" for p in p_list if p.strip() and (
                                     len(p)>6) and 
                                 not any( [el for el in ["FOX","Check out what's clicking","Check out what's clicking",
                                                         "Click here","Fox News","contributed to this story"] if el in p ]) ]
    except Exception as e:
        print("Error:",e)
        return False
    
    # save news    
    if any(text_news):
        text_news = [ title+"\n\n" ] + text_news
        space = " - " 
        file_ = os.path.join(folder,common.FOX + space + common.NEWS_FILE)
        print("****",file_)
        with open(file_,"w") as f:        
            #print(text_)
            f.writelines( text_news)
        #save title
        with open( os.path.join(folder,common.TITLE_FILE),"w") as f:
            f.write(news_title)
            
        with open( os.path.join(folder,common.LINK_FILE),"w") as f:
            f.write(link)
            
        return True
    else:
        print("News empty. File not created.")
        return False
        
    
            
browser = None
def read_news_from_fox(base_folder,day):
    global browser

    print("Reading news from fox...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()
  
    browser.get(common.BASE_URL_FOX)  
    time.sleep(common.PAUSE_LOAD_PAGE)
  
    div = browser.find_element_by_class_name("main-secondary")
    articles = div.find_elements_by_tag_name("article")
    h2 = [ a.find_element_by_tag_name("h2") for a in articles]
    links = [ h.find_element_by_tag_name("a").get_attribute("href") for h in h2]
    texts = [ h.text for h in h2]
    
    
    
    news_created = 0
    for link,text in zip(links,texts):
        print(link)
        print(text)    
        if read_news( link,text,folder): news_created += 1
        time.sleep(common.PAUSE_NEXT)    

    browser.close()
    print("News created:",news_created)
    
if __name__=="__main__":
    read_news_from_fox("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    