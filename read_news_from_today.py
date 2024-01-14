#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
     
@author: egon
"""
 
import os
import time
import datetime
from new_browser import new_browser
from save_images import save_images
import common


from format_text import format_text,format_file_name

        
def read_news(link,title,folder):
    # create folder
    if common.TODAY in title: return False
    news_title = title 
    news_folder_name = format_file_name(title)
    folder = os.path.join(folder, news_folder_name)
    
    if common.already_created(news_folder_name,True):    
        print("News already exists:",news_folder_name)
        return False
  
    os.makedirs(folder)

    browser.get(link)
    time.sleep(common.PAUSE_LOAD_PAGE)
    try:
        div = browser.find_element_by_class_name("article-body__content")
        p = div.find_elements_by_tag_name("p")  
        # found the last P of the news text
        idx_last_par = len(p)
        last_p_mark = ["Related:","Related video:","PROTECTED BY RECAPTCHA","Newsletter","CORRECTION"]
        found = None
        for mark in last_p_mark:
            for idx,p_ in enumerate(p):
                if mark in p_.text.strip():
                    idx_last_par = idx
                    found = True
                    break
            if found: break                
        news_text = [ format_text(p_.text)+"\n\n" for p_ in p[0:idx_last_par] if p_.text.strip() and 
                      ("TODAY" not in p_.text) and not p_.text.isupper()  ]
        try:
            iframes = div.find_elements_by_tag_name("iframe")
            idx = -1
            for idx,iframe in enumerate(iframes):
                data = iframe.screenshot_as_png
                with open( os.path.join(folder,"today - "+title+"."+str(idx)+".iframe.png" ),"wb") as f:
                    f.write(data)
            print("IFrames:",idx+1)
        except Exception as e:
            print("No data from iframes:",e)
        image_links = []
        try:
            images = div.find_elements_by_tag_name("img")
            image_links = [i.get_attribute("src") for i in images]
        except:
            print("No images found.")
            
    except Exception as e:
        print("News format not recognized:",e)
        return False
    
    # save text    
    if any(news_text):
        space = " - " 
        file_ = os.path.join(folder,common.TODAY + space + common.NEWS_FILE)
        print(file_)
        with open(file_,"w") as f:        
            #print(text_)
            f.writelines( news_text)
        with open( os.path.join(folder, common.TITLE_FILE),"w") as f:
            f.write( news_title)
        #save images
        if image_links: save_images(browser,folder,common.TODAY,image_links)
        with open( os.path.join(folder,common.LINK_FILE),"w") as f:
            f.write( link)
        return True
    else:
        print("News empty. File not created") 
        return False
             
    
    
browser = None
from selenium.webdriver.common.keys import Keys
def read_news_from_today(base_folder,day):
    global browser
    print("Reading news from ", common.BASE_URL_TODAY,"...")
    print("Date:",day)
    folder = os.path.join(base_folder,day)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not browser: browser = new_browser()

    browser.maximize_window()
    browser.get(common.BASE_URL_TODAY)
    try:
        button = browser.find_element_by_id("cx_button_close")
        button.click()
    except:
        pass
    time.sleep(common.PAUSE_LOAD_PAGE)
    body = browser.find_element_by_tag_name("body")
    for i in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)

    h2 = browser.find_elements_by_class_name("tease-card__title")
    links = [ h.find_element_by_tag_name("a").get_attribute("href") for h in h2] 
    titles = [ h.text for h in h2]
    total_news = 0
    for link,title in zip(links,titles):
        print(link)
        print(title)
        if read_news(link,title,folder): total_news += 1
        time.sleep(common.PAUSE_NEXT)
    

    browser.close()
    print("News created:",total_news)
if __name__=="__main__":
    read_news_from_today("/hdd/news",datetime.datetime.now().strftime("%d-%m-%Y"))
    
    
    