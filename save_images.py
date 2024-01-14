#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 16:15:08 2021

@author: egon
"""

import os
import requests
import time
from PIL import Image

PAUSE_NEXT = 0.2
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def save_images(browser,folder,newslet,image_links):
    counter = 0
    for image in image_links:
        if image[0:5]=="data:": continue
        print("Saving (%s): %s" % (counter,image))
        space = " - " if newslet else ""
        filename = os.path.join(folder,newslet + space+"image."+str(counter+1)+".jpg")
        #print(counter,"Filename:",filename)
        
        try:
            image = requests.get(image,headers=header,timeout=10)
            if image.status_code != 200:
                print("Error:",image.reason)
                continue
            #print("Content:", len(image.content))
            with open(filename,"wb") as f:
                f.write(image.content)
            try:
                img = Image.open(filename)
                w,h = img.size
                if w<640 or h<480:
                    continue
            except Exception as e:
                print("Error PIL:",e)
                continue
            counter += 1
        except Exception as e:
            print("Error:",e)
            
        time.sleep(PAUSE_NEXT)
    return counter
        