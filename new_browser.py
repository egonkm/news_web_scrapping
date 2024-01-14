#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:32:58 2021

@author: egon
"""
from selenium import webdriver

def new_browser():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(10)
    return browser