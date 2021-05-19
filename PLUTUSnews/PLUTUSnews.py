# -*- coding: utf-8 -*-
"""
Created on Sun May 31 19:32:50 2020

@author: dx788
"""

import pickle
import pandas as pd

from PLUTUSnews.crawler.UDNcrawl import UDNcrawl
from PLUTUSnews.segmenter.CKIPsegmenter import CKIPsegmenter

def PLUTUSnews(date, stock, importance):
    
    '''
    Collect those news that matters.
    
    Parameters:
        date (str): Query date
        stock (list): Interested stock
        importance (float): Importance sensitivity for news

    Returns:
        news_result (pd.DataFrame): News that regarding the topic
        stock_result (pd.DataFrame): News that regarding the interested stocks
    '''
    
    # date = 20200607''
    # stock = ['美吾華', '恆大']
    
    # 讀入詞庫
    with open('./PLUTUSnews/word_freq.pkl', 'rb') as file:
        df_t = pickle.load(file)
        
    # 讀入新聞分類模型
    with open('./PLUTUSnews/NEWSrf_model.pkl', 'rb') as file:
        rf_cv = pickle.load(file)

    # 詞庫有關防疫的詞彙
    word_bags = df_t.columns[0:-1]

    # 當日新聞詞頻矩陣
    news = UDNcrawl('防疫', date, date)
    
    try:
        # 當日新聞的詞頻矩陣
        news_t = CKIPsegmenter(news, 0)
        
        # 將當日新聞詞頻矩陣與詞庫連結
        df_full = pd.concat([news_t, df_t])
        df_news = df_full.loc[:,word_bags].iloc[:len(news_t)]
        df_news = df_news.fillna(0)
    
        # 當日新聞分類結果
        news['prob'] = rf_cv.predict(df_news)
        news_result = news[news['prob'] > importance]
        news_result = news_result.iloc[:,:4]
        print('PLUTUS news sucess!!')
        
    except:
        # 有 Error 的話回傳空資料表 (通常是中文轉碼錯誤)
        print('CKIP encoding error :' + date)
        news_result = pd.DataFrame()
        
    # 搜尋有關個股新聞
    stock_result = pd.DataFrame()

    for i in stock:
        temp = UDNcrawl(i, date, date)
        stock_result = stock_result.append(temp)
        
    return news_result, stock_result

# nn, ss = PLUTUSnews('20210425', ['美吾華', '恆大'], 0.3)