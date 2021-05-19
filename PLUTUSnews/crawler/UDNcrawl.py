# -*- coding: utf-8 -*-
"""
Created on Sun May 24 17:30:44 2020

@author: dx788
"""

import re
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

    time = []
    link = []
    title = []
    summary = []
    
    for post in posts:
        time.append(strBegin)
        link.append('https://udndata.com' + post.find('a').get('href'))
        title.append(re.findall('\..+$', post.find('a').text)[0][1:])
        summary.append(post.find('p').text)
    
    temp = {'time':time, 'link':link, 'title':title, 'summary':summary}
    result = pd.DataFrame(temp)
    return result

### Crawl UDN All Year

# Create Time Query LUT
# month = ['{num:02d}'.format(num=i) for i in range(1, 13)]
# day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Initialize the empty df
# df = pd.DataFrame()

# for i in range(12):
#    for j in range(1, day[i]+1):
#        query = '2019' + month[i] + str('{num:02d}'.format(num=j))
#        print(query)
#        result = UDNcrawl('防疫概念股', query, query)
#        df = df.append(result)

# df = df.reset_index()
# df.to_csv('UDN_2019.csv', index=False)

### Crawl UDN One News Post

# rr = requests.get(postUrl)
# html_doc = rr.text
# soup = BeautifulSoup(html_doc)
# content = soup.find('div', {"itemprop":"articleBody"}).text

### Crawl UND One Day
    
# dd = UDNcrawl('防疫', '20210425', '20210425')
# dd.to_csv('UDN_6.csv', index=False)