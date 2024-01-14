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
    try:
        browser.get(link)
    except:
        return False
    time.sleep(common.PAUSE_LOAD_PAGE)
    if "Error" in browser.title:
        print("News not found")
        return False
    
    # check for Agree button
    try:
         if not button_clicked: browser.find_element_by_id("onetrust-accept-btn-handler").click()
         button_clicked = True
    except:
        print("Button not found")

    time.sleep(2)  
    #load the news     
    try:
        # main news type
        main_div = browser.find_element_by_class_name("l-container")
        h1 = main_div.find_element_by_class_name("pg-headline").text
        section = main_div.find_element_by_class_name("zn-body-text")
        p_list = section.find_elements_by_class_name("zn-body__paragraph")
        h1_text = format_text(h1) +"\n\n" if h1.strip() else ""
        text_news = [ h1_text ] + [ format_text(p.text)+"\n\n" for p in p_list[0:-1] if p.text.strip() and
                                     not any( [el for el in ["CNN","--","contributed to this story"] if el in p.text ]) ]
        
        print("Main format found.")            
    except Exception as e:
        print("Not main format. Trying article format...")  
        try:
            # article type
            div_main = browser.find_element_by_class_name("ls-main")
            article = div_main.find_element_by_tag_name("article")
            h2 = article.find_element_by_tag_name("h2").text
            p_list = article.find_elements_by_class_name("sc-gZMcBi")
            if h2.strip():
                h2_text = format_text(h2)
            else:
                h2_text = ""
            text_news = [format_text(p.text)+"\n\n" for p in p_list if p.text.strip() and
                                     not any( [el for el in ["CNN","--","contributed to this story"] if el in p.text ]) ]
        except:
            print("News format not recognized.")
            return False
        
    # save news    
    if any(text_news):
        space = " - " 
        file_ = os.path.join(folder,common.CNN + space + common.NEWS_FILE)
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
def read_news_from_cnn(base_folder,day):
    global browser

    print("Reading news from ", common.BASE_URL_CNN,"...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()
    browser.maximize_window()
    browser.get(common.BASE_URL_CNN) 
    time.sleep(common.PAUSE_LOAD_PAGE)   
    items = browser.find_elements_by_class_name("itemtitle")
    news_texts = [item.text for item in items]
    news_links = [item.find_element_by_tag_name("a").get_attribute("href") for item in items]
    news_created = 0
    for i in range(len(news_links)):
        if read_news( news_links[i],news_texts[i],folder): news_created += 1
        time.sleep(common.PAUSE_NEXT)    

    browser.close()
    print("News created:",news_created)
    
if __name__=="__main__":
    read_news_from_cnn("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    