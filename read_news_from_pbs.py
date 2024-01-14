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
        main_div = browser.find_element_by_class_name("body-text")
        p_list = [p.text for p in main_div.find_elements_by_tag_name("p")]       
        text_news = [ format_text(p)+"\n\n" for p in p_list[0:-1] if p.strip() and (
                                         len(p)>6) and 
                                     not any( [el for el in ["READ MORE","WATCH","contributed to this story"] if el in p ]) ]
    except Exception as e:
        print("Error:",e)
        return False
    
    # save news    
    if any(text_news):
        text_news = [ title+"\n" ] + text_news
        space = " - " 
        file_ = os.path.join(folder,common.PBS + space + common.NEWS_FILE)
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
def read_news_from_pbs(base_folder,day):
    global browser

    print("Reading news from pbs...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()
    
    feeds = [ "https://www.pbs.org/newshour/feeds/rss/headlines","https://www.pbs.org/newshour/feeds/rss/politics",
            "https://www.pbs.org/newshour/feeds/rss/education","https://www.pbs.org/newshour/feeds/rss/health",
            "https://www.pbs.org/newshour/feeds/rss/arts","https://www.pbs.org/newshour/feeds/rss/nation",
            "https://www.pbs.org/newshour/feeds/rss/world","https://www.pbs.org/newshour/feeds/rss/economy",
            "https://www.pbs.org/newshour/feeds/rss/science"]
    
    links = []
    texts = []
    TITLE = "<title><![CDATA["
    
    for feed in feeds:
        browser.get(feed) 
        time.sleep(common.PAUSE_LOAD_PAGE)
        txt = browser.find_element_by_tag_name("body").text
        idx = txt.find("<item>")
        
        while idx>-1:
            end_idx = txt.find("</item>",idx)
            item = txt[idx:end_idx]
            idx = txt.find("<item>",end_idx)
            if any( [txt for txt in ["Associated Press","WATCH LIVE" ,"/show/" ]  if txt in item]): continue
        
            idx_link = item.find("<link>")
            if idx_link == -1: continue
            end = item.find("</link>",idx_link)
            link = item[idx_link+6:end]
            idx_title = item.find(TITLE)
            if idx_title == -1: continue
            end_title = item.find("]]></title>",idx_title)
            title = item[idx_title+len(TITLE):end_title]
            links.append(link)
            texts.append(title)
        
    
    news_created = 0
    for link,text in zip(links,texts):
        print(link)
        print(text)
        print("-----")
        if read_news( link,text,folder): news_created += 1
        time.sleep(common.PAUSE_NEXT)    

    browser.close()
    print("News created:",news_created)
    
if __name__=="__main__":
    read_news_from_pbs("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    