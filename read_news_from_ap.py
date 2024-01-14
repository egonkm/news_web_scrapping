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

def not_header(p):
    p = p.strip()
    if p.isupper(): return False
    idx = p.find("-")
    if idx>0:
        start = p[0:idx]
        if start.isupper(): return False
        
    return True
    
    
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
        main_div = browser.find_element_by_class_name("Article")
    except:
        return False
    
    p_list = [p.text for p in main_div.find_elements_by_tag_name("p")]
    AP_FIRST_P = "(AP) —"
    idx = p_list[0].find(AP_FIRST_P)
    if idx>-1: p_list[0] = p_list[0][idx+len(AP_FIRST_P)+1:-1]        
    text_news = [ format_text(p)+"\n\n" for p in p_list[0:-1] if p.strip() and ( p[0] != "-") and not_header(p) and (
                                     len(p)>6) and 
                                 not any( [el for el in ["AP","--","contributed to this story"] if el in p ]) ]

    
    try:
        imgs = browser.find_elements_by_class_name("image-0-2-48")
        image_links = [i.get_attribute("src") for i in imgs]
    except:
        image_links = []
            
    # except Exception as e:
    #     print("News format not recognized:",e)
    #     return False
        
    # save news    
    if any(text_news):
        text_news = [ title+"\n" ] + text_news
        space = " - " 
        file_ = os.path.join(folder,common.AP + space + common.NEWS_FILE)
        print("****",file_)
        with open(file_,"w") as f:        
            #print(text_)
            f.writelines( text_news)
        #save title
        with open( os.path.join(folder,common.TITLE_FILE),"w") as f:
            f.write(news_title)
            
        #save images
        if image_links:
            save_images(browser,folder,common.CNN,image_links)
            
        with open( os.path.join(folder,common.LINK_FILE),"w") as f:
            f.write(link)
            
        return True
    else:
        print("News empty. File not created.")
        return False
        
    
            
browser = None
def read_news_from_ap(base_folder,day):
    global browser

    print("Reading news from ", common.BASE_URL_AP,"...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()
    
    browser.get(common.BASE_URL_AP) 
    time.sleep(common.PAUSE_LOAD_PAGE)
    

    iagree = browser.find_element_by_id("onetrust-accept-btn-handler")
    iagree.click()
    close = browser.find_element_by_class_name("sailthru-overlay-close")
    close.click()

    a_list = browser.find_elements_by_tag_name("a")
    els = [a for a in a_list if "title-" in a.get_attribute("class") ]

        
    links = [link.get_attribute("href") for link in els]
    texts = [link.find_element_by_tag_name("h4").text for link in els]
    
    print("Links found:",len(links))
    news_created = 0
    for link,text in zip(links,texts):
        if read_news( link,text,folder): news_created += 1
        time.sleep(common.PAUSE_NEXT)    

    browser.close()
    print("News created:",news_created)
    
if __name__=="__main__":
    read_news_from_ap("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    