#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 13:21:46 2021

@author: egon
"""

import re

def format_text(text):
    result = re.sub("\(.*?\)","",text)
    result = re.sub("\[.*?\]","",result)
    result = result.replace("ADVERTISEMENT","")
    result = result.replace("\\","")
    
    for comma in re.findall(r"\d,\d",result): # comma between digits
        replace_with = comma.replace(",","")
        result = result.replace(comma,replace_with)
        
    for period in re.findall("r[a-z].[A-Z]",result): #  period without space
        replace_with = period.replace(".",". ")
        result = result.replace(period,replace_with)
        
    result = result.replace(".,",".")
    result = result.replace(",.",".")
    
    result = result.replace("ET"," Eastern Time")
    result = result.replace("Ph.D","PHD")
    result = result.replace("Ms.","Miss")
    result = result.replace("Dr.","Doctor ")
    result= result.replace(',"','"')
    result = result.replace("&","and")
    result = result.replace(" ,",", ")
    result = result.replace(" .",".")
    # result = result.replace(". ",".\n") # avoid . , without space afterwards
    result = result.replace(",",", ")
    
    while "  " in result: result = result.replace("  "," ")
    return result

def format_file_name(file_name):
    file_name = file_name.replace("/","-").replace("\\","-").replace(":","").replace("?","").replace("!","")
    return file_name