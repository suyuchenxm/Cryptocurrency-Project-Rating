#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 00:55:53 2019

@author: surichen
"""
"""
In this file, selenium, requests and BeautifulSoup are used to scraping the cryptocurrency features
The process includes:
1. using selenuim create the webdriver
2. continuely unroll the webpage
3. clone all the hyper link/ urls of projects
4. collect features data includes: 
    project name, 
    Websites,
    white paper,
    country,
    ticker name,
    Total supply,
    ICO Price,
    Hard Cap,
    Twitter, facebook, Linkedin url
    
"""
import selenium
import requests
import json
import datetime
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

#reproducible file stored all the Projects Url in icomarks.com
#links=pd.read_csv('links.csv')

def get_ico_page(url):
    """
    requests the page
    """
    url='https://icomarks.com'+url
    page=requests.get(url)
    while page.status_code==200:
        soup=BeautifulSoup(page.content,'lxml')
        return soup
    
def get_ICO_details(soup,name):
    """
    function get the feautre data from Projects websites in icomarks.com
    """
    data={}
    data['project name'] = name
    for div in soup.find_all('div','icoinfo-block__item'):     
        line = div.text.strip().replace(':\r','').split("\n")
        if len(line) == 2:
            data[line[0]] = line[1]
        elif len(line) == 1:
            link = div.a.get('href')
            if link:
                data[line[0]] = link
        elif line[0].startswith('Website'):
            link = div.a.get('href')
            if link:
                data[line[0]] = link
        elif line[0].startswith('White paper'):
            link = div.a.get('href')
            if link:
                data[line[0]] = link
        else:pass
    return data
        
        
#def get_team_details(soup):
    """
    updating..
    get team details from linkedin
    """
    
#def get_news(soup):
    """
    updaing...
    get all news about this project from ICOmarks.com
    get all twitters/facebook info from icomarks.com
    """
#==========main========================================

chrome_path = os.getcwd()
driver = webdriver.Chrome(chrome_path+'/chromedriver')
driver.get("https://icomarks.com/icos")
click_more = True
count_page=1
page_click=10000
while count_page<=page_click:
    if count_page%20==0:rest=30
    else:rest=2
    time.sleep(rest)
    element = driver.find_element_by_id("show-more")
    try:
        if element:
            element.click()
            print(count_page)
            count_page+=1
        else:
            time.sleep(2)
    except:
        print('click wrong')
        pass
       
soup=BeautifulSoup(driver.page_source,'lxml')
icoListItem=soup.find_all('div',{'class':'icoListItem'})
ico_a_tag=soup.find_all('a',{'class':'icoListItem__title'})
lst=[]
for tag in ico_a_tag:
    #name=re.findall(r'[a-zA-Z0-9]+$',tag.get('href'))[0]
    lst.append(tag.get('href'))
linkscount=pd.DataFrame(lst)
linkscount=linkscount.drop_duplicates()

# if input links by read_csv, cases=links, anyway, you can easily change the cases size
cases=linkscount  
df=pd.DataFrame()
for idx in cases.index:
    name,url=cases.iloc[idx,0],cases.iloc[idx,1]    
    soup=get_ico_page(url)
    data=get_ICO_details(soup,name)
    keys=['project name', 'Website:', 'White paper:', 'Country', 'Ticker',
          'Total supply', 'ICO Price',  'Hard cap',  'Twitter',  'Linkedin']
    for key in keys:
        if key in data.keys():
            df.loc[idx,key]=data[key]
        else:pass


#links=pd.DataFrame.from_dict(dict_,orient='index')
linkscount.to_csv('links.csv')
df.to_csv('data_icomark.csv')
