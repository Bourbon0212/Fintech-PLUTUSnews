# -*- coding: utf-8 -*-
"""
Created on Sun May 24 13:55:06 2020

@author: dx788
"""

import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

def CYNEScrawl(strBegin, strEnd):
    
    '''
    Web News Crawler from CYNES.
    
    Parameters:
    strBegin (str): News start time
    strEnd (str): News end time

    Returns:
    result (pd.DataFrame): News crawl results
    '''
    
    # Strbegine = '2020-01-01 16:00:00' 
    # Strend = '2020-01-01 18:59:59'
    
    # 日期字串轉成時間格式
    begineTime = time.strptime(strBegin,"%Y-%m-%d %H:%M:%S")
    endTime = time.strptime(strEnd,"%Y-%m-%d %H:%M:%S")
    # 時間格式轉換成時間戳記
    startAt = int(time.mktime(begineTime))
    endAt = int(time.mktime(endTime))
    
    url = "https://news.cnyes.com/api/v3/news/category/tw_stock?startAt={}&endAt={}"
    postUrl = "https://news.cnyes.com/news/id/{}?exp=a"
    
    r = requests.get(url.format(startAt, endAt))
    json_data = r.json()
    posts = json_data['items']['data']
    
    publish = []
    title = []
    context = []
    
    for post in posts:
        rr = requests.get(postUrl.format(post['newsId']))
        html_doc = rr.text
        soup = BeautifulSoup(html_doc)
        content = soup.find('div', {"itemprop":"articleBody"}).text
        
        publish.append(post['publishAt'])
        title.append(post['title'])
        context.append(content)
        # print('---{}---'.format(post['title']))
        # print(content)
    
    temp = {'time':publish, 'title':title, 'context':context}
    result = pd.DataFrame(temp)
    return result

df = CYNEScrawl('2020-04-01 16:00:00', '2020-04-30 18:59:59')
