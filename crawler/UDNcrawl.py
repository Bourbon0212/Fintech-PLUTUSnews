# -*- coding: utf-8 -*-
"""
Created on Sun May 24 17:30:44 2020

@author: dx788
"""
    
import requests
import pandas as pd
from bs4 import BeautifulSoup

def UDNcrawl(keyword, strBegin, strEnd):
    
    '''
    Web News Crawler from UDN.
    
    Parameters:
        keyword (str): Interested topic
        strBegin (str): News start time
        strEnd (str): News end time

    Returns:
        result (pd.DataFrame): News crawl results
    '''   
    
    # strBegin = '20120501'
    # strEnd = '20120630'
 
    # Big5 Encoding
    opt = ''
    for char in keyword:
        tmp = str(char.encode('big5')).replace("\\x", "%")
        tmp = tmp.replace("b'", "")
        tmp = tmp.replace("'", "")
        opt += tmp
        opt = opt.upper()
    
    url = 'https://udndata.com/ndapp/Searchdec?udndbid=udndata&page=1&SearchString={}%2B%A4%E9%B4%C1%3E%3D{}%2B%A4%E9%B4%C1%3C%3D{}%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8%7C%C1%70%A6%58%B1%DF%B3%F8%7CUpaper&sharepage=50&select=1&kind=2'
    r = requests.get(url.format(opt, strBegin, strEnd))
    html_doc = r.text
    soup = BeautifulSoup(html_doc)
    posts = soup.find_all('div', class_ ="news")

    link = []
    title = []
    summary = []
    
    for post in posts:
        link.append('https://udndata.com' + post.find('a').get('href'))
        title.append(post.find('a').text)
        summary.append(post.find('p').text)
    
    temp = {'link':link, 'title':title, 'summary':summary}
    result = pd.DataFrame(temp)
    return result

df = UDNcrawl('美吾華', '20200101', '20200524')
        
# rr = requests.get(postUrl)
# html_doc = rr.text
# soup = BeautifulSoup(html_doc)
# content = soup.find('div', {"itemprop":"articleBody"}).text